# 参与贡献

感谢你改进 `zdkjianji`。本仓库优先接受能够降低返工、提高媒体兼容性或适用于多条口播素材的改进。

## 提交流程

1. Fork 仓库并从 `main` 创建功能分支。
2. 修改 Skill、参考规则、脚本或可复用资产。
3. 运行 `python3 scripts/check_skill.py .`。
4. 如果修改了代理或字幕脚本，使用一段真实媒体做代表性测试。
5. 提交 Pull Request，说明问题、修改内容、适用范围和验证结果。

## 内容要求

- 保持 `SKILL.md` 简洁，详细规则放入 `references/`。
- 重复且容易出错的机械操作优先写成 `scripts/`。
- 不提交原视频、成片、音频、密钥、个人信息或大型临时文件。
- 不把单个项目的专属文案或偶发审美偏好固化为默认流程。
- 改动字幕规则时，兼顾文本准确性、时间码映射和视觉安全区。
- 改动分辨率规则时，区分代理预览、设计画布和最终母版。

## 提交信息

使用简短、明确的动词开头，例如：

```text
Add subtitle overlap validation
Improve 2K output decision rules
Fix proxy aspect-ratio handling
```

