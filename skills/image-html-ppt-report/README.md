# Image HTML PPT Report Skill

这是一个用于制作“基于图片页 + HTML 播放器”的 PPT 风格汇报材料的 Agent Skill。

当前目录是 **Codex Skill** 格式，同时也可以被 Claude Code、OpenClaw 或其他支持项目指令/工具脚本的 Agent 工作台复用。

## 这个 Skill 做什么

它支持三种工作模式：

1. **全流程确认模式**
   从主题开始，逐步确认目标、大纲、提示词、图片、讲稿、音频，最后生成 `index.html`。

2. **确认大纲后自动生成模式**
   人类确认页码大纲后，后续自动生成提示词、图片、讲稿、音频、素材目录和 HTML 播放器。

3. **已有素材装配模式**
   已经有 `NN-topic.png` 和可选音频时，直接生成离线 `index.html` 播放器。

推荐命名：

```text
NN-topic.md
NN-topic.png
NN-topic-script.md
NN-topic-script-edge.mp3
```

## 目录结构

```text
image-html-ppt-report/
├── SKILL.md
├── SKILL-CN.md
├── README.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── index-template.html
├── references/
│   ├── workflow.md
│   └── workflow-CN.md
└── scripts/
    ├── build_index.py
    ├── export_slides_pdf.py
    ├── generate_narration_edge.py
    ├── generate_slide_deck_images.py
    ├── generate_slide_image.py
    └── scan_session_assets.py
```

## 在 Codex 中使用

### 全局安装

把整个 `image-html-ppt-report/` 文件夹放到：

```text
~/.codex/skills/
```

Windows 常见位置：

```text
C:\Users\<你的用户名>\.codex\skills\
```

然后在 Codex 里这样使用：

```text
Use $image-html-ppt-report，围绕“某个主题”做一套 12 页汇报材料。
```

或者：

```text
Use $image-html-ppt-report，把当前目录已有的 PNG 图片生成 index.html 播放器。
```

### 项目内使用

也可以把它放到某个项目目录下：

```text
project-root/.codex/skills/image-html-ppt-report/
```

这种方式适合只在某个项目或团队资料目录里使用。

## 在 Claude Code 中适配

Claude Code 不一定原生识别 Codex Skill 的 `SKILL.md` 机制，但可以把本 skill 当作“项目级工作指南 + 工具脚本”使用。

推荐做法：

1. 把整个 `image-html-ppt-report/` 放进项目资料目录，例如：

```text
project-root/agent-skills/image-html-ppt-report/
```

2. 在项目的 `CLAUDE.md` 中加入引用说明：

```markdown
## Image HTML PPT Report

When creating PPT-style report materials based on slide images and offline HTML playback, follow:

- `agent-skills/image-html-ppt-report/SKILL.md`
- Chinese reference: `agent-skills/image-html-ppt-report/SKILL-CN.md`
- Detailed workflow: `agent-skills/image-html-ppt-report/references/workflow.md`

Use `assets/index-template.html` as the default HTML player template.
Use `scripts/generate_slide_image.py` or `scripts/generate_slide_deck_images.py` to generate slide images.
Use `scripts/generate_narration_edge.py` to generate narration audio.
Use `scripts/build_index.py` to generate `index.html` from numbered slide images.
Use `scripts/scan_session_assets.py` to inspect existing report folders.
Use `scripts/export_slides_pdf.py` to export ordered slide images to PDF.
```

3. 使用时对 Claude Code 说：

```text
请按照 agent-skills/image-html-ppt-report/SKILL-CN.md 的流程，
把这个目录里的汇报图片生成一个离线 index.html 播放器。
```

如果 Claude Code 支持自定义 slash command，也可以创建一个命令，把 `SKILL-CN.md` 的核心流程作为命令说明。

## 在 OpenClaw 中适配

OpenClaw 或类似 Agent 工作台通常会有项目说明、上下文目录、工具脚本目录或任务模板。适配时不需要依赖 Codex 的 skill 加载机制。

推荐放置方式：

```text
project-root/
├── agent-guides/
│   └── image-html-ppt-report/
│       ├── SKILL.md
│       ├── SKILL-CN.md
│       ├── assets/
│       ├── references/
│       └── scripts/
└── reports/
    └── your-report-folder/
```

在 OpenClaw 的项目说明或工作台配置中加入：

```text
当任务涉及汇报材料、分享会材料、图片页转 HTML 播放器、素材统计目录时，
读取 agent-guides/image-html-ppt-report/SKILL-CN.md。

默认使用三种模式：
1. 全流程确认模式
2. 确认大纲后自动生成模式
3. 已有素材装配模式

生成 HTML 时优先使用 assets/index-template.html。
生成图片时运行 scripts/generate_slide_image.py 或 scripts/generate_slide_deck_images.py。
生成音频时运行 scripts/generate_narration_edge.py。
已有素材时运行 scripts/build_index.py。
统计素材时运行 scripts/scan_session_assets.py。
导出 PDF 时运行 scripts/export_slides_pdf.py。
```

## 环境和依赖

本 skill 的核心材料规范和 HTML 模板不依赖特定 Agent 工具，但脚本运行需要本机有 Python 环境。

基础要求：

