/*
 * This file is part of Sweetbrier-Node (sophy.c architecture).
 *
 * Sweetbrier-Node is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Sweetbrier-Node is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Sweetbrier-Node.  If not, see <https://www.gnu.org/licenses/>.
 */
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

