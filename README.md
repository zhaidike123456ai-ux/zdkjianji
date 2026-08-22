# zdkjianji

[![Validate Skill](https://github.com/zhaidike123456ai-ux/zdkjianji/actions/workflows/validate.yml/badge.svg)](https://github.com/zhaidike123456ai-ux/zdkjianji/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`zdkjianji` 是一套面向中文口播视频的 Codex Skill，将转写、口误与气口清理、字幕纠错、Remotion 视觉设计、工作台预览、多人视觉审查和高清交付串成一条可复用流程。

仓库中的 [SKILL.md](SKILL.md) 是 Codex 的执行规范；本 README 用于介绍安装和使用方法。

## 主要能力

- 检测 MP4/MOV 源素材的分辨率、帧率、色彩和音轨。
- 创建 480P/720P 恒定帧率代理，降低 Remotion Studio 预览压力。
- 生成词级时间码，识别并删除口误、重录残句、气口和无意义停顿。
- 纠正 ASR 错字，按语义重排字幕并避免标题、人物窗和字幕相互遮挡。
- 根据口播内容设计信息卡片、因果链、步骤动画、转场和总结页。
- 支持三个视觉子代理独立评分，最后交叉验证问题和修改优先级。
- 根据原素材和发布需求推荐 1080P、2K 或其他输出规格。
- 检查 BT.709、`yuv420p`、音画时长、完整解码和关键画面。

## 安装

将仓库克隆到 Codex Skills 目录：

```bash
git clone https://github.com/zhaidike123456ai-ux/zdkjianji.git ~/.codex/skills/zdkjianji
```

重新打开 Codex 会话后即可调用：

```text
使用 $zdkjianji 处理这条口播视频，先转写并删除口误和气口，完成风格预览后再询问我是否渲染。
```

## 工作流程

1. 检测源素材参数，给出代理和最终输出建议。
2. 生成原始逐字稿、词级时间码和字幕。
3. 输出口误、重录、停顿和气口审查清单。
4. 经确认后生成连续剪辑母版并同步重映射字幕时间轴。
5. 先完成风格帧、知识卡片和语义动效设计。
6. 使用 480P/720P 代理在 Remotion Studio 预览。
7. 用户确认后继续修改；需要时进行三个视觉代理独立审查。
8. 确认完整效果和输出分辨率后才渲染高清母版。
9. 完成媒体、字幕、音画和关键画面质检后交付。

## 清晰度决策

最终输出不会机械地固定为某个分辨率，而是先检查原素材，再向用户给出建议：

| 原素材 | 通常建议 |
|---|---|
| 低于 1080P | 保持原生，或使用 1080P 设计画布并明确不会恢复真实细节 |
| 1080×1920 竖屏 | 保持原生 1080P，避免无意义放大 |
| 不低于 1440×2560 | 可选择 2K，或用 1080P 降低体积与渲染时间 |
| 4K 或多素材混剪 | 根据主素材、最低质量素材和发布平台共同判断 |

用户没有指定时，Skill 会先报告源素材状态，给出推荐项和备选项，再询问用户确认。代理预览清晰度与最终导出清晰度独立设置。

## 内置工具

检查源视频：

```bash
python3 scripts/probe_media.py input.mp4 --json
```

生成 720P 代理：

```bash
python3 scripts/make_proxy.py input.mp4 proxy.mp4 --height 720 --fps 30
```

校验终版字幕：

```bash
python3 scripts/validate_srt.py captions.srt
```

脚本需要 Python 3，并依赖系统可执行的 `ffmpeg` 与 `ffprobe`。

## 仓库结构

```text
zdkjianji/
├── SKILL.md                       # Codex 执行入口
├── agents/openai.yaml             # Skill 界面元数据
├── references/                    # 字幕、视觉、分辨率和质检规则
├── scripts/                       # 媒体检测、代理生成、SRT 校验
└── assets/knowledge-card/         # 可复用 Remotion 知识卡片资产
```

## 持续优化

每次真实项目结束后，只将可复现、跨项目有效的经验写回 Skill。项目专属文案和偶发审美偏好保留在项目内。修改后重新运行仓库自检：

```bash
python3 scripts/check_skill.py .
```

详细规则请查看 [references/optimization-loop.md](references/optimization-loop.md)。

## 参与贡献

提交改进前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。优先提交能够复现、适用于多条素材的流程改进，并附上验证方法。

## 许可协议

本项目使用 [MIT License](LICENSE)。
