# office-skills

面向日常办公场景的 Agent Skills 集合。

这个仓库用于沉淀可复用的办公工作流，把资料整理、汇报材料、会议纪要、调研报告、周报复盘等高频任务逐步整理成：

```text
workflow + skill + template + script + example
```

这里的 skill 不只是提示词，而是一套可交给 Agent 使用的工作方法，包括：

- 任务边界
- 文件命名规范
- 人工确认点
- 可执行脚本
- 输出模板
- 验证规则
- 跨工具使用说明

## Skills

### image-html-ppt-report

路径：

```text
skills/image-html-ppt-report/
```

用途：

用“图片页 + HTML 播放器”的方式制作 PPT 风格汇报材料。

核心链路：

```text
NN-topic.md
-> NN-topic.png
-> NN-topic-script.md
-> NN-topic-script-edge.mp3
-> index.html
-> report.pdf
```

支持三种模式：

1. 全流程确认模式：从主题、大纲、提示词、图片、讲稿到音频逐步确认。
2. 确认大纲后自动生成模式：确认页码大纲后，自动完成后续材料。
3. 已有素材装配模式：已有图片和可选音频时，直接生成 HTML 播放器和 PDF。

## 推荐仓库结构

```text
office-skills/
├── README.md
└── skills/
    └── image-html-ppt-report/
        ├── SKILL.md
        ├── SKILL-CN.md
        ├── README.md
        ├── agents/
        ├── assets/
        ├── references/
        └── scripts/
```

## 使用方式

### Codex

可以把某个 skill 复制到：

```text
~/.codex/skills/
```

也可以放到项目内：

```text
project-root/.codex/skills/
```

### Claude Code / OpenClaw / 其他 Agent 工具

这些工具不一定原生识别 Codex Skill 格式，但可以把 skill 当作项目指南和工具脚本使用。

具体适配方式见：

```text
skills/image-html-ppt-report/README.md
```

## 积累方式

不需要一次性覆盖所有办公场景。

更推荐的节奏是：

```text
第一次：用 AI 临时完成任务。
第二次：整理文件结构和人工确认点。
第三次：把重复动作写成脚本。
后续：沉淀成 skill，并放进这个仓库。
```

当 skills 慢慢积累起来，这个仓库就会变成个人或团队的办公 Agent 工作台资产库。
