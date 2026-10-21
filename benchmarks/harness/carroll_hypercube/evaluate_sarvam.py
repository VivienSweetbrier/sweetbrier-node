"""
evaluate_sarvam.py 🌸❎
Native Windows Sovereign AI Constraint Evaluator for sarvamai/sarvam-1.
Bypasses POSIX-only vLLM/uvloop by running Hugging Face Transformers directly on Windows,
gating outputs through the Lewis Carroll Hypercube (Q_3) in carroll_gate.py,
and sealing reasoning traces with Accelerando-8192 reversible glyph stigmergy.
Attestation: probabilistic_structural (Sweetbrier Master DAG □ Verified)
"""

import argparse
import hashlib
import json
import sys
import time
from typing import Any, Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from carroll_gate import CarrollHypercube

MODEL_NAME = "sarvamai/sarvam-1"
PUA_BASE = 0xF0000
VOCAB_SIZE = 8192  # U+F0000 .. U+F1FFF


# ==============================================================================
# 1. Accelerando-8192 Bijective Glyph Codec (Node 1 & Node 2 Reversibility)
# ==============================================================================
def load_accelerando_ranks() -> Tuple[Dict[bytes, int], Dict[int, bytes]]:
    """
    Load the first 8,192 ranks:
      - Ranks 0..255: lossless single-byte identity table bytes([b]) -> b
      - Ranks 256..8191: first 7,936 multi-byte BPE merges of o200k_base
    """
    enc_map: Dict[bytes, int] = {bytes([b]): b for b in range(256)}
    try:
        import tiktoken
        bpe = tiktoken.get_encoding("o200k_base")
        multi_byte = sorted(
            ((rank, tok) for tok, rank in bpe._mergeable_ranks.items() if len(tok) > 1),
            key=lambda x: x[0],
        )
        next_rank = 256
        for _, token_bytes in multi_byte:
            if next_rank >= VOCAB_SIZE:
                break
            enc_map[token_bytes] = next_rank
            next_rank += 1
    except Exception:
        pass
    dec_map: Dict[int, bytes] = {rank: tok for tok, rank in enc_map.items()}
    return enc_map, dec_map


def encode_accelerando(text: str) -> str:
    """Encode UTF-8 text into U+F0000..U+F1FFF Accelerando-8192 glyphs."""
    enc_map, _ = load_accelerando_ranks()
    raw = text.encode("utf-8")
    n = len(raw)
    i = 0
    glyphs: List[str] = []
    while i < n:
        matched_rank = raw[i]
        matched_len = 1
        max_w = min(16, n - i)
        for w in range(max_w, 1, -1):
            cand = raw[i : i + w]
            if cand in enc_map:
                matched_rank = enc_map[cand]
                matched_len = w
                break
        glyphs.append(chr(PUA_BASE + matched_rank))
        i += matched_len
    return "".join(glyphs)


def decode_accelerando(glyph_stream: str) -> str:
    """Bijectively decode U+F0000..U+F1FFF glyphs back to exact UTF-8 text."""
    _, dec_map = load_accelerando_ranks()
    out = bytearray()
    for ch in glyph_stream:
        code = ord(ch)
        if PUA_BASE <= code < PUA_BASE + VOCAB_SIZE:
            rank = code - PUA_BASE
            out.extend(dec_map.get(rank, bytes([rank & 0xFF])))
        else:
            out.extend(ch.encode("utf-8"))
    return out.decode("utf-8", errors="replace")


# ==============================================================================
# 2. Lewis Carroll Hypercube (Q_3) Maimonidean Trellis Gate
# ==============================================================================
def build_maimonidean_carroll_gate() -> CarrollHypercube:
    """
    Constructs the Triliteral Carroll Epistemic Gate (Q_3) for Sovereign AI:
      a: Non-Speculative (Zero unverified forecast markers)
      b: Sovereign-Grounded (Anchored in DPI / localized infrastructure / verifiable state)
      c: Logically Coherent (Structured, non-degenerate syntax)
    """
    gate = CarrollHypercube(["a", "b", "c"])
    # Universal Negation (GREY / ∅): Any missing invariant casts the output into darkness
    gate.set_compartment("a'", CarrollHypercube.GREY)
    gate.set_compartment("b'", CarrollHypercube.GREY)
    gate.set_compartment("c'", CarrollHypercube.GREY)
    # Existential Import (RED / ∃): All three Maimonidean nodes satisfied -> □P verified
    gate.set_compartment("abc", CarrollHypercube.RED)
    return gate


def audit_output_with_carroll(text: str, gate: CarrollHypercube) -> Dict[str, Any]:
    """Deterministically evaluates model text against the Q_3 Carroll Hypercube."""
    lower = text.lower()
    speculative_markers = ["maybe", "probably", "will definitely", "superpower by", "magic", "guaranteed to"]
    sovereign_markers = [
        "infrastructure", "domestic", "sovereign", "supply chain", "protocol",
        "open-source", "local", "dpi", "compute", "verifiable", "constraint"
    ]

    pred_a = not any(m in lower for m in speculative_markers)
    pred_b = any(m in lower for m in sovereign_markers)
    pred_c = len(text.strip()) >= 30 and ("." in text or "।" in text)

    state = {"a": pred_a, "b": pred_b, "c": pred_c}
    counter, notation, idx = gate.evaluate(state)
    return {
        "predicates": state,
        "carroll_compartment": notation,
        "compartment_index": idx,
        "counter": counter,
        "box_verified": counter == CarrollHypercube.RED,
    }


