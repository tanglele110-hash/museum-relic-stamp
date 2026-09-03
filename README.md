# 博物馆文物图章 · Museum Relic Stamp

将一张文物参考图转化为完整的 3:4 竖版图章海报：暖象牙旧纸、六种主题印色、双语标题、竖排书法与文物徽记。

**制作者：@木渡川（TANGLELE）**

An Agent Skill for creating complete museum-artifact stamp posters from a supplied reference image, with six ink themes and bilingual typography.

## 效果预览

![六种主题印色与成品预览](assets/theme-color-options.png)

查看[六张完整样例](assets/theme-examples/README.md)。样例是用户与 AI 协作制作的成品，用于视觉参考，不是博物馆官方出品。

## 使用方法

需要能够读取本地 Skill 文件、查看参考图片，并支持参考图生成与图像编辑的 AI 宿主。本仓库提供工作流程、提示词与样例；图像生成能力及费用由宿主提供。

1. 下载或克隆整个仓库，将包含 `SKILL.md` 的 `museum-relic-stamp` 文件夹放入宿主支持的 Skill 目录。保留 `assets`、`references`、`scripts`、`agents` 与授权文件的相对位置。
2. 按宿主要求重新加载 Skill；上传一张清晰的文物图片，提供文物名及你已知的馆名、年代等信息。
3. 指定主题色，或从展示的色卡中选择；也可以明确说“由你根据文物配色”。
4. 生成后检查文物形态、文字和实际像素尺寸。

```text
调用 museum-relic-stamp，根据这张文物照片生成博物馆图章。
文物名：良渚文化玉琮王
主题色：青蓝
尺寸：768 × 1024
```

亦可在支持 `$skill-name` 的宿主中使用 `$museum-relic-stamp`。

如果宿主不支持安装 Skill，但能够读取本地文件并生成图片，可要求它完整阅读 [SKILL.md](SKILL.md) 及其必读资源后执行。没有图像生成能力的宿主无法仅靠这些文件产出图片。

## 配色与输出

| 主题印色 | Hex |
| --- | --- |
| 青蓝 | `#176F91` |
| 鎏金 | `#D4AF37` |
| 天青灰 | `#A1B4B2` |
| 艾绿 | `#7BAE7F` |
| 枫丹 | `#D46A4A` |
| 青川 | `#87BFB7` |

纸底固定为暖象牙 `#F0ECE3`；主题色用于文字、框线与装饰，保留文物本色。支持自定义主题色。

- 默认目标尺寸：`768 × 1024`；可选：`1536 × 2048`，均为 3:4 竖版。
- 一次生成包含文字的完整图片；最多一次局部修正、一次全局重生成。
- 六张历史样例实际为 `1086 × 1448`，只作风格参考，不代表新图达到目标像素规格。
- 生成模型可能出现文字或尺寸偏差；Skill 要求实测检查并如实报告，不能保证每次生成都达标。
- 文物身份、形态、材质与本色以用户图片为依据；缺失的馆名、年代和文物级别不得编造。

## 文件说明

| 路径 | 内容 |
| --- | --- |
| [SKILL.md](SKILL.md) | 触发条件、输入边界、选色和生成流程 |
| [references/style-spec.md](references/style-spec.md) | 构图、配色、文案与材质规范 |
| [references/prompt-template.md](references/prompt-template.md) | 一次成图提示词与修正规则 |
| [assets/theme-examples/](assets/theme-examples/README.md) | 六张原始 PNG 样例与校验清单 |
| [assets/theme-color-options.png](assets/theme-color-options.png) | 六色总览 PNG |
| [scripts/build-theme-color-options.ps1](scripts/build-theme-color-options.ps1) | Windows 色卡维护脚本 |
| [agents/openai.yaml](agents/openai.yaml) | 宿主显示信息 |

日常使用不需要运行维护脚本。重新排版色卡需要 Windows、System.Drawing，以及具有相应用途授权的华文楷体和 Georgia 字体；先用 `-OutputDirectory` 输出到独立目录检查。仓库不包含字体文件或 SVG。

## 授权与署名

- **脚本、提示词和说明文档：[MIT](LICENSE)**。
- **制作者有权授权的原创视觉贡献：[CC BY 4.0](LICENSE-ASSETS.md)**，包括六张样例及色卡中的原创贡献。复用时请署名、链接许可并说明修改。
- **官方文物图片、字体及其他第三方材料保留原有权利与适用条件**，不因本仓库开源而自动获得 MIT 或 CC BY 授权。

文物参考图片均来自官方公开图片资料。公开展示不等于开放许可；具体来源记录与字体商用条件见[素材来源、字体与署名](references/rights-and-attribution.md)及[素材清单](assets/rights-manifest.json)。本项目不代表博物馆官方授权或背书。

建议视觉署名：`原创视觉：@木渡川（TANGLELE），CC BY 4.0`，附上许可链接；改编时另说明实际修改。仅使用 Skill 不会让新生成作品自动继承上述许可证，直接复用受许可内容时仍须遵守相应条件。
