---
name: image-html-ppt-report
description: Create PPT-style report materials using an image-plus-HTML workflow. Use when Codex needs to turn a report outline, numbered slide images, per-slide prompts, narration scripts, audio, PDFs, or generated assets into a reusable offline index.html presentation player, asset catalog, delivery package, or workflow for sharing meeting decks, project reports, training sessions, demos, and internal presentations.
---

# Image HTML PPT Report

## Goal

Produce PPT-style report materials with this core pattern:

```text
report outline -> per-page prompts -> slide images -> optional scripts/audio -> offline index.html player -> catalog/package
```

Treat each slide as a stable image asset and use `index.html` as the presentation runtime. This avoids dependence on PowerPoint layout compatibility while still producing materials that feel like a slide deck during a meeting or screen share.

## Use Cases

Use this skill for:

- Internal report decks built from generated or designed slide images.
- Sharing-session or training materials with narration.
- Project progress reports that need a lightweight local HTML playback entry.
- Demo decks that should be easy to package and send to colleagues.
- Summaries of an existing image-HTML deck into a reusable method or asset catalog.

If the user specifically asks for a `.pptx`, use the relevant presentation tooling. This skill is for the image + HTML workflow; it can still produce assets that may later be imported into PPT.

## Deliverable Model

Prefer one folder per report:

```text
report-folder/
├── index.html
├── report-assets.md
├── NN-topic.md
├── NN-topic.png
├── NN-topic-script.md
├── NN-topic-script-edge.mp3
├── report.pdf
└── generate_*.py
```

Required for a basic report:

- Numbered slide images: `NN-topic.png`.
- Offline playback page: `index.html`.

Optional but recommended:

- Page prompts: `NN-topic.md`.
- Speaker notes or narration scripts: `NN-topic-script.md`.
- Audio narration: `NN-topic-script-edge.mp3`.
- Asset catalog: `report-assets.md`.
- PDF export if the user needs an additional distribution format.

## Mode Selection

Choose one of three modes before starting. If the user does not specify a mode, infer it from the available inputs and state the mode being used.

### Mode 1: Guided Creation

Use when the user has only a topic, goal, or rough idea and wants to participate throughout the creation process.

Human confirmation points:

- Confirm topic, audience, purpose, style, page count, and delivery format.
- Draft the numbered page outline and wait for approval.
- Draft per-page prompts and wait for approval when quality matters.
- Generate or collect slide images, then ask for review or targeted revisions.
- Draft speaker scripts and ask for review if narration will be used.
- Generate audio only after scripts are acceptable.
- Generate `index.html` and package automatically after assets are approved.

### Mode 2: Outline-Approved Generation

Use when the user wants to confirm the outline, then let Codex complete the rest.

Human confirmation points:

- Confirm topic, audience, purpose, style, page count, and delivery format.
- Draft the numbered page outline and wait for approval.
- After outline approval, automatically create prompts, slide images, optional scripts/audio, asset catalog, and `index.html`.
- Report any uncertain content, failed generation, or assets needing human review at the end.

### Mode 3: Assemble Only

Use when the user already has the required slide images and optional audio/scripts.

Human confirmation points:

- Confirm the source folder if unclear.
- Scan assets, identify missing or inconsistent files, and ask only if the gaps block assembly.
- Generate `index.html` directly from `assets/index-template.html` with `scripts/build_index.py`.
- Create or update the asset catalog if requested.

## Workflow

1. Clarify the report purpose and audience.
   Identify whether the material is for a formal report, training, internal sharing, project demo, or reusable package. Choose a quiet report style unless the content clearly calls for a more expressive visual direction.

2. Define the page plan.
   Create a numbered outline. Each page needs a single job: title, context, problem, data, architecture, process, case, comparison, conclusion, or action.

3. Build image assets.
   Generate or collect one image per page. Keep the aspect ratio consistent, preferably 16:9. Use two-digit page numbers so ordering is stable.

4. Add scripts and audio when useful.
   Write one script per page when the report needs spoken explanation. Generate one audio file per page only when autoplay narration matters.
   Keep `NN-topic-script.md` as pure narration text. Everything in this file is sent to TTS, so do not include duration notes, tone guidance, headings, bullets, markdown annotations, or production comments.

5. Create or update `index.html`.
   Prefer the bundled `assets/index-template.html`. Use `scripts/build_index.py` to generate `index.html` from numbered assets, then adjust styling or labels only when the report needs it. Keep the final page dependency-free so it can be opened directly in a browser.