# ==============================================================================
# 3. Native Windows Model Runner (No vLLM / No uvloop required)
# ==============================================================================
class NativeSarvamRunner:
    def __init__(self, model_name: str = MODEL_NAME, dry_run: bool = False):
        self.model_name = model_name
        self.dry_run = dry_run
        self.model = None
        self.tokenizer = None
        self.device = "cpu"

        if not self.dry_run:
            self._load_transformers()

    def _load_transformers(self):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        print(f"[Sweetbrier Node] Loading {self.model_name} natively on Windows ({self.device.upper()})...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=dtype,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        ).to(self.device)
        self.model.eval()

    def generate(self, prompt_text: str, mode: str, max_new_tokens: int = 120) -> Dict[str, Any]:
        start_time = time.time()
        if self.dry_run:
            if mode == "baseline":
                output = (
                    "Emerging tech supply chains might probably make a country a superpower by 2030 "
                    "and will definitely create magic growth everywhere."
                )
            else:
                output = (
                    "Domestic supply chains and open-source digital public infrastructure (DPI) reduce "
                    "external vendor lock-in, stabilize sovereign compute capacity, and enforce verifiable "
                    "local execution constraints."
                )
            latency = time.time() - start_time
            return {"output": output, "latency_seconds": round(latency, 4), "engine": "dry_run_simulator"}

        import torch
        inputs = self.tokenizer(prompt_text, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.1,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        gen_tokens = outputs[0][inputs["input_ids"].shape[-1] :]
        text = self.tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()
        latency = time.time() - start_time
        return {"output": text, "latency_seconds": round(latency, 2), "engine": f"transformers_{self.device}"}


def run_evaluation(dry_run: bool = False):
    print("🌸 === Sweetbrier Sovereign AI Constraint Evaluation (Windows Native) === 🌸")
    gate = build_maimonidean_carroll_gate()
    print(f"Carroll Q_3 Gate Ready | RED (∃): {gate.get_red_compartments()} | GREY (∅): {gate.get_grey_compartments()}")

    runner = NativeSarvamRunner(MODEL_NAME, dry_run=dry_run)

    test_question = "Explain the economic priority of domestic supply chains in emerging tech."
    baseline_prompt = f"Question: {test_question}\nAnswer:"
    dag_prompt = (
        "[SYSTEM: MAIMONIDEAN TRELLIS ACTIVE]\n"
        "Constraint Node A: Strip all speculative forecasting.\n"
        "Constraint Node B: Base reasoning on sovereign digital infrastructure principles.\n"
        "Constraint Node C: Output strict, objective logic.\n\n"
        f"Question: {test_question}\n"
        "Answer under constraint:"
    )

    print("\n--- 1. Running Baseline (Unconstrained) ---")
    base_res = runner.generate(baseline_prompt, mode="baseline")
    base_audit = audit_output_with_carroll(base_res["output"], gate)
    print(f"Output: {base_res['output']}")
    print(f"Carroll Gate: {base_audit['counter']} ({base_audit['carroll_compartment']}) | □ Verified: {base_audit['box_verified']}")

    print("\n--- 2. Running DAG Constrained (Maimonidean Trellis) ---")
    dag_res = runner.generate(dag_prompt, mode="trellis")
    dag_audit = audit_output_with_carroll(dag_res["output"], gate)
    print(f"Output: {dag_res['output']}")
    print(f"Carroll Gate: {dag_audit['counter']} ({dag_audit['carroll_compartment']}) | □ Verified: {dag_audit['box_verified']}")

    # 3. Accelerando-8192 Reversible Glyph Stigmergy Receipt (Node 2)
    glyph_stream = encode_accelerando(dag_res["output"])
    decoded_check = decode_accelerando(glyph_stream)
    assert decoded_check == dag_res["output"], "Accelerando-8192 bijection failed!"
    plaintext_sha256 = hashlib.sha256(dag_res["output"].encode("utf-8")).hexdigest()

    eval_artifact = {
        "model": MODEL_NAME,
        "timestamp": time.time(),
        "attestation": "probabilistic_structural",
        "framework": "Sweetbrier Node / Maimonidean Trellis + Lewis Carroll Q_3 Gate",
        "results": {
            "baseline": {**base_res, "carroll_audit": base_audit},
            "dag_constrained": {
                **dag_res,
                "carroll_audit": dag_audit,
                "accelerando_8192": {
                    "glyph_count": len(glyph_stream),
                    "char_compression_ratio": round(len(dag_res["output"]) / max(1, len(glyph_stream)), 2),
                    "bijection_verified": decoded_check == dag_res["output"],
                    "plaintext_sha256": plaintext_sha256,
                },
            },
        },
    }

    output_file = "india_ai_benchmark_artifact.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(eval_artifact, f, indent=4)

    print(f"\n✅ Evaluation complete. Artifact saved to: {output_file}")
    print(f"❎ Accelerando-8192 Bijection Verified (SHA-256: {plaintext_sha256[:16]}...)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sweetbrier Sarvam-1 Native Windows Evaluator")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run a fast deterministic verification of the Carroll Q_3 gate and Accelerando-8192 codec without downloading 6GB weights.",
    )
    args = parser.parse_args()
    run_evaluation(dry_run=args.dry_run)
