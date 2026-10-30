# From Dataset to Model

Slide deck for the Claude Code meetup talk *From Dataset to Model: ML Development
with Coding Agents*. Twenty slides, one HTML file, no build step.

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

Placeholders to fill in before the talk: `[repo link]` and `[your handle]` on the
closing slide.

To push a local edit to the published copy, ask Claude Code to republish
`index.html` to the artifact URL; the publish strips the wrapper outside the
`artifact:start` / `artifact:end` markers.

## Assets

`assets/` holds real screenshots from the sibling `overlay` project (synthetic
contact sheet, ABO review sheet, labeling tool, evaluator error image) and the
generator's fonts, Anton and Lato (SIL Open Font License, licenses included).
Fonts load from Google Fonts first and fall back to the local files when offline.

`prod-*.webp` are product photos generated with Gemini (`gemini-3-pro-image-preview`),
color-matched to the `#faf7ef` panel and feathered at the edges. The SVG overlays and boxes
sit on top of them. `false_negative.jpg` (slide 15) is a re-render of the evaluator's
error image built from `prod-shoe` with the same composited watermark.

The ABO review sheet shows images from Amazon Berkeley Objects (CC BY 4.0,
images credited to Amazon.com).
