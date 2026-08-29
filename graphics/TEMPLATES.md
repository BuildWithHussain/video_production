# Reusable compositions

Compositions in `compositions/` that are meant to be re-run with new content,
rather than one-off graphics for a single video.

To work on one: copy it to `index.html` in a scratch project directory that also
has `theme/` (symlink is fine) and a `meta.json`, then run
`npx hyperframes check .` / `snapshot .` / `render .` there. The CLI operates on
a project directory, so it will not target a file inside `compositions/`
directly.

---

## `title-bouncing-ball.html` — typed title with a bouncing ball

Light title card: the headline types itself in while a blue ball bounces along
the top of the letters and exits right. Recreated from the "Chapter 1 —
Frappe/ERPNext course" intro, so it matches that series.

**Change the title and nothing else.** `CFG.text` drives everything downstream —
typing duration, the ball's horizontal speed, and how far the bounce surface
extends — so a longer or shorter headline re-times itself.

### Knobs (`CFG` at the top of the `<script>`)

| Key | Now | What it does |
| --- | --- | --- |
| `text` | "Cost of an ERP Failure" | the headline |
| `charFrames` | 3 | gap between letters (100ms) |
| `fadeFrames` | 7 | how long one letter takes to reach full opacity (233ms). Longer than `charFrames`, so 2-3 letters are always mid-fade and the trailing edge reads soft. Drop to 3 to match the source video exactly, which pops. |
| `crossRatio` | 1.377 | ball crosses the full frame in `typingFrames × crossRatio` |
| `gravity` / `launchVy` / `restitution` | 4.2 / 38 / 0.93 | the bounce, in px per frame |
| `ballR` | 13 | ball radius; the element's size and centering offset derive from it |
| `capLine` | 496 | y of the cap-height line — the ball rests **on** it, never sinks through |
| `floatOut` | false | when true the ball takes one soft hop past the end of the title and coasts out. Matches the source video, but the bounce rhythm dies and it reads as slowing down. |
| `blurPerV` | 0.13 | motion blur, scaled by speed. The ball itself never deforms. |

Colours are `:root` vars at the top of the `<style>`: `--card-bg`,
`--title-ink`, `--ball`. This card uses the source video's own light palette,
not the frappe-ui dark theme in `THEME.md`.

### How the ball works

matter.js runs the bounce (a circle on a static ground at the cap line) and the
result is baked to one position per frame **at load**. A single GSAP proxy tween
then reads that table, which keeps the timeline seekable and the render
deterministic — a live physics step would be neither.

The bake runs twice: pass 1 records where the ball actually lands so pass 2 knows
which contact is the last one still over the title. That only matters when
`floatOut` is on.

### Duration

`DUR` in the script must stay in sync with `data-duration` on both `#root` and
`#card`. At the current settings the ball leaves frame around 3.0s and the card
holds the finished title until 4.0s.
