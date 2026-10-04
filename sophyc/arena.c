#include "arena.h"

Arena arena_init(void* backing_buffer, size_t capacity) {
    Arena a = {
        .buffer = (uint8_t*)backing_buffer,
        .capacity = capacity,
        .offset = 0
    };
    return a;
}

void* arena_alloc(Arena* a, size_t size) {
    // Ensure memory alignment (8 bytes for standard 64-bit safety)
    size_t aligned_size = (size + 7) & ~7;
    
    if (a->offset + aligned_size > a->capacity) {
        return NULL; // Out of memory, deterministic failure, prevents segfault
    }
    
    void* ptr = &a->buffer[a->offset];
    a->offset += aligned_size;
    return ptr;
}

void arena_reset(Arena* a) {
    a->offset = 0; // O(1) functional garbage collection
}
