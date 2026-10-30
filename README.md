# From Dataset to Model

Slide deck for the Claude Code meetup talk *From Dataset to Model: ML Development
with Coding Agents*. Twenty-one slides, one HTML file, no build step.

## Present

Open `index.html` in Chrome, Safari or Firefox. Press `F` for fullscreen.

| Key | Action |
| --- | --- |
| `→` `Space` `Enter` | next build, then next slide |
| `←` `Backspace` | previous build or slide |
| `Home` / `End` | first / last slide |
| `N` | toggle the speaker-notes panel (remembered between loads) |
| `F` | fullscreen |
| `?` | key help |

Click or tap the right 80 % of the screen to advance, the left 20 % to go back.
Swipe works on touch screens. The URL hash (`#slide-7`) tracks the current slide,
so you can link straight to one.

## Edit

Everything lives in `index.html`:

- `:root` at the top of `<style>` holds the palette and type tokens.
- Each `<section class="slide">` is one slide. Elements with `data-step="n"`
  reveal on the n-th keypress. `.drop`, `.pop` and `.bbox` add entrance animations.
- Speaker notes are the `<aside class="notes">` at the end of each section.
- `data-phase="explore|label|model|eval|improve"` on a section adds the
  pipeline breadcrumb in the header.

Placeholder to fill in before the talk: `[your handle]` on the closing slide.

### Editing the published copy

The deck is published as a Claude artifact:
<https://claude.ai/artifact/NVxFLenKPvNe4YMEssQJtv>. There, anyone with edit
access can press `E` (or the Edit button, bottom left) to edit slide text and
speaker notes in place. Edited blocks get an orange outline; Save publishes a
new version of the artifact. Enter is blocked inside a block; Shift+Enter adds
a line break. SVG labels, layout and builds are not editable there.

To bring those edits back into the repo, read the artifact's HTML to a file and run:

```sh
python3 -I tools/sync_from_artifact.py artifact.html index.html
```

It patches only the text blocks that changed and leaves the rest of
`index.html` untouched. If the slide structure differs between the two files,
it stops instead of guessing. The rule for what counts as an editable block
lives both in the `deck-capture` script and in the sync script; change both
together.

To push a local edit to the published copy, republish the part of
`index.html` between the `artifact:start` / `artifact:end` markers to the same
artifact URL, with `assets/` alongside.

## Assets

`assets/` holds real screenshots from the sibling `overlay` project (synthetic
contact sheet, ABO review sheet, labeling tool, evaluator error image) and the
generator's fonts, Anton and Lato (SIL Open Font License, licenses included).
Fonts load from Google Fonts first and fall back to the local files when offline.

`prod-*.webp` are product photos generated with Gemini (`gemini-3-pro-image-preview`),
color-matched to the `#faf7ef` panel and feathered at the edges. The SVG overlays and boxes
sit on top of them. `prod-oats`, `prod-kettle` and `prod-tshirt` were added later the same
way to complete the product set. `synthetic_contact_sheet.jpg` (slide 7) is a re-render: the
`overlay` project's real generator (`scripts/generate_synthetic.py`, default config, seed 42,
100 samples) run over the eight `prod-*` photos in place of the original illustrated fixtures.
`labeling_ui.png` (slide 8) is a fresh screenshot of the real labeling tool on an artificial
fixture: sample 0000074 from that run (the kettle) with its three generated boxes loaded as a draft.
`false_negative.jpg` (slide 15) is a re-render of the evaluator's
error image built from `prod-shoe` with the same composited watermark.

The ABO review sheet shows images from Amazon Berkeley Objects (CC BY 4.0,
images credited to Amazon.com).
