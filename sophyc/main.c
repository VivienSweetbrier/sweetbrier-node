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
#include <stdio.h>
#include <stdlib.h>
#include "arena.h"
#include "dag.h"

// Forward declaration of our pure function evaluator
extern EvalResult evaluate_dag(Arena* arena, const DagNode* root);

int main() {
    printf("[SOPHY.C] Booting Sweetbrier-Node Bare-Metal Chassis...\n");

    // 1. Pre-allocate the memory buffer (1MB Arena)
    // (Using standard malloc ONLY ONCE at boot to get the OS memory block, 
    //  from here on out, it is strictly malloc-free pointer bumping).
    size_t arena_size = 1024 * 1024; 
    void* backing_memory = malloc(arena_size);
    if(!backing_memory) {
        printf("[SOPHY.C] FAILED to secure OS memory block.\n");
        return 1;
    }

    Arena arena = arena_init(backing_memory, arena_size);
    printf("[SOPHY.C] Arena Initialized (1MB). Malloc locked.\n");

    // 2. Build an immutable DAG in the Arena
    DagNode* root = arena_alloc(&arena, sizeof(DagNode));
    root->op = OP_ROOT;
    root->child_count = 2;
    root->children = arena_alloc(&arena, sizeof(DagNode*) * 2);

    // Child 1: Node_0 check
    DagNode* child1 = arena_alloc(&arena, sizeof(DagNode));
    child1->op = OP_REQUIRE_DIGNITY;
    child1->payload = "Valid Human Context"; // Try setting to NULL to trigger safety tripwire
    child1->child_count = 0;
    root->children[0] = child1;

    // Child 2: Causal d-separation blocker
    DagNode* child2 = arena_alloc(&arena, sizeof(DagNode));
    child2->op = OP_D_SEPARATION_GATE;
    child2->payload = NULL;
    child2->child_count = 0; // Safe (count <= 2)
    root->children[1] = child2;

    printf("[SOPHY.C] Evaluating Circuit Breaker DAG...\n");
    EvalResult result = evaluate_dag(&arena, root);

    if (result.is_safe) {
        printf("[SOPHY.C] STATUS: OK - %s\n", result.rejection_reason);
    } else {
        printf("[SOPHY.C] STATUS: BLOCKED - %s\n", result.rejection_reason);
    }

    // 3. O(1) Memory Reset
    arena_reset(&arena);
    printf("[SOPHY.C] Arena reset. Ready for next cycle in O(1) time.\n");

    free(backing_memory); // OS shutdown
    return 0;
}

