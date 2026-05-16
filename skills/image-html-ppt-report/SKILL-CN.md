# Image HTML PPT Report 中文说明

## 目标

这个 skill 用于制作“基于图片页 + HTML 播放器”的 PPT 风格汇报材料，核心流程是：

```text
汇报主题/目标 -> 页码大纲 -> 每页提示词 -> 每页图片 -> 可选讲稿/音频 -> 离线 index.html 播放器 -> 目录/打包
```

每一页先稳定为一张图片，再用 `index.html` 作为播放入口。这样可以避免不同电脑、不同 PowerPoint 环境造成的版式变化，同时保留“像 PPT 一样汇报”的体验。

## 适用场景

- 内部汇报材料。
- 分享会、培训课件、演示材料。
- 项目进展汇报。
- 需要打包给同事打开的离线演示材料。
- 已经有图片页，需要统一生成 HTML 播放器。

如果用户明确需要 `.pptx` 文件，应使用专门的 PowerPoint 制作能力；本 skill 重点是 image + HTML 工作流。

## 三种模式

### 1. Guided Creation：全流程确认模式

适合正式汇报、重要材料、需要人类把关质量的场景。

人工确认点：

- 确认主题、受众、目标、风格、页数和交付格式。
- 生成页码大纲后等待确认。
- 生成每页提示词后按需等待确认。
- 生成或整理每页图片后，让人类 review 或提出修改。
- 生成讲稿后按需等待确认。
- 讲稿可接受后再生成音频。
- 资产确认后自动生成 `index.html` 和目录。

### 2. Outline-Approved Generation：确认大纲后自动生成模式

适合内部初版、快速草稿、用户只想控制结构而不想逐页确认的场景。

人工确认点：

- 确认主题、受众、目标、风格、页数和交付格式。
- 生成页码大纲后等待确认。
- 大纲确认后，自动完成提示词、图片、可选讲稿/音频、素材目录和 `index.html`。
- 最后报告哪些页面可能需要人工复核。

### 3. Assemble Only：已有素材装配模式

适合用户已经准备好图片页和可选音频/讲稿，只需要生成播放器的场景。

人工确认点：

- 如果源目录不明确，先确认目录。
- 扫描素材，发现阻塞性缺口时再询问。
- 使用 `assets/index-template.html` 和 `scripts/build_index.py` 直接生成 `index.html`。
- 如用户需要，再生成或更新素材目录。

## 推荐目录结构

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

基础版本只要求：

- `NN-topic.png`：编号图片页。
- `index.html`：离线播放入口。

推荐补充：

- `NN-topic.md`：每页图片提示词或页面设计说明。
- `NN-topic-script.md`：每页讲稿。
- `NN-topic-script-edge.mp3`：每页音频。
- `report-assets.md`：素材统计目录。

## HTML 模板原则

新建播放器时优先使用：

- `assets/index-template.html`
- `scripts/build_index.py`

模板包含：

- 主图播放区。
- 上一页/下一页。
- 页码计数。
- 缩略图总览。
- 全屏。
- 工具栏收起。
- 可选音频自动播放模式。
- 键盘快捷键。

缩略图原则：

- 直接复用原始 slide 图片，不额外生成小图。
- 每个缩略图卡片固定宽度。
- 自动折行。
- 数量多时缩略图面板纵向滚动。
- 图片使用 `object-fit: contain`，完整展示，不裁切。

## 文件命名规则

推荐统一英文后缀：

```text
NN-topic.md
NN-topic.png
NN-topic-script.md
NN-topic-script-edge.mp3
```

说明：

- `NN` 使用两位页码，例如 `01`、`02`。
- `topic` 是页面主题，尽量简短稳定。
- `script` 表示讲稿。
- `script-edge` 表示用 Edge TTS 或类似工具生成的讲稿音频。

所有新材料统一使用英文 `script` 命名，不使用 `讲稿` 作为文件名后缀。

`NN-topic-script.md` 必须只放会被朗读出来的正文。这个文件里的所有文字都会进入 TTS 并生成 MP3，不要放建议时长、语气说明、标题、项目符号、Markdown 标记、制作备注或其他说明信息。此类信息应放在 `NN-topic.md`、大纲文档或单独 notes 文件里。

## 素材目录

当用户要求“整理经验”“形成统计目录”“生成素材清单”时，创建 Markdown 目录，包含：

- 材料定位：这套汇报材料用于什么场景。
- 各类文件数量和大小统计。
- 页面目录：页码、主题、图片、提示词、讲稿、音频。
- `index.html` 模块说明。
- 制作流程。
- 命名规则。
- 复用清单。
- 已知问题和改进建议。

## 内置资源

- `assets/index-template.html`：固化的离线播放器模板。
- `scripts/build_index.py`：从编号图片和可选音频生成 `index.html`。
- `scripts/scan_session_assets.py`：扫描目录并输出素材统计和页面映射。
- `scripts/generate_slide_image.py`：通过 OpenAI-compatible 图片 API 生成单页图片。
- `scripts/generate_slide_deck_images.py`：根据 `NN-topic.md` 批量生成编号图片。
- `scripts/generate_narration_edge.py`：根据 `NN-topic-script.md` 生成 `NN-topic-script-edge.mp3`。
- `scripts/export_slides_pdf.py`：把按页码排序的 `NN-topic.png` 图片合并导出为多页 PDF。
- `references/workflow.md`：英文详细工作流。
- `references/workflow-CN.md`：中文详细工作流。

本 skill 不处理视频素材生成。

脚本依赖按任务区分：生成图片需要 `openai`，导出 PDF 需要 `pillow`，生成 Edge 讲稿音频需要 `edge-tts`。只生成 HTML 或扫描素材目录时只使用 Python 标准库。

## 完成前检查

- 确认所有 HTML 引用的图片文件存在。
- 确认 `slides.length` 等于目标页数。
- 如果启用音频，确认 `audios.length` 与 `slides.length` 一致。
- 确认页码连续，或说明缺页原因。
- 确认中文文件名在 HTML 中通过 `encodeURI()` 加载。
- 确认 `index.html` 可以直接用浏览器打开，不依赖开发服务器。
- 明确说明哪些验证没有执行。
