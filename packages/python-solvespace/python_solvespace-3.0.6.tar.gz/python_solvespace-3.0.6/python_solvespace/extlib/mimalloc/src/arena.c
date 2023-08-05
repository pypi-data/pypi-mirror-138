/* ----------------------------------------------------------------------------
Copyright (c) 2019, 2020, Microsoft Research, Daan Leijen
This is free software; you can redistribute it and/or modify it under the
terms of the MIT license. A copy of the license can be found in the file
"LICENSE" at the root of this distribution.
-----------------------------------------------------------------------------*/

/* ----------------------------------------------------------------------------
"Arenas" are fixed area's of OS memory from which we can allocate
large blocks (>= MI_ARENA_MIN_BLOCK_SIZE, 4MiB).
In contrast to the rest of mimalloc, the arenas are shared between
threads and need to be accessed using atomic operations.

Currently arenas are only used to for huge OS page (1GiB) reservations,
or direct OS memory reservations -- otherwise it delegates to direct allocation from the OS.
In the future, we can expose an API to manually add more kinds of arenas
which is sometimes needed for embedded devices or shared memory for example.
(We can also employ this with WASI or `sbrk` systems to reserve large arenas
 on demand and be able to reuse them efficiently).

The arena allocation needs to be thread safe and we use an atomic bitmap to allocate.
-----------------------------------------------------------------------------*/
#include "mimalloc.h"
#include "mimalloc-internal.h"
#include "mimalloc-atomic.h"

#include <string.h>  // memset
#include <errno.h> // ENOMEM

#include "bitmap.h"  // atomic bitmap


// os.c
void* _mi_os_alloc_aligned(size_t size, size_t alignment, bool commit, bool* large, mi_stats_t* stats);
void  _mi_os_free_ex(void* p, size_t size, bool was_committed, mi_stats_t* stats);

void* _mi_os_alloc_huge_os_pages(size_t pages, int numa_node, mi_msecs_t max_secs, size_t* pages_reserved, size_t* psize);
void  _mi_os_free_huge_pages(void* p, size_t size, mi_stats_t* stats);

bool  _mi_os_commit(void* p, size_t size, bool* is_zero, mi_stats_t* stats);
bool  _mi_os_decommit(void* addr, size_t size, mi_stats_t* stats);


/* -----------------------------------------------------------
  Arena allocation
----------------------------------------------------------- */


// Block info: bit 0 contains the `in_use` bit, the upper bits the
// size in count of arena blocks.
typedef uintptr_t mi_block_info_t;
#define MI_ARENA_BLOCK_SIZE   (MI_SEGMENT_SIZE)        // 8MiB  (must be at least MI_SEGMENT_ALIGN)
#define MI_ARENA_MIN_OBJ_SIZE (MI_ARENA_BLOCK_SIZE/2)  // 4MiB
#define MI_MAX_ARENAS         (64)                     // not more than 256 (since we use 8 bits in the memid)

// A memory arena descriptor
typedef struct mi_arena_s {
  _Atomic(uint8_t*) start;                // the start of the memory area
  size_t   block_count;                   // size of the area in arena blocks (of `MI_ARENA_BLOCK_SIZE`)
  size_t   field_count;                   // number of bitmap fields (where `field_count * MI_BITMAP_FIELD_BITS >= block_count`)
  int      numa_node;                     // associated NUMA node
  bool     is_zero_init;                  // is the arena zero initialized?
  bool     is_committed;                  // is the memory fully committed? (if so, block_committed == NULL)
  bool     is_large;                      // large- or huge OS pages (always committed)
  _Atomic(uintptr_t) search_idx;          // optimization to start the search for free blocks
  mi_bitmap_field_t* blocks_dirty;        // are the blocks potentially non-zero?
  mi_bitmap_field_t* blocks_committed;    // if `!is_committed`, are the blocks committed?
  mi_bitmap_field_t  blocks_inuse[1];     // in-place bitmap of in-use blocks (of size `field_count`)
} mi_arena_t;


// The available arenas
static mi_decl_cache_align _Atomic(mi_arena_t*) mi_arenas[MI_MAX_ARENAS];
static mi_decl_cache_align _Atomic(uintptr_t)   mi_arena_count; // = 0


/* -----------------------------------------------------------
  Arena allocations get a memory id where the lower 8 bits are
  the arena index +1, and the upper bits the block index.
----------------------------------------------------------- */

