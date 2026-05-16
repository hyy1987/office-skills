# Image + HTML PPT 汇报材料工作流

本文是 `image-html-ppt-report` 的中文工作流说明，用于给同事理解和复用。

## 核心思想

不要把 `index.html` 当普通网页做，而是把它当作“汇报材料播放器”：

```text
编号图片页 + 可选讲稿音频 + 静态 HTML 控制器
```

浏览器只负责稳定展示图片页、切换页面、播放音频和显示缩略图。这样材料更容易打包、复制和发送给同事。

这个工作流只覆盖图片页、可选讲稿音频、静态 HTML 和素材目录，不处理视频生成。

PDF 应由按页码排序的 `NN-topic.png` 直接合并生成，不走 HTML 转 PDF。

## 三种创建模式

### 1. 全流程确认模式

适合正式汇报。

```text
主题/目标 -> 确认
页码大纲 -> 确认
每页提示词 -> 质量要求高时确认
每页图片 -> review
讲稿 -> 需要旁白时确认
音频 -> 正式播放时试听
index.html -> 自动生成
```

这个模式最稳，但人工参与最多。

### 2. 确认大纲后自动生成模式

适合快速初版或内部材料。

```text
主题/目标 -> 确认
页码大纲 -> 确认
提示词/图片/讲稿/音频/目录/index.html -> 自动生成
```

大纲确认后，后续尽量自动完成。完成后再列出需要人工复核的页面。

### 3. 已有素材装配模式

适合用户已经准备好素材。

```text
扫描目录 -> 提示阻塞性缺口 -> 生成 index.html -> 可选生成素材目录
```

这个模式主要使用：

```text
scripts/build_index.py
scripts/scan_session_assets.py
```

## 推荐资产单元

每一页推荐使用一组文件：

```text
NN-topic.md
NN-topic.png
NN-topic-script.md
NN-topic-script-edge.mp3
```

含义：

- `.md`：图片生成提示词或页面设计说明。
- `.png`：最终幻灯片图片。
- `-script.md`：讲稿。
- `-script-edge.mp3`：讲稿音频。

`NN-topic-script.md` 只能包含要被朗读出来的正文。音频生成脚本会把文件里的所有文字送入 TTS，所以不要写建议时长、语气说明、标题、项目符号、Markdown 标记或制作备注。这些信息应放到提示词、大纲或单独 notes 文件中。

音频脚本默认不额外插入朗读内容，只保留原文段落换行。

最小可用版本只需要 `.png` 和 `index.html`。

## 播放器模板

新建播放器时使用：

```text
assets/index-template.html
```

或用脚本生成：

```text
python scripts/build_index.py <report-folder> --title "Report Title"
```

模板已经包含：

- 上一页/下一页。
- 页码计数。
- 缩略图总览。
- 全屏。
- 工具栏收起。
- 可选音频模式。
- 键盘快捷键。

## 缩略图规则

缩略图直接复用原始图片页，不额外生成小图。

布局规则：

- 每个缩略图卡片固定宽度。
- 不按照固定 15 页布局。
- 任意数量自动折行。
- 超出屏幕高度时，缩略图面板内部纵向滚动。
- 图片完整展示，不裁切。

## HTML 文件生成原则

最终 `index.html` 使用显式数组：

```js
const slides = ["01-title.png", "02-background.png"];
const audios = ["01-title-script-edge.mp3", "02-background-script-edge.mp3"];
```

不要依赖浏览器在本地扫描目录，因为普通本地 HTML 无法可靠列出文件夹内容。

中文文件名、空格和标点要通过：

```js
encodeURI(file)
```

再赋值给 `img.src` 或 `audio.src`。

## 素材目录

一套可复用材料建议包含一个 Markdown 素材目录，记录：

1. 材料用途。
2. 文件类型统计。
3. 页面映射。
4. HTML 模块说明。
5. 制作流程。
6. 命名规则。
7. 复用清单。
8. 已知问题和改进建议。

## 打包建议

分享最终汇报材料时：

- 发送整个 report folder，不要只发 `index.html`。
- 图片和音频默认与 `index.html` 放同一目录。
- 避免 HTML 中出现绝对路径。
- 打包后重新打开 `index.html` 测试一次。

分享 skill 给同事时：

- 发送 `image-html-ppt-report/` 这个 skill 文件夹。
- 同事可以放到自己的 Codex skills 目录，或某个项目的 `.codex/skills/` 目录。
- 示例汇报材料不要混进 skill，除非明确作为模板资产维护。

## 常见风险

- HTML 中引用的文件后来被改名。
- 图片数组和音频数组长度不一致。
- 中文文件名没有做 URI 编码。
- 浏览器阻止音频自动播放。
- 原目录能打开，打包后因为绝对路径失效。
- 缩略图或控制栏在小屏幕上挤压变形。
