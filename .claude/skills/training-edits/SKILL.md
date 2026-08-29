---
name: training-edits
description: Editorial judgment for cutting long-form cohort/training session recordings (2h+ live coding classes) down to a publishable tutorial. Use when editing a multi-hour screen+facecam recording of a live class, workshop, or cohort session — deciding what to cut, when to drop the screen for full camera, where the facecam inset sits, how to treat audience questions, and how to end. Complements the mechanical pipeline notes in the project's edit/project.md.
---

# Training-session edits

Derived from the Agentic AI Development cohort, Day 3: a 2h12m live class cut
to 1h22m. Two synced angles — screen recording and facecam — from one
ScreenFlow capture.

This is the **editorial** layer: what to cut and why, and what the picture
should be doing. The ffmpeg/EDL mechanics live in each project's
`edit/project.md`.

## The shape of the edit

A live class is not a tutorial. It contains three things:

1. **Teaching** — the reason the video exists. Keep almost all of it.
2. **Waiting** — agent runs, builds, installs. Compress, don't cut: the
   audience needs to see that the agent takes time.
3. **Live-only material** — chat logistics, "we have 13 minutes", "show a
   thumbs up if you can hear me", decision-by-committee about what to build.
   Cut it entirely. It is meaningless to a recorded viewer and actively
   signals "you weren't there."

Roughly 40% of a live session is categories 2 and 3.

### What always gets cut

- **Deciding what to build.** Ten minutes of "maybe a license manager, maybe
  a booking app" is dead weight. Cut from where the deliberation starts to
  where the decision is stated. The viewer wants the build, not the vote.
- **Audience-logistics beats.** Thumbs-up checks, time-remaining announcements,
  "can you all see my screen", "copy this and paste it in the chat."
- **Failed searches and fumbles.** "Have I starred it? … no, I can't find it."
  Keep the question that prompted it, cut the flailing.
- **Whole tangential tool demos** that aren't the subject. A five-minute detour
  into an unrelated CLI is a clean, invisible cut if you take it from its
  hand-off line ("By the way, there is this…") to where the main thread
  resumes.
- **Repeated goodbyes.** Live sessions trail off — end on the first real one.

### What to keep that looks cuttable

- **Halting bridges and "let me show you with an example."** These read as
  authentic. Only obvious retake blocks are free cuts.
- **Agent-working time**, compressed. Cutting it to zero misrepresents the
  workflow. Speed-ramp it so the wait is visible but not felt.

### Cut boundaries

- **Land on sentence starts, never mid-sentence.** The single most common
  defect. A cut whose OUT point is 3 seconds late drops the viewer into
  "…thing, whatever has this booking" instead of "I wanted to build
  basically." Always resolve the OUT point to the first word of the resuming
  sentence.
- **Anchor every cut to a transcript phrase, not a timestamp**, and record the
  phrase alongside the cut. Timestamps shift as earlier cuts land; the phrase
  doesn't.
- **A cut can subsume an earlier one.** When a new, larger cut swallows an old
  one, merge them into a single entry rather than leaving overlapping pairs.

## Camera vs screen

Default is **screen with a facecam inset**. Drop to **full camera** when the
speaker stops driving the screen and starts talking to the audience:

- **Answering a question.** The single most reliable trigger. When they read
  out a question and answer it, the screen is irrelevant — go full camera for
  the whole answer, back on the closing beat.
- **Making a point about method** rather than demonstrating it. "This is a very
  important piece — if you want to do agentic development long-term…" is a
  full-camera beat even though a screen is present.
- **Cold open.** Start on camera, cut to screen on the first line that
  references what's on it. It establishes a person before it establishes a
  tool.
- **The sign-off.**
- **Right after a big cut.** Resuming on full camera hides the seam — the
  viewer reads it as a deliberate scene change rather than a splice.

Full-camera beats run **10s to 100s**. Under ~8s they read as a glitch.

**Transitions are hard cuts.** No dissolve, no scale-up. Hard cuts between
layouts read as deliberate; anything softer reads as a mistake.

**Keep the screen underneath even when it's invisible.** Compose the camera
*over* the screen rather than switching sources. Both angles then share one
timeline and can never drift apart — see the sync section below.