// Use `0` as a special id for direct OS allocated memory.
#define MI_MEMID_OS   0

static size_t mi_arena_id_create(size_t arena_index, mi_bitmap_index_t bitmap_index) {
  mi_assert_internal(arena_index < 0xFE);
  mi_assert_internal(((bitmap_index << 8) >> 8) == bitmap_index); // no overflow?
  return ((bitmap_index << 8) | ((arena_index+1) & 0xFF));
}

static void mi_arena_id_indices(size_t memid, size_t* arena_index, mi_bitmap_index_t* bitmap_index) {
  mi_assert_internal(memid != MI_MEMID_OS);
  *arena_index = (memid & 0xFF) - 1;
  *bitmap_index = (memid >> 8);
}

static size_t mi_block_count_of_size(size_t size) {
  return _mi_divide_up(size, MI_ARENA_BLOCK_SIZE);
}

/* -----------------------------------------------------------
  Thread safe allocation in an arena
----------------------------------------------------------- */
static bool mi_arena_alloc(mi_arena_t* arena, size_t blocks, mi_bitmap_index_t* bitmap_idx)
{
  size_t idx = 0; // mi_atomic_load_relaxed(&arena->search_idx);  // start from last search; ok to be relaxed as the exact start does not matter
  if (_mi_bitmap_try_find_from_claim_across(arena->blocks_inuse, arena->field_count, idx, blocks, bitmap_idx)) {
    mi_atomic_store_relaxed(&arena->search_idx, mi_bitmap_index_field(*bitmap_idx));  // start search from found location next time around
    return true;
  };
  return false;
}


/* -----------------------------------------------------------
  Arena Allocation
----------------------------------------------------------- */

static mi_decl_noinline void* mi_arena_alloc_from(mi_arena_t* arena, size_t arena_index, size_t needed_bcount,
                                                  bool* commit, bool* large, bool* is_pinned, bool* is_zero, size_t* memid, mi_os_tld_t* tld)
{
  mi_bitmap_index_t bitmap_index;
  if (!mi_arena_alloc(arena, needed_bcount, &bitmap_index)) return NULL;

  // claimed it! set the dirty bits (todo: no need for an atomic op here?)
  void* p    = arena->start + (mi_bitmap_index_bit(bitmap_index)*MI_ARENA_BLOCK_SIZE);
  *memid     = mi_arena_id_create(arena_index, bitmap_index);
  *is_zero   = _mi_bitmap_claim_across(arena->blocks_dirty, arena->field_count, needed_bcount, bitmap_index, NULL);
  *large     = arena->is_large;
  *is_pinned = (arena->is_large || arena->is_committed);
  if (arena->is_committed) {
    // always committed
    *commit = true;
  }
  else if (*commit) {
    // arena not committed as a whole, but commit requested: ensure commit now
    bool any_uncommitted;
    _mi_bitmap_claim_across(arena->blocks_committed, arena->field_count, needed_bcount, bitmap_index, &any_uncommitted);
    if (any_uncommitted) {
      bool commit_zero;
      _mi_os_commit(p, needed_bcount * MI_ARENA_BLOCK_SIZE, &commit_zero, tld->stats);
      if (commit_zero) *is_zero = true;
    }
  }
  else {
    // no need to commit, but check if already fully committed
    *commit = _mi_bitmap_is_claimed_across(arena->blocks_committed, arena->field_count, needed_bcount, bitmap_index);
  }
  return p;
}

static mi_decl_noinline void* mi_arena_allocate(int numa_node, size_t size, size_t alignment, bool* commit, bool* large, bool* is_pinned, bool* is_zero, size_t* memid, mi_os_tld_t* tld)
{  
  UNUSED_RELEASE(alignment);
  mi_assert_internal(alignment <= MI_SEGMENT_ALIGN);
  const size_t max_arena = mi_atomic_load_relaxed(&mi_arena_count);  
  const size_t bcount = mi_block_count_of_size(size);
  if (mi_likely(max_arena == 0)) return NULL;
  mi_assert_internal(size <= bcount*MI_ARENA_BLOCK_SIZE);

  // try numa affine allocation
  for (size_t i = 0; i < max_arena; i++) {
    mi_arena_t* arena = mi_atomic_load_ptr_relaxed(mi_arena_t, &mi_arenas[i]);
    if (arena==NULL) break; // end reached
    if ((arena->numa_node<0 || arena->numa_node==numa_node) && // numa local?
      (*large || !arena->is_large)) // large OS pages allowed, or arena is not large OS pages
    {
      void* p = mi_arena_alloc_from(arena, i, bcount, commit, large, is_pinned, is_zero, memid, tld);
      mi_assert_internal((uintptr_t)p % alignment == 0);
      if (p != NULL) {
        return p;
      }
    }
  }

  // try from another numa node instead..
  for (size_t i = 0; i < max_arena; i++) {
    mi_arena_t* arena = mi_atomic_load_ptr_relaxed(mi_arena_t, &mi_arenas[i]);
    if (arena==NULL) break; // end reached
    if ((arena->numa_node>=0 && arena->numa_node!=numa_node) && // not numa local!
      (*large || !arena->is_large)) // large OS pages allowed, or arena is not large OS pages
    {
      void* p = mi_arena_alloc_from(arena, i, bcount, commit, large, is_pinned, is_zero, memid, tld);
      mi_assert_internal((uintptr_t)p % alignment == 0);
      if (p != NULL) {
        return p;
      }
    }
  }
  return NULL;
}


