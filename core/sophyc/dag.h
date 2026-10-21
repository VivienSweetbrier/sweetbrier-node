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
#ifndef SOPHY_DAG_H
#define SOPHY_DAG_H

#include <stdbool.h>
#include <stddef.h>

// OpCodes for the Neurosymbolic Logic Gates
typedef enum {
    OP_ROOT,
    OP_REQUIRE_DIGNITY,     // Node_0: Epistemic violence check
    OP_VERIFY_PHENOMENOLOGY,// Node_1: Indigenous data check
    OP_D_SEPARATION_GATE,   // Causal blocker
    OP_EXECUTE_LLM          // Safe execution pass
} OpCode;

// Immutable DAG Node
typedef struct DagNode {
    OpCode op;
    const char* payload; 
    struct DagNode** children;
    size_t child_count;
} DagNode;

typedef struct {
    bool is_safe;
    const char* rejection_reason;
} EvalResult;

#endif