6. Create an asset catalog.
   Summarize file counts, page mapping, production workflow, naming rules, and reuse notes. If available, run `scripts/scan_session_assets.py` to speed up the inventory.

7. Validate the package.
   Check image loading, page order, navigation, fullscreen, thumbnails, audio playback, and missing assets.

8. Package for colleagues.
   Package the skill folder itself when sharing the skill. Package the report folder when sharing a finished deck. Keep generated decks and the skill separate unless the user asks for examples inside the package.

## HTML Player Requirements

Use a single static `index.html` with embedded CSS and JavaScript unless the existing project already has a stronger pattern. Start from `assets/index-template.html` for new decks.

Baseline structure:

- `main.stage`: full-window slide display surface.
- `img#slide`: current slide image with `object-fit: contain`.
- `audio#slideAudio`: reusable audio element when narration exists.
- `nav.controls`: compact presentation controls.
- `section#thumbPanel`: thumbnail overview.
- `const slides = [...]`: ordered image filenames.
- `const audios = [...]`: ordered audio filenames, same length as `slides` when enabled.
- `render()`: single refresh path for image, alt text, filename, counter, button states, and audio state.

Use `encodeURI(file)` before assigning Chinese filenames, spaces, or punctuation to `src`.

## Interaction Baseline

Include these controls unless the user asks for a simpler viewer:

- Previous / next.
- Page counter.
- Thumbnail overview.
- Fullscreen.
- Collapsible controls.
- Manual/autoplay mode when audio exists.
- Audio play/pause and progress when audio exists.

Recommended keys:

- `ArrowLeft`: previous page.
- `ArrowRight` or `Space`: next page.
- `F`: fullscreen.
- `O`: overview.
- `C`: collapse controls.
- `A`: toggle autoplay/manual mode.
- `P`: play/pause narration when autoplay is active.
- `Escape`: close overview when open.

## Design Rules

- Make the slide image the primary experience.
- Keep UI chrome compact and fixed to an edge.
- Use a neutral dark stage for bright slide images.
- Prevent document scrolling during presentation.
- Use fixed-width thumbnail cards that wrap automatically; the thumbnail panel should scroll vertically when there are many slides.
- Avoid decorative effects that cover report content.
- Use subtle transitions only if they do not reduce readability.

## Asset Catalog

When asked to summarize, document, or prepare the workflow for reuse, create a Markdown catalog with:

- Material positioning: what the report/player is for.
- Asset statistics by extension.
- Page catalog: page number, topic, image, prompt, script, audio.
- `index.html` module breakdown.
- Production workflow.
- Naming rules.
- Reuse checklist.
- Known issues and improvement suggestions.

## Bundled Resources

- `scripts/scan_session_assets.py`: scan a report/session folder and print extension counts plus page-level asset mapping.
- `scripts/build_index.py`: generate `index.html` from numbered slide images and optional per-page audio using the bundled template.
- `scripts/generate_slide_image.py`: generate one slide image from a prompt through an OpenAI-compatible image API.
- `scripts/generate_slide_deck_images.py`: generate numbered slide images from `NN-topic.md` files.
- `scripts/generate_narration_edge.py`: generate `NN-topic-script-edge.mp3` from `NN-topic-script.md` files using Edge TTS.
- `scripts/export_slides_pdf.py`: export ordered `NN-topic.png` slide images into a multi-page PDF.
- `assets/index-template.html`: the fixed offline presentation player template.
- `references/workflow.md`: detailed reusable workflow and packaging guidance.
- `SKILL-CN.md` and `references/workflow-CN.md`: Chinese companion documentation for colleagues.

Read `references/workflow.md` when the task involves teaching the method, making a colleague-facing package, or generalizing an existing deck into a reusable process.

This skill intentionally does not generate video materials.

Script dependencies are task-specific: image generation needs `openai`, PDF export needs `pillow`, and Edge narration needs `edge-tts`. HTML assembly and asset scanning use only the Python standard library.

## Final Checks

Before finishing:

- Confirm every referenced image exists.
- Confirm `slides.length` matches the intended page count.
- Confirm `audios.length` matches `slides.length` when narration mode is enabled.
- Confirm page numbers are continuous or explicitly explain gaps.
- Confirm Chinese filenames are URI-encoded in browser `src` assignments.
- Confirm the report can be opened without a dev server unless the user requested a web app.
- Mention any validation that could not be run.
