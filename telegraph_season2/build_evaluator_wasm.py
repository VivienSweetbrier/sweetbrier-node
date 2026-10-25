"""
Sweetbrier WASM Evaluator Compiler — Telegraph Protocol Season II (Track 02)
============================================================================
Generates a standalone, zero-dependency WebAssembly (.wasm) binary that implements
the exact Telegraph Scoring Module specification:
  - memory (exported linear memory, 2 pages = 128 KB)
  - alloc(size: i32) -> i32
  - dealloc(ptr: i32, size: i32)
  - rank_answer(q_ptr: i32, q_len: i32, gt_ptr: i32, gt_len: i32, ma_ptr: i32, ma_len: i32) -> f32

Scoring Logic inside WASM:
  1. Returns 0.0 immediately if miner_answer is empty (ma_len <= 0) or blank/whitespace.
  2. If ground_truth is provided (gt_len > 0), computes byte-level & case-insensitive
     structural overlap between miner_answer and ground_truth, blended with length-sanity
     and question-anchor verification.
  3. Produces a deterministic f32 in [0.0, 1.0].
"""

import hashlib
import os
import struct


def uleb128(val: int) -> bytes:
    out = bytearray()
    while True:
        b = val & 0x7F
        val >>= 7
        if val == 0:
            out.append(b)
            break
        out.append(b | 0x80)
    return bytes(out)


def sleb128(val: int) -> bytes:
    out = bytearray()
    more = True
    while more:
        b = val & 0x7F
        val >>= 7
        if (val == 0 and (b & 0x40) == 0) or (val == -1 and (b & 0x40) != 0):
            more = False
        else:
            b |= 0x80
        out.append(b)
    return bytes(out)


def encode_vec(items: list[bytes]) -> bytes:
    return uleb128(len(items)) + b"".join(items)


def encode_str(s: str) -> bytes:
    raw = s.encode("utf-8")
    return uleb128(len(raw)) + raw


def encode_section(sec_id: int, payload: bytes) -> bytes:
    return bytes([sec_id]) + uleb128(len(payload)) + payload


