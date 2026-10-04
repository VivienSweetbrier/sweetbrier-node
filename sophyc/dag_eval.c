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
#include "dag.h"
#include "arena.h"
#include <stdio.h>

// Evaluates the DAG using an explicit stack allocated in the Arena
EvalResult evaluate_dag(Arena* arena, const DagNode* root) {
    EvalResult result = { .is_safe = true, .rejection_reason = "Safe" };
    
    if (!root) return result;

    // Allocate our explicit traversal stack inside the Arena
    // Supporting a maximum depth of 1024 nodes
    size_t max_stack = 1024;
    const DagNode** stack = arena_alloc(arena, sizeof(DagNode*) * max_stack);
    if (!stack) {
        return (EvalResult){false, "ERR: Arena Exhausted on Stack Allocation"};
    }

    size_t stack_idx = 0;
    stack[stack_idx++] = root;

    while (stack_idx > 0) {
        const DagNode* current = stack[--stack_idx];

        // Evaluate the neurosymbolic logic gate
        switch (current->op) {
            case OP_REQUIRE_DIGNITY:
                if (!current->payload) {
                    return (EvalResult){false, "ERR: Node_0 Dignity Violation"};
                }
                break;
            case OP_VERIFY_PHENOMENOLOGY:
                if (!current->payload) {
                    return (EvalResult){false, "ERR: Node_1 Phenomenology Violation"};
                }
                break;
            case OP_D_SEPARATION_GATE:
                // Block causal drift
                if (current->child_count > 2) {
                    return (EvalResult){false, "ERR: Causal Drift Detected (>2 vectors)"};
                }
                break;
            case OP_EXECUTE_LLM:
            case OP_ROOT:
            default:
                break;
        }

        // Push children to the explicit stack
        for (size_t i = 0; i < current->child_count; i++) {
            if (stack_idx >= max_stack) {
                return (EvalResult){false, "ERR: Stack Overflow Prevented (DAG Too Deep)"};
            }
            stack[stack_idx++] = current->children[i];
        }
    }

    return result;
}

