---
name: zdkjianji
description: "End-to-end Chinese talking-head video editing workflow for MP4/MOV media: inspect source quality, create a 480P/720P proxy, transcribe with word timestamps, remove verbal mistakes and breathing gaps, correct and semantically paginate captions, design reusable Remotion knowledge-card visuals, preview in Remotion Studio, run independent visual reviews, render an approved 1080P/2K master, and perform audio/video/color QA. Use when Codex is asked to 剪口播、处理口误气口、制作字幕、设计信息卡片或转场、解决 Remotion 预览卡顿、制作竖屏知识视频、输出高清成片，或把既有剪辑流程复用于新素材。"
---

# ZDK 剪辑

把“转写—精剪—视觉设计—预览确认—高清交付”作为有门禁的流水线执行。保留源文件，所有中间产物写入项目目录。

## 核心原则

- 先检查，再处理；先代理预览，再用母版渲染。
- 先制作审查稿和删除清单，再改变时间线。
- 字幕忠于实际语音，只纠正明确的 ASR 错字、数字、专名和断句。
- 动效表达语义，不为“有动画”而动画。
- 在用户确认 Studio 预览前，不渲染完整成片。
- 先依据源素材提出推荐分辨率；若用户未指定或候选规格会明显影响质量、体积和渲染时间，先询问用户再锁定输出。不得无依据放大。
- 每一步都产生可检查的文件，不把诊断和修复混在一起。

## 执行流程

1. 阅读 [workflow.md](references/workflow.md)，建立项目目录和阶段门禁。
2. 运行 `scripts/probe_media.py <video>`，记录分辨率、帧率、时长、色彩和音轨；阅读 [resolution-policy.md](references/resolution-policy.md)，向用户说明推荐值和可选值。
3. 运行 `scripts/make_proxy.py <input> <output> --height 720` 创建代理文件；低性能设备可用 480。
4. 转写词级时间码，生成原始逐字稿、SRT 和 JSON。先保留原话，不立即润色。
5. 依据 [caption-rules.md](references/caption-rules.md) 标出口误、重录残句、长停顿、气口和可疑识别，生成审查稿与删除清单。
6. 经确认后构建连续剪辑母版。优先一次性生成连续 CFR 媒体，避免大量碎片 `<Video>` 造成浏览器解码抖动。
7. 从纠正后的词级时间码生成语义短句字幕；同步映射所有删除区间，禁止只改文字不改时间码。
8. 阅读 [visual-design.md](references/visual-design.md)，先完成风格帧和关键场景设计。可复制 `assets/knowledge-card/` 作为起点。
9. 在 Remotion Studio 使用代理素材预览。检查关键帧、字幕安全区、转场边界和实时播放；先让用户确认，再迭代。
10. 用户明确要求多人审查时，让三个视觉子代理独立评分，禁止互看结论；主代理最后交叉验证并形成优先级修改清单。
11. 用户确认完整效果和输出分辨率后再渲染；母版视频优先使用 `OffthreadVideo`，代理预览可使用 `@remotion/media` 的 `Video`。
12. 按 [quality-gates.md](references/quality-gates.md) 完成解码、色彩、音画、字幕和关键画面检查，再交付成片、SRT、逐字稿与时间码。

## 阶段门禁

- **转写门禁**：逐字稿、时间码、口误清单可读且可追溯。
- **剪辑门禁**：连续母版时长正确，删除点无吞字、爆音和不自然跳切。
- **设计门禁**：先展示 Studio 预览，不以完整渲染代替预览确认。
- **审查门禁**：高优先级问题修完；字幕不与页面标题、人物窗或平台 UI 冲突。
- **交付门禁**：用户确认画面和分辨率后才导出；媒体检查全部通过。

## 分辨率决策

- 用户已明确指定分辨率时，先判断源素材能否真实支撑，再执行或说明放大限制。
- 用户未指定时，先报告源分辨率并给出一个推荐项、至多两个备选项，说明清晰度、文件体积和渲染时间差异，然后询问用户。
- 1080×1920 竖屏源通常推荐原生 1080P；不要默认放大到 1440×2560。源素材达到或超过 2K 时，才把 2K 作为自然候选。
- 低于 1080P 的源素材可以放在 1080P 设计画布中交付，但必须说明这不会恢复源视频的真实细节。
- 代理分辨率与最终分辨率分开决定：代理使用 480P/720P 不限制最终母版规格。

## 字幕与画面联动

- 从名词、动作、因果和步骤中提取视觉锚点。例如“空调直吹”映射气流箭头，“猛灌冰水”映射四步因果，“强光暴晒”映射 UV 射线和防护状态。
- 每个章节只保留一个主焦点。页面大标题出现时，字幕延后 6–10 帧或移动到固定安全区。
- 烧录字幕通常控制为 1–2 行；在中文短视频中优先按语义分组，不按固定字数机械切分。
- 源视频已有文字时，裁切、遮罩或只保留一套 CTA，避免三层文字叠加。

## 预览卡顿诊断

- 先确认 Studio 使用的是 480P/720P CFR 代理，而非高码率母版。
- 减少同屏视频解码器、模糊滤镜和超大阴影；只对当前场景挂载媒体。
- 区分“预览掉帧”和“导出重复帧”。静态大卡片配小人物窗会让整帧 `freezedetect` 误报；应裁切人物动态区域复核。
- 不用完整高清渲染反复试错；用 Studio、关键帧截图或短帧区间渲染验证。

## 持续优化

每次完成真实项目后，阅读 [optimization-loop.md](references/optimization-loop.md)。只把可复现、跨项目有效的经验写回 Skill；项目专属文案和偶发偏好留在项目内。修改后重新运行验证脚本和至少一个代表性测试。