- Python 3.10 或更新版本。
- 能在命令行中运行 `python`。
- 如果只扫描素材目录或把已有 PNG 装配成 `index.html`，不需要安装第三方 Python 包。

按功能安装依赖：

```bash
# 生成图片
pip install openai

# 把 PNG 按页码合并成 PDF
pip install pillow

# 生成 Edge TTS 讲稿音频
pip install edge-tts
```

如果需要一次性启用全部脚本：

```bash
pip install openai pillow edge-tts
```

各脚本依赖如下：

| 脚本 | 用途 | 外部依赖 |
| --- | --- | --- |
| `scripts/build_index.py` | 从 `NN-topic.png` 和可选 MP3 生成 `index.html` | 无，使用 Python 标准库 |
| `scripts/scan_session_assets.py` | 扫描素材目录并输出统计信息 | 无，使用 Python 标准库 |
| `scripts/generate_slide_image.py` | 根据单页提示词生成 PNG | `openai`，以及 OpenAI 或兼容图片 API |
| `scripts/generate_slide_deck_images.py` | 批量调用图片生成脚本 | `openai`，以及 OpenAI 或兼容图片 API |
| `scripts/generate_narration_edge.py` | 根据 `NN-topic-script.md` 生成 MP3 | `edge-tts`，需要能访问 Edge TTS 服务 |
| `scripts/export_slides_pdf.py` | 把按页码排序的 PNG 合并为 PDF | `pillow` |

图片生成相关环境变量：

- `OPENAI_API_KEY`：默认读取的 API key 环境变量。
- `OPENAI_BASE_URL`：可选，使用 OpenAI-compatible 服务时配置。
- `OPENAI_IMAGE_MODEL`：可选，覆盖默认图片模型。
- `PPT_IMAGE_SIZE`：可选，覆盖默认图片尺寸。
- `PPT_IMAGE_QUALITY`：可选，传递给图片 API 的质量参数。

注意：不要把真实 API key、`.env` 文件、生成的 MP3/PNG/PDF 等材料提交到公开仓库。仓库中的 `.gitignore` 已默认忽略常见密钥文件和生成产物，但提交前仍应检查 `git status` 和敏感字段搜索结果。

## 脚本用法

### 生成单页图片

```bash
python scripts/generate_slide_image.py path/to/01-title.md -o path/to/01-title.png
```

常用参数：

```bash
python scripts/generate_slide_image.py path/to/01-title.md \
  --model gpt-image-2 \
  --size 1536x1024 \
  --env-key OPENAI_API_KEY
```

如果使用兼容 OpenAI 的图片服务：

```bash
python scripts/generate_slide_image.py path/to/01-title.md \
  --base-url https://your-compatible-endpoint/v1
```

### 批量生成图片

目录中准备：

```text
01-title.md
02-background.md
03-plan.md
```

运行：

```bash
python scripts/generate_slide_deck_images.py path/to/report-folder
```

如需让第 2 页开始参考上一页图片风格：

```bash
python scripts/generate_slide_deck_images.py path/to/report-folder --reference-previous
```

### 生成讲稿音频

`NN-topic-script.md` 必须是纯朗读正文。文件里的所有文字都会进入 TTS 生成 MP3，不要写建议时长、语气说明、标题、项目符号、Markdown 标记或制作备注。

单文件：

```bash
python scripts/generate_narration_edge.py path/to/01-title-script.md
```

目录批量：

```bash
python scripts/generate_narration_edge.py path/to/report-folder
```

默认输出：

```text
NN-topic-script-edge.mp3
```

默认只保留原文段落换行，不额外插入朗读内容。

### 扫描素材目录

```bash
python scripts/scan_session_assets.py path/to/report-folder
```

输出 Markdown 格式的素材统计和页面映射。

输出 JSON：

```bash
python scripts/scan_session_assets.py path/to/report-folder --json
```

### 生成 index.html

```bash
python scripts/build_index.py path/to/report-folder --title "Report Title"
```

默认会在目标目录生成：

```text
index.html
```

也可以指定输出文件：

```bash
python scripts/build_index.py path/to/report-folder --title "Report Title" --output report.html
```

## 给同事的最小使用说明

如果同事只想把已有图片做成 HTML 播放器：

1. 准备素材目录：

```text
01-title.png
02-background.png
03-solution.png
```

2. 可选准备音频：

```text
01-title-script-edge.mp3
02-background-script-edge.mp3
03-solution-script-edge.mp3
```

3. 运行：

```bash
python image-html-ppt-report/scripts/build_index.py path/to/report-folder --title "汇报标题"
```

4. 打开生成的：

```text
path/to/report-folder/index.html
```

### 导出 PDF

PDF 由编号图片页直接合并生成，不通过 HTML 转 PDF。

```bash
python scripts/export_slides_pdf.py path/to/report-folder -o report.pdf
```

脚本会扫描：

```text
NN-topic.png
```

按页码排序后输出多页 PDF。

## 注意事项

- 最终 HTML 是静态文件，不需要开发服务器。
- 当前 skill 不生成视频素材。
- 不要只发送 `index.html`，要连同图片和音频一起发送。
- 文件名可以用中文，但 HTML 中必须通过 `encodeURI()` 加载；模板已处理。
- 图片按两位页码排序，例如 `01-`、`02-`。
- zip 包发布前，应重新运行校验和一次生成测试。