void* _mi_arena_alloc_aligned(size_t size, size_t alignment, bool* commit, bool* large, bool* is_pinned, bool* is_zero,
                              size_t* memid, mi_os_tld_t* tld)
{
  mi_assert_internal(commit != NULL && is_pinned != NULL && is_zero != NULL && memid != NULL && tld != NULL);
  mi_assert_internal(size > 0);
  *memid   = MI_MEMID_OS;
  *is_zero = false;
  *is_pinned = false;

  bool default_large = false;
  if (large==NULL) large = &default_large;     // ensure `large != NULL`
  const int numa_node = _mi_os_numa_node(tld); // current numa node

  // try to allocate in an arena if the alignment is small enough and the object is not too small (as for heap meta data)
  if (size >= MI_ARENA_MIN_OBJ_SIZE && alignment <= MI_SEGMENT_ALIGN) {
    void* p = mi_arena_allocate(numa_node, size, alignment, commit, large, is_pinned, is_zero, memid, tld);
    if (p != NULL) return p;
  }

  // finally, fall back to the OS
  if (mi_option_is_enabled(mi_option_limit_os_alloc)) {
    errno = ENOMEM;
    return NULL;
  }
  *is_zero = true;
  *memid   = MI_MEMID_OS;  
  void* p = _mi_os_alloc_aligned(size, alignment, *commit, large, tld->stats);
  if (p != NULL) *is_pinned = *large;
  return p;
}

void* _mi_arena_alloc(size_t size, bool* commit, bool* large, bool* is_pinned, bool* is_zero, size_t* memid, mi_os_tld_t* tld)
{
  return _mi_arena_alloc_aligned(size, MI_ARENA_BLOCK_SIZE, commit, large, is_pinned, is_zero, memid, tld);
}

/* -----------------------------------------------------------
  Arena free
----------------------------------------------------------- */

void _mi_arena_free(void* p, size_t size, size_t memid, bool all_committed, mi_os_tld_t* tld) {
  mi_assert_internal(size > 0 && tld->stats != NULL);
  if (p==NULL) return;
  if (size==0) return;

  if (memid == MI_MEMID_OS) {
    // was a direct OS allocation, pass through
    _mi_os_free_ex(p, size, all_committed, tld->stats);
  }
  else {
    // allocated in an arena
    size_t arena_idx;
    size_t bitmap_idx;
    mi_arena_id_indices(memid, &arena_idx, &bitmap_idx);
    mi_assert_internal(arena_idx < MI_MAX_ARENAS);
    mi_arena_t* arena = mi_atomic_load_ptr_relaxed(mi_arena_t,&mi_arenas[arena_idx]);
    mi_assert_internal(arena != NULL);
    const size_t blocks = mi_block_count_of_size(size);
    // checks
    if (arena == NULL) {
      _mi_error_message(EINVAL, "trying to free from non-existent arena: %p, size %zu, memid: 0x%zx\n", p, size, memid);
      return;
    }
    mi_assert_internal(arena->field_count > mi_bitmap_index_field(bitmap_idx));
    if (arena->field_count <= mi_bitmap_index_field(bitmap_idx)) {
      _mi_error_message(EINVAL, "trying to free from non-existent arena block: %p, size %zu, memid: 0x%zx\n", p, size, memid);
      return;
    }
    // potentially decommit
    if (arena->is_committed) {
      mi_assert_internal(all_committed); // note: may be not true as we may "pretend" to be not committed (in segment.c)
    }
    else {
      mi_assert_internal(arena->blocks_committed != NULL);
      _mi_os_decommit(p, blocks * MI_ARENA_BLOCK_SIZE, tld->stats); // ok if this fails
      _mi_bitmap_unclaim_across(arena->blocks_committed, arena->field_count, blocks, bitmap_idx);
    }
    // and make it available to others again 
    bool all_inuse = _mi_bitmap_unclaim_across(arena->blocks_inuse, arena->field_count, blocks, bitmap_idx);
    if (!all_inuse) {
      _mi_error_message(EAGAIN, "trying to free an already freed block: %p, size %zu\n", p, size);
      return;
    };
  }
}

