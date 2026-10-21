# Sock / expression lab — softer talking revision

## Revision 2

The user requested smaller, softer talking shapes, with the character contrast of a tiny presence and an exceptionally deep roboticized voice. Only the three talking mouths changed: smaller curved apertures, no tongue accent, and a tiny round mouth. Neutral, both blink states and the stitched glitch remain pixel-identical to the first pass. Timings are unchanged.

The first pass remains in `expressions-128/`; its geometry is retained in `expression_model_128_v1.json`. The current geometry is `expression_model_128.json`, and the renderer now defaults to `expressions-128-soft-v2/` so rebuilding does not overwrite the first pass. No voice was generated and no voice settings were changed. See `CHARACTER_AND_LEAF.md` for the character and naming context.

## Scope and approval

The user selected the native 128×128 head and requested that her face be brought to life. This study adds blinking, silent talking-mouth shapes and a stitched-eye glitch. The neutral head remains the approved baseline; the user has also approved the smaller, softer expression revision and its current timing. No body, voice, live microphone input, lip sync, global jitter or screen flashes are included.

## Open these

- `expressions-128-soft-v2/sock_alive_preview.gif`: enlarged loop on a neutral checkerboard, suitable for judging the black hair.
- `expressions-128-soft-v2/sock_alive_128.gif`: native 128×128 transparent animated GIF.
- `expressions-128-soft-v2/expression-sheet.png`: labelled review sheet for the seven unique states.
- `expressions-128-soft-v2/sock_expressions_128.png`: native horizontal spritesheet. See `expressions.json` for cell rectangles and order.
- `expressions-128-soft-v2/*.png`: individual states plus an explicit movement-mask diagnostic.

## The seven states

Neutral; half blink; closed blink; small talking mouth; open talking mouth; round talking mouth; stitched glitch. The demonstration timeline uses these states more than once. Its exact order and durations are in `expression_model_128.json` and the output manifest.

The talking sequence is a visual animation test, NOT synchronized to the linked song, speech or microphone. The user's Oingo Boingo / Weird Science link was a mood reference; no song audio or video footage is bundled.

## How identity is kept stable

- The neutral frame matches the approved PNG exactly.
- Reuse the original face underpainting, restoring seams and stitch marks before compositing changed features. Do not erase features with a flat skin-colour rectangle.
- Draw eyelids and mouths at native resolution and composite only through explicit eye/mouth masks.
- Protect the nose and foreground fringe, even where those overlap a patch rectangle.
- Keep the head position, hair, nose, outline and transparency identical across every state.
- Keep native sprites within the approved palette. The checkerboard GIF adds two display-only background colours, which are not part of the sprite.
- Encode GIFs with an explicit palette-index mapping so transparent black and opaque hair black remain distinct. Decode every frame to verify transparency, disposal and timing, rather than assuming an encoder's success means the loop is correct.

## Rebuild

Python plus Pillow. The original JPG references are not needed for this animation path.

```bash
python animate_sock.py
python -B test_expressions.py
```

Edit `expression_model_128.json` for native mouth geometry and timings. The animation script uses the saved native-128 construction and baseline under `comparison-64-128/`; it does not overwrite them. `--out <directory>` selects a different animation output folder.

## Verification

Automated checks cover: seven distinct states; neutral fidelity; palette/alpha invariance; no changes outside the allowed motion mask; exact decoded native and enlarged GIF pixels; per-frame duration and loop metadata; spritesheet-to-individual-frame identity; and preservation of the approved baseline hash. The rendered expression review sheet was also visually inspected.

## Next question

Judge her expression and timing before connecting voice or adding a body. The important artistic choices are how wide her talking grin should be and whether the stitched glitch has the right amount of mischief.
