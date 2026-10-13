# Sock / Dash — handoff to the circus

## Approved checkpoint

The user approved the native 128×128 face-and-hair draft and the smaller, softer talking-mouth revision: "that's perfect :3". Treat `expressions-128-soft-v2/` as the current expression set. Preserve the 64×64 alternate and the first expression pass. This is an approved face/expression study, not a finished body or VTuber system.

- Seven states: neutral, half blink, closed blink, small talk, open talk, round talk, stitched glitch.
- Twelve palette entries including transparency. Native PNGs are RGBA; this is not a hardware 4bpp encoding.
- Hair, head position, nose and transparency remain fixed. Talking has deliberately small movement.
- The demonstration GIF is silent and scripted, NOT speech- or microphone-driven lip sync.

## Assets and editable source

- `expressions-128-soft-v2/expressions.json`: exported state order, cell rectangles and animation metadata; inspect this rather than assuming frame positions.
- `expressions-128-soft-v2/sock_expressions_128.png`: native horizontal expression sheet.
- `expressions-128-soft-v2/sock_alive_128.gif`: native transparent demonstration loop.
- `expressions-128-soft-v2/sock_alive_preview.gif`: enlarged checkerboard review loop, not the transparent integration asset.
- `expressions-128-soft-v2/expression-sheet.png`: labelled review board.
- `expression_model_128.json`: current mouth/eye geometry and timeline.
- `animate_sock.py`: expression renderer/exporter.
- `comparison-64-128/`: approved native head and its construction data.
- `CURRENT_DRAFT.json`: current selection and approval status.
- `CHARACTER_AND_LEAF.md`: shared-interface concept, Mallow's leaf name and voice direction.

## Important integration warning

The original ASCII-pipeline brief assumed TWO 64×64 frames in an enlarged 512×256 sheet. This delivery uses SEVEN native 128×128 expression states. Do not merely overwrite the old PNG and assume its CSS/frame offsets still apply. Inspect the existing application and read the new manifest before adapting it. Keep the native pixels crisp with nearest-neighbour / pixelated display scaling.

The approved art already exists. Do not regenerate it as a giant ASCII matrix or redraw the face while integrating controls. Make any future visual edits in named construction geometry and submit them as a separate review checkpoint.

## Proposed next checkpoint — not yet selected by the user

A small controllable browser puppet using the existing approved assets:

- Idle/neutral with blinking.
- Explicit start/stop talking controls using the small mouth states.
- An intentional stitched-glitch control; no unsolicited flashing or whole-face jitter.
- Manual controls first. Microphone access, model connections, live speech synthesis and audio-driven lip sync are separate later decisions.

Suggested division of work, subject to the user's choice: the circus can adapt its existing UI; this character-drafting leaf can help audition the voice. Do not assume these tasks are already assigned or approved.

## Voice and body remain separate gates

User's voice direction: the tiniest presence with an unfathomably deep voice, referencing Circuit des Yeux but roboticized. No singer audio, synthesized voice or changed voice settings is bundled. First judge a short original spoken test before committing to speech integration.

If adding shoulders, wings or overalls later, preserve the approved head's readability. A taller canvas is preferable to automatically shrinking the whole character into the existing head-sized square.

## Rebuild and test

Python plus Pillow:

```bash
python animate_sock.py
python -B -m unittest discover -s . -p "test_*.py"
```

The animation rebuild uses bundled construction data and baseline assets; it does not need the original JPGs. Rebuilding the original reference-comparison boards does require the original image paths documented in `README.md`.
