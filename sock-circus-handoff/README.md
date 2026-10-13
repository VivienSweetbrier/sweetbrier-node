# Sock / Dash — face-and-hair construction study 01

## Current scope

The user chose a face-and-hair study first, at **64×64**, within **16 palette entries**, and approved this first study's likeness as recognizably Sock. Body, wings, soldering iron and animation are deliberately deferred. This remains a drawing study, not a final character asset or a replacement for the existing spritesheet.

## Start here

- `output/study-board.png`: annotated reference, silhouette, flat shapes and enlarged draft.
- `output/sock_head_64.png`: native RGBA sprite, transparent background.
- `output/sock_head_8x.png`: exact nearest-neighbour enlargement; no added detail.
- `head_model.json`: editable construction geometry and palette.
- `output/construction.json`: source hashes and landmarks in source pixels, normalized draft-frame coordinates and native sprite pixels.

## How the data was obtained

- Primary reference: `SOPHYBOT.jpg` (seated). The artist/assistant manually approximated the silhouette, locks, face planes, eye boxes, facial seams, nose and closed smile from a coordinate-grid overlay.
- Secondary reference: `DASH DISCOVERS 42.jpg` (standing). Visually cross-checked for identity cues; its geometry was NOT automatically fused with the primary reference.
- All geometry is approximate manual annotation, not machine-detected or exact segmentation. Coordinates in `head_model.json` use the documented crop origin within the original primary image.
- Hair colours are channel medians of measured source pixels grouped into brightness bands in a hair-only region. Face/nose colours use small regional medians. Transparency and pure black are explicit palette entries.
- Named polygons/lines are snapped and drawn directly on the 64-pixel grid. The source image is not simply downsampled into the sprite.
- An inspected first raster merged the viewer-right eye into its fringe. The draft fringe was shortened and that eye's glint inset as deliberate optical corrections. The automated eye-separation check guards this specific fault; it does not certify artistic likeness.
- `output/head-grid.txt` is an ASCII EXPORT of the finished raster, not the drawing source. Its alphabet is `.Kabcdefghij`, in the same order as `head_model.json`'s palette object.

## Rebuild

Requires Python and Pillow. The original images remain at the paths in `head_model.json`; change `primary_source` and `secondary_source` there if rebuilding elsewhere. The reference images are not bundled in the ZIP, but the annotated reference crop is included in the output.

```bash
python build_study.py
python -B test_study.py
```

The default output directory is `output/`. `--out <directory>` chooses a different output directory. No existing application source or old spritesheet is touched.

## Verification

Four test cases pass: native dimensions/palette/transparency, exact integer nearest-neighbour preview, source/landmark provenance and readable PNG review artifacts, and an ivory separation pixel between each button eye and the fringe. Real RED/GREEN command outputs are retained in `test-*.json` in the working folder.

The current sprite uses **12 entries including transparency**, below the 16-entry limit. The PNG is RGBA; this is a palette-budget constraint, not a claim of a hardware 4bpp binary format.

## Next approval gate

The user selected **native 128×128 as the working test draft**, while preserving 64×64 as an alternate. The selected asset is `comparison-64-128/sock_head_128.png`; `CURRENT_DRAFT.json` records both asset paths and hashes. See `COMPARISON.md` for the comparison. The user then requested face animation: `EXPRESSIONS.md` and `expressions-128-soft-v2/` contain the user-approved smaller, softer talking-mouth revision. The first expression pass remains in `expressions-128/`. See `CHARACTER_AND_LEAF.md` for Sock’s outward-interface role, deep-voice direction, and this leaf’s chosen name, Mallow. Body and voice integration remain deferred. Keep revisions in named geometry or explicitly documented native-pixel adjustments, not untraceable changes to a giant ASCII array.