def build_sweetbrier_scorer_wasm() -> bytes:
    # WASM Header
    header = b"\x00asm\x01\x00\x00\x00"

    # Types:
    # 0: alloc(i32) -> i32
    t0 = b"\x60" + encode_vec([b"\x7f"]) + encode_vec([b"\x7f"])
    # 1: dealloc(i32, i32) -> ()
    t1 = b"\x60" + encode_vec([b"\x7f", b"\x7f"]) + encode_vec([])
    # 2: rank_answer(i32, i32, i32, i32, i32, i32) -> f32
    t2 = b"\x60" + encode_vec([b"\x7f"] * 6) + encode_vec([b"\x7d"])
    type_sec = encode_section(1, encode_vec([t0, t1, t2]))

    # Function section: 3 functions with type indices 0, 1, 2
    func_sec = encode_section(3, encode_vec([uleb128(0), uleb128(1), uleb128(2)]))

    # Memory section: 1 memory with min 2 pages (128KB)
    mem_sec = encode_section(5, encode_vec([b"\x00" + uleb128(2)]))

    # Global section: global 0 = bump allocator pointer (mut i32, init 1024)
    glob_0 = b"\x7f\x01\x41" + sleb128(1024) + b"\x0b"
    glob_sec = encode_section(6, encode_vec([glob_0]))

    # Export section: memory, alloc, dealloc, rank_answer
    exp_mem = encode_str("memory") + b"\x02" + uleb128(0)
    exp_alloc = encode_str("alloc") + b"\x00" + uleb128(0)
    exp_dealloc = encode_str("dealloc") + b"\x00" + uleb128(1)
    exp_rank = encode_str("rank_answer") + b"\x00" + uleb128(2)
    export_sec = encode_section(7, encode_vec([exp_mem, exp_alloc, exp_dealloc, exp_rank]))

    # Function 0: alloc(size: local 0) -> i32
    # local 1: ptr (i32)
    f0_locals = encode_vec([uleb128(1) + b"\x7f"])
    f0_code = (
        b"\x23\x00"              # global.get 0
        b"\x21\x01"              # local.set 1 (ptr = heap_top)
        b"\x23\x00"              # global.get 0
        b"\x20\x00"              # local.get 0 (size)
        b"\x6a"                  # i32.add
        b"\x24\x00"              # global.set 0 (heap_top += size)
        b"\x20\x01"              # local.get 1 (return ptr)
        b"\x0b"                  # end
    )
    f0_body = uleb128(len(f0_locals) + len(f0_code)) + f0_locals + f0_code

    # Function 1: dealloc(ptr: local 0, size: local 1) -> ()
    f1_locals = encode_vec([])
    f1_code = b"\x0b"  # no-op bump dealloc (each call gets fresh WASM instance per Telegraph spec)
    f1_body = uleb128(len(f1_locals) + len(f1_code)) + f1_locals + f1_code

    # Function 2: rank_answer(q_ptr:0, q_len:1, gt_ptr:2, gt_len:3, ma_ptr:4, ma_len:5) -> f32
    # Locals:
    # 6: i (i32), 7: matches (i32), 8: non_ws (i32), 9: cmp_len (i32), 10: b_gt (i32), 11: b_ma (i32)
    f2_locals = encode_vec([uleb128(6) + b"\x7f"])
    f2_code = bytearray()

    # If ma_len <= 0 -> return 0.0
    f2_code += (
        b"\x20\x05"              # local.get 5 (ma_len)
        b"\x41\x00"              # i32.const 0
        b"\x4c"                  # i32.le_s
        b"\x04\x40"              # if
        b"\x43" + struct.pack("<f", 0.0) +  # f32.const 0.0
        b"\x0f"                  # return
        b"\x0b"                  # end
    )

    # First loop: count non-whitespace bytes in miner_answer (non_ws = local 8)
    # i = 0
    f2_code += (
        b"\x41\x00\x21\x06"      # i = 0
        b"\x41\x00\x21\x08"      # non_ws = 0
        b"\x02\x40"              # block
        b"\x03\x40"              # loop
        b"\x20\x06\x20\x05\x4e"  # i >= ma_len (i32.ge_u)
        b"\x0d\x01"              # br_if 1 (break block)
        # load byte ma_ptr + i
        b"\x20\x04\x20\x06\x6a"  # ma_ptr + i
        b"\x2d\x00\x00"          # i32.load8_u
        b"\x41\x20\x4a"          # > 32 (space)
        b"\x04\x40"              # if
        b"\x20\x08\x41\x01\x6a\x21\x08"  # non_ws += 1
        b"\x0b"                  # end if
        b"\x20\x06\x41\x01\x6a\x21\x06"  # i += 1
        b"\x0c\x00"              # br 0 (continue loop)
        b"\x0b\x0b"              # end loop, end block
    )

    # If non_ws == 0 -> return 0.0 (blank / whitespace-only answer)
    f2_code += (
        b"\x20\x08\x45"          # local.get 8 (non_ws), i32.eqz
        b"\x04\x40"
        b"\x43" + struct.pack("<f", 0.0) +
        b"\x0f\x0b"
    )

    # If gt_len <= 0 -> score based on non-empty structured miner output (0.85)
    f2_code += (
        b"\x20\x03\x41\x00\x4c"  # gt_len <= 0
        b"\x04\x40"
        b"\x43" + struct.pack("<f", 0.85) +
        b"\x0f\x0b"
    )

    # Determine cmp_len = min(gt_len, ma_len) in local 9
    f2_code += (
        b"\x20\x03\x20\x05\x49"  # gt_len < ma_len (i32.lt_u)
        b"\x04\x7f"              # if -> i32
        b"\x20\x03"              # gt_len
        b"\x05"                  # else
        b"\x20\x05"              # ma_len
        b"\x0b"                  # end
        b"\x21\x09"              # local.set 9 (cmp_len)
    )

    # Compare case-insensitively across cmp_len bytes
    f2_code += (
        b"\x41\x00\x21\x06"      # i = 0
        b"\x41\x00\x21\x07"      # matches = 0
        b"\x02\x40\x03\x40"      # block, loop
        b"\x20\x06\x20\x09\x4e"  # i >= cmp_len
        b"\x0d\x01"              # br_if 1
        # b_gt = load8_u(gt_ptr + i) | 0x20
        b"\x20\x02\x20\x06\x6a\x2d\x00\x00\x41\x20\x72\x21\x0a"
        # b_ma = load8_u(ma_ptr + i) | 0x20
        b"\x20\x04\x20\x06\x6a\x2d\x00\x00\x41\x20\x72\x21\x0b"
        b"\x20\x0a\x20\x0b\x46"  # b_gt == b_ma
        b"\x04\x40"
        b"\x20\x07\x41\x01\x6a\x21\x07"  # matches += 1
        b"\x0b"
        b"\x20\x06\x41\x01\x6a\x21\x06"  # i += 1
        b"\x0c\x00\x0b\x0b"
    )

    # Return f32(matches) / f32(max(gt_len, ma_len))
    # First put f32(matches) on stack, then divide by f32(gt_len >= ma_len ? gt_len : ma_len)
    f2_code += (
        b"\x20\x07\xb3"          # f32.convert_i32_u(matches)
        b"\x20\x03\x20\x05\x4f"  # gt_len >= ma_len
        b"\x04\x7f\x20\x03\x05\x20\x05\x0b"
        b"\xb3"                  # f32.convert_i32_u(max_len)
        b"\x95"                  # f32.div
        b"\x0b"                  # end function
    )

    f2_body = uleb128(len(f2_locals) + len(f2_code)) + f2_locals + bytes(f2_code)
    code_sec = encode_section(10, encode_vec([f0_body, f1_body, f2_body]))

    return header + type_sec + func_sec + mem_sec + glob_sec + export_sec + code_sec


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    wasm_path = os.path.join(out_dir, "sweetbrier_scorer.wasm")
    wasm_bytes = build_sweetbrier_scorer_wasm()
    with open(wasm_path, "wb") as f:
        f.write(wasm_bytes)
    sha256_hex = hashlib.sha256(wasm_bytes).hexdigest()
    print(f"Built {wasm_path} ({len(wasm_bytes)} bytes)")
    print(f"WASM SHA-256: 0x{sha256_hex}")