## The facecam inset

- **Crop tight and portrait-ish**, not the full 16:9 frame. Frame from the
  head to the hands with minimal air left and right. A crop that reaches
  head-to-hands is necessarily near-square (~0.85–1.0 aspect) — 16:9 tall
  enough to include hands is barely a crop at all.
- **Find the crop from the gestures, not the face.** Sample the frame where
  they gesture widest; that hand position is the constraint. A crop that looks
  perfect on a still will clip a raised hand ten seconds later.
- **Small and tight to the corner.** ~20% of frame width, margin ~16px at 720p.
- **Move it, don't let it sit on content.** When the speaker's content lands
  under the inset, move the inset — top-right to bottom-right and back.
- **Move early.** Place the move a beat *before* the content it would cover
  appears, not as it appears.
- **Ease the move over ~0.5s**, smoothstep. Instant jumps read as a glitch;
  anything over ~0.8s draws attention to itself.
- **Mirror the camera if the speaker faces away from their own content.** If
  they look screen-right but the screen is to their left, `hflip` fixes the
  eyeline. Check for on-camera text first.

## Question cards

When the speaker answers an audience question the viewer never saw, put the
question on screen.

- **Only for questions that shape the answer.** Not every "yes, that works."
- **Lower-third, centered, clear of the inset.** Semi-transparent dark panel,
  brand accent on the `Q`, product design tokens — it should look like the
  product being taught, not like a broadcast chyron.
- **Rise from the bottom, hold for the whole answer, drop out.** In on a
  damped spring (ζ≈0.65 — physical overshoot, ~5–10%), out faster on an ease-in.
  Avoid `elastic`/`back` eases; they read as cartoon.
- **Pair it with the full-camera beat.** Question card + full camera is the
  house treatment for Q&A.

## Endings

- **End on the first real goodbye.** Cut everything after.
- **Dip to black over 1.5–2s**, starting the instant the last content word
  finishes. Longer fades were requested and then felt too slow — the fade
  should start *after* the sentence lands, not swallow it.
- **Fade the picture only.** Let the audio play out clean and stop at the cut.
  Dimming the sound with the picture feels like a broadcast fault.
- **Hold ~1s of room tone** past the last word before the cut. Silence is part
  of the ending.
- Watch for the tail landing on a **speed-ramped** silence — a compressed
  closing beat feels clipped. Restore real time on the final segment.

## Sync — non-negotiable

Two angles from one recording must stay locked for the whole video.

- **Verify frame-lock before anything else**: identical frame count and
  duration to the millisecond, and identical audio (MD5 the decoded PCM at
  head *and* tail). If they match, no alignment step is needed — don't build
  one.
- **Never render the two angles as separate tracks and composite afterwards.**
  It looks tidier and silently desyncs: `concat` pads each segment to its
  longest stream, so a video+audio track and a video-only track come out
  different lengths. This produced 4.4s of creeping lip-sync error — invisible
  for the first 20 minutes, obvious by the half-way mark.
- **Composite per segment, screen as the base layer.** `overlay` takes its
  length from the main input, so the screen dictates every frame count and
  drift becomes structurally impossible.
- After every render, check both streams report `start_time=0.000` and that
  video and audio durations agree to well under 100ms.

## Working method

- **Review marks arrive on the rendered timeline; the EDL is in source time.**
  Convert every mark to source before applying, then apply cuts in source
  space — otherwise each cut shifts every later mark.
- **Confirm each mark against the transcript before acting.** Marks are
  routinely a few seconds off what was meant, and the surrounding words tell
  you what was actually intended. Several in this session landed on the wrong
  sentence; one named a timestamp two minutes from the phrase it described.
- **Marks land in trimmed silence surprisingly often.** Fail loudly rather
  than silently dropping the edit.
- **Verify by sampling frames at every boundary and reading them.** Layout,
  inset position, crop edges — all visible in a still. Audio is not; the
  speaker has to audition it.
- **Keep all editorial decisions in one hand-editable file** with the anchor
  phrase beside each. Re-cuts then cost minutes, not a re-derivation.
- **Cache renders per batch**, but remember the cache keys on filename, not
  content — wipe it whenever the sources change.
