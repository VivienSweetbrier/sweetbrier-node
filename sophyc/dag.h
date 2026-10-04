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
