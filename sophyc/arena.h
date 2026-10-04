#ifndef SOPHY_ARENA_H
#define SOPHY_ARENA_H

#include <stddef.h>
#include <stdint.h>

// Static memory arena for deterministic, malloc-free allocations
typedef struct {
    uint8_t* buffer;
    size_t capacity;
    size_t offset;
} Arena;

Arena arena_init(void* backing_buffer, size_t capacity);
void* arena_alloc(Arena* a, size_t size);
void arena_reset(Arena* a);

#endif