/* -----------------------------------------------------------
  Add an arena.
----------------------------------------------------------- */

static bool mi_arena_add(mi_arena_t* arena) {
  mi_assert_internal(arena != NULL);
  mi_assert_internal((uintptr_t)mi_atomic_load_ptr_relaxed(uint8_t,&arena->start) % MI_SEGMENT_ALIGN == 0);
  mi_assert_internal(arena->block_count > 0);

  uintptr_t i = mi_atomic_increment_acq_rel(&mi_arena_count);
  if (i >= MI_MAX_ARENAS) {
    mi_atomic_decrement_acq_rel(&mi_arena_count);
    return false;
  }
  mi_atomic_store_ptr_release(mi_arena_t,&mi_arenas[i], arena);
  return true;
}

bool mi_manage_os_memory(void* start, size_t size, bool is_committed, bool is_large, bool is_zero, int numa_node) mi_attr_noexcept
{
  if (is_large) {
    mi_assert_internal(is_committed);
    is_committed = true;
  }
  
  const size_t bcount = mi_block_count_of_size(size);
  const size_t fields = _mi_divide_up(bcount, MI_BITMAP_FIELD_BITS);
  const size_t bitmaps = (is_committed ? 2 : 3);
  const size_t asize  = sizeof(mi_arena_t) + (bitmaps*fields*sizeof(mi_bitmap_field_t));
  mi_arena_t* arena   = (mi_arena_t*)_mi_os_alloc(asize, &_mi_stats_main); // TODO: can we avoid allocating from the OS?
  if (arena == NULL) return false;

  arena->block_count = bcount;
  arena->field_count = fields;
  arena->start = (uint8_t*)start;
  arena->numa_node    = numa_node; // TODO: or get the current numa node if -1? (now it allows anyone to allocate on -1)
  arena->is_large     = is_large;
  arena->is_zero_init = is_zero;
  arena->is_committed = is_committed;
  arena->search_idx   = 0;
  arena->blocks_dirty = &arena->blocks_inuse[fields]; // just after inuse bitmap
  arena->blocks_committed = (is_committed ? NULL : &arena->blocks_inuse[2*fields]); // just after dirty bitmap
  // the bitmaps are already zero initialized due to os_alloc
  // just claim leftover blocks if needed
  ptrdiff_t post = (fields * MI_BITMAP_FIELD_BITS) - bcount;
  mi_assert_internal(post >= 0);
  if (post > 0) {
    // don't use leftover bits at the end
    mi_bitmap_index_t postidx = mi_bitmap_index_create(fields - 1, MI_BITMAP_FIELD_BITS - post);
    _mi_bitmap_claim(arena->blocks_inuse, fields, post, postidx, NULL);
  }

  mi_arena_add(arena);
  return true;
}

// Reserve a range of regular OS memory
int mi_reserve_os_memory(size_t size, bool commit, bool allow_large) mi_attr_noexcept 
{
  size = _mi_os_good_alloc_size(size);
  bool large = allow_large;
  void* start = _mi_os_alloc_aligned(size, MI_SEGMENT_ALIGN, commit, &large, &_mi_stats_main);
  if (start==NULL) return ENOMEM;
  if (!mi_manage_os_memory(start, size, (large || commit), large, true, -1)) {
    _mi_os_free_ex(start, size, commit, &_mi_stats_main);
    _mi_verbose_message("failed to reserve %zu k memory\n", _mi_divide_up(size,1024));
    return ENOMEM;
  }
  _mi_verbose_message("reserved %zu kb memory%s\n", _mi_divide_up(size,1024), large ? " (in large os pages)" : "");
  return 0;
}

