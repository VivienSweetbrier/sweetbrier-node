# Sock / Dash — native 64 vs 128 comparison

## Approval boundary

The user approved the first 64×64 likeness, then selected the native **128×128** version as the working test draft after comparison. Retain 64×64 as a smaller, chunkier alternate. Body framing, animation and expression work are not yet selected. `CURRENT_DRAFT.json` records the current choice; earlier generation manifests and ZIPs remain historical snapshots.

## View

Open `comparison-64-128/comparison.png`.

- Left: the exact approved 64×64 PNG, displayed at 8×.
- Right: the saved source-space geometry rasterized directly onto 128×128, displayed at 4×.
- Both display panels are 512×512, with the same neutral checkerboard.
- Same construction, expression, sampled palette and 16-entry budget. Both use 12 RGBA entries including transparency.
- The native 128 sprite is NOT an enlargement, filtered upscale or downsample of a generated reference image. No antialiasing is applied to either sprite.
- Thin seams, mouth line and glints remain native-grid details rather than being doubled bitmap blocks. This comparison does not claim a completed pixel-by-pixel polishing pass.

## Files

- `comparison-64-128/sock_head_64.png`: byte-identical copy of the approved original.
- `comparison-64-128/sock_head_128.png`: transparent native 128×128 sprite.
- `comparison-64-128/sock_head_64_display.png` and `sock_head_128_display.png`: exact nearest-neighbour display previews.
- `comparison-64-128/comparison.json`: panel locations, palette counts, baseline hash and pixel difference from a simple enlargement.
- `comparison-64-128/head_model_128.json`: derived construction snapshot for this render.
- `compare_resolutions.py`: reproducible comparison generator, using the pure renderer from `build_study.py` and geometry from `head_model.json`.

## Rebuild and test

Requires Python and Pillow. From this folder:

```bash
python compare_resolutions.py
python -B test_comparison.py
```

The comparison path does not require the original reference JPGs: geometry and palette are already recorded. The older `build_study.py` CLI still requires those JPGs to regenerate its reference board, but importing its pure renderer does not read them.

`--out <directory>` changes the comparison output destination. The existing approved `output/sock_head_64.png`, original 64 study board and original ZIP are not replaced.

Tests verify native dimensions, binary alpha, palette membership/budget, non-equivalence to a bitmap enlargement, unchanged approved asset, exact nearest-neighbour previews and every opaque sprite pixel in both board panels. Artistic likeness remains a user judgment.
