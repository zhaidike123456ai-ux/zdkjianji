# 高清交付质检

## 媒体门槛

- 尺寸必须等于用户确认的输出规格；未确认前不得把 1080P 或 2K 写成固定结果。
- 若采用 1080P 发布画布，竖屏使用 1080×1920、横屏使用 1920×1080；更高规格按 `resolution-policy.md` 判断。
- 帧率与制作 Composition 一致，常用 30fps CFR。
- H.264 + AAC 作为通用 MP4 交付格式。
- 像素格式使用 `yuv420p`。
- HD 输出统一标记为 BT.709、limited/TV range，避免 `yuvj420p` 和 BT.470BG 被平台误解。
- 音视频时长差通常不超过 100ms；尾帧静音可按内容判断。

## 必做检查

```bash
ffprobe -v error -show_streams -show_format final.mp4
ffmpeg -v error -i final.mp4 -f null -
```

确认：尺寸、帧率、总帧数、色彩四项、音频采样率、声道、时长，以及完整解码无报错。

## 重复帧判断

全画面以静态卡片为主、小人物窗为辅时，`freezedetect` 会误判。先定位人物窗，再裁切动态区域检测：

```bash
ffmpeg -i final.mp4 -vf "crop=w:h:x:y,freezedetect=n=-50dB:d=0.5" -an -f null -
```

结合关键帧截图和实际播放确认，不把单一检测器当作最终结论。

## 视觉抽检

至少抽取：首帧、每个章节建立帧、每个转场中点、总结页、结尾页。检查文字裁切、素材黑屏、层级碰撞、人物窗、错误占位和重复 CTA。

## 交付策略

先写入临时路径，通过检查后再替换 `output/final/`。旧版本移动到 `output/archive/`，并告知用户是否可恢复。