static size_t mi_debug_show_bitmap(const char* prefix, mi_bitmap_field_t* fields, size_t field_count ) {
  size_t inuse_count = 0;
  for (size_t i = 0; i < field_count; i++) {
    char buf[MI_BITMAP_FIELD_BITS + 1];
    uintptr_t field = mi_atomic_load_relaxed(&fields[i]);
    for (size_t bit = 0; bit < MI_BITMAP_FIELD_BITS; bit++) {
      bool inuse = ((((uintptr_t)1 << bit) & field) != 0);
      if (inuse) inuse_count++;
      buf[MI_BITMAP_FIELD_BITS - 1 - bit] = (inuse ? 'x' : '.');
    }
    buf[MI_BITMAP_FIELD_BITS] = 0;
    _mi_verbose_message("%s%s\n", prefix, buf);
  }
  return inuse_count;
}

void mi_debug_show_arenas(void) mi_attr_noexcept {
  size_t max_arenas = mi_atomic_load_relaxed(&mi_arena_count);
  for (size_t i = 0; i < max_arenas; i++) {
    mi_arena_t* arena = mi_atomic_load_ptr_relaxed(mi_arena_t, &mi_arenas[i]);
    if (arena == NULL) break;
    size_t inuse_count = 0;
    _mi_verbose_message("arena %zu: %zu blocks with %zu fields\n", i, arena->block_count, arena->field_count);
    inuse_count += mi_debug_show_bitmap("  ", arena->blocks_inuse, arena->field_count);
    _mi_verbose_message("  blocks in use ('x'): %zu\n", inuse_count);
  }
}

/* -----------------------------------------------------------
  Reserve a huge page arena.
----------------------------------------------------------- */
// reserve at a specific numa node
int mi_reserve_huge_os_pages_at(size_t pages, int numa_node, size_t timeout_msecs) mi_attr_noexcept {
  if (pages==0) return 0;
  if (numa_node < -1) numa_node = -1;
  if (numa_node >= 0) numa_node = numa_node % _mi_os_numa_node_count();
  size_t hsize = 0;
  size_t pages_reserved = 0;
  void* p = _mi_os_alloc_huge_os_pages(pages, numa_node, timeout_msecs, &pages_reserved, &hsize);
  if (p==NULL || pages_reserved==0) {
    _mi_warning_message("failed to reserve %zu gb huge pages\n", pages);
    return ENOMEM;
  }
  _mi_verbose_message("numa node %i: reserved %zu gb huge pages (of the %zu gb requested)\n", numa_node, pages_reserved, pages);

  if (!mi_manage_os_memory(p, hsize, true, true, true, numa_node)) {
    _mi_os_free_huge_pages(p, hsize, &_mi_stats_main);
    return ENOMEM;
  }
  return 0;
}


// reserve huge pages evenly among the given number of numa nodes (or use the available ones as detected)
int mi_reserve_huge_os_pages_interleave(size_t pages, size_t numa_nodes, size_t timeout_msecs) mi_attr_noexcept {
  if (pages == 0) return 0;

  // pages per numa node
  size_t numa_count = (numa_nodes > 0 ? numa_nodes : _mi_os_numa_node_count());
  if (numa_count <= 0) numa_count = 1;
  const size_t pages_per = pages / numa_count;
  const size_t pages_mod = pages % numa_count;
  const size_t timeout_per = (timeout_msecs==0 ? 0 : (timeout_msecs / numa_count) + 50);

  // reserve evenly among numa nodes
  for (size_t numa_node = 0; numa_node < numa_count && pages > 0; numa_node++) {
    size_t node_pages = pages_per;  // can be 0
    if (numa_node < pages_mod) node_pages++;
    int err = mi_reserve_huge_os_pages_at(node_pages, (int)numa_node, timeout_per);
    if (err) return err;
    if (pages < node_pages) {
      pages = 0;
    }
    else {
      pages -= node_pages;
    }
  }

  return 0;
}

int mi_reserve_huge_os_pages(size_t pages, double max_secs, size_t* pages_reserved) mi_attr_noexcept {
  UNUSED(max_secs);
  _mi_warning_message("mi_reserve_huge_os_pages is deprecated: use mi_reserve_huge_os_pages_interleave/at instead\n");
  if (pages_reserved != NULL) *pages_reserved = 0;
  int err = mi_reserve_huge_os_pages_interleave(pages, 0, (size_t)(max_secs * 1000.0));
  if (err==0 && pages_reserved!=NULL) *pages_reserved = pages;
  return err;
}
