# 通用一次成图提示词 / General One-pass Prompt

先完成 `SKILL.md` 的主题色选择关口：用户未给颜色且未授权自行判断时，首轮展示实际色卡和选项，等待答复，不生成。只有获得明确选色或自动选色授权后，再根据 `style-spec.md` 形成一份事实安全的内容简报，替换尖括号变量。获准自主选色时，优先从六种主题色中选取与素材中文物主体本色同色系或色系相近的颜色，排除背景、展台及叠加文字的颜色干扰；再以材质、冷暖关系与可读性在相近色候选之间取舍。主题色必须填写用户选定或按上述规则选出的名称和 Hex，不得缺省回退青蓝。生成输入默认为用户素材 + 对应主题样例；仅有构图需要时再补一张六色样例，总输入最多三张。综合色卡只用于选色；旧十二兽首参考图和单色色卡截图不输入生成工具。必须完整列出最终文字，未知事实使用中性表达，不保留尖括号。

```text
Use case: infographic-diagram
Asset type: finished vertical museum-style collectible stamp poster, one complete raster image, strict portrait 3:4, target size <768 × 1024 by default or 1536 × 2048 for 2K>. Never use 2:3.

Input images:
- The matching theme example from the six-example set controls layout, typography hierarchy, warm aged-paper texture, distressed frame, seals, ornaments, spacing, and archival print finish. If supplied, one additional example controls composition only. Never inherit their artifact identity, museum, period, grade, wording or artifact-specific emblem.
- Use two images by default: the user artifact and its matching theme example; at most three with the optional composition example. The selection sheet is display-only. Do not supply legacy zodiac references or single-color swatch screenshots.
- Theme PRINTING INK is specified directly: <theme name and exact hex>. Apply it to typography, calligraphy, frame lines, icons, emblems and ornaments, overriding example colors where necessary. It NEVER controls paper color, artifact color or seal color. Paper ALWAYS remains warm ivory #F0ECE3.
- The user image is the sole authority for the new artifact's identity, silhouette, material, color, ornament, condition, and viewing angle: <faithful visual description>.

Primary request:
Create a new museum relic stamp poster for “<文物名>” in the same visual style, not a zodiac or Yuanmingyuan poster. ALWAYS use textured warm ivory #F0ECE3 paper. Use <user-selected theme name and exact hex, or theme chosen under explicit user delegation> as the letterpress INK for all text, frame lines, icons, emblems and ornament; use a light impression of that same ink for the circular cloud medallion. Preserve tiny vermilion seals, distressed rectangular border, generous margins, bilingual hierarchy, and archival print wear. Never use theme ink as background color.

Subject:
A centered museum-quality presentation of <artifact name and category>, closely based on the user image. Preserve <material, colors, silhouette, ornament, condition, proportions, and key structures>. Use soft museum display lighting appropriate to the actual material. Do not turn it into an animal head, bronze sculpture, living subject, cartoon, or unrelated object.

Composition:
Match the packaged series structure: top-left English title block; centered small circular line-art emblem depicting this artifact or category; top-right vertical Chinese title and tiny seal; large distressed theme-ink panel; matching cloud icons left and right, the right cloud an exact horizontal mirror of the left; two four-character vertical calligraphy phrases; artifact centered over a pale same-ink ornamental medallion; attribution line; lower museum note; footer marks. Reuse the EXACT top artifact emblem at the footer, scaled to fit, never an unrelated dragon or zodiac icon. Keep the artifact complete with breathing room and preserve its natural orientation.

Text (render verbatim; no substitutions or extra characters):
"MUSEUM RELIC"
"CULTURAL HERITAGE SERIES"
"<English artifact name>"
"A Legacy of <quality 1>, <quality 2>"
"and Timeless Craft"
"Echo of <English essence>"
"Beauty across centuries, Spirit beyond time."
"<馆名或博物馆>" / "馆藏文物" / "·" / "<文物简称>"
"<馆名或博物馆> · <文物完整名称>"
"<事实安全的中文短句>"
Large left vertical calligraphy: "<左侧四字>"
Large right vertical calligraphy: "<右侧四字>"
"<时代或馆藏文物> | <材质工艺或传统工艺遗存> | <中性价值短语>"
"博物馆" / "文物系列"
"<馆名或博物馆>馆藏文物图章"
"<一至两句事实安全的文物说明>"
"CULTURAL RELIC" / "SERIES"
"匠心永典" / "TIMELESS ETERNAL"
"MUSEUM · ARCHIVE"

Constraints:
One-pass complete image with all text included, targeting exactly <pixel dimensions>. The user image controls subject, material, color, and form; the selected theme example controls style only; the explicit theme name and Hex control printing ink ONLY. Paper remains warm ivory #F0ECE3. Do not include Yuanmingyuan, zodiac, animal-head, or fountain wording unless the artifact genuinely belongs to that topic. Do not invent museum, period, artist, provenance, excavation, collection, or grade. Top and footer must share the same artifact/category emblem, and panel clouds must be mirror-symmetric. No modern UI, photographic background, bright gradients, glossy gold, newly invented watermark, mockup frame, or extra slogans. Preserve required third-party attribution or rights information; removing a watermark or re-rendering an image is not a rights clearance. Do not claim museum endorsement or copy unlicensed distinctive branding. Avoid pseudo-Chinese and prioritize exact text.
```

## 生成后检查 / Post-generation check

1. 主体是否仍是用户文物，未被替换成样例中的文物；输入是否为用户素材 + 对应主题样例，且仅按构图需要补一张样例。
2. 材质、综合色彩、残损、纹饰和视角是否忠于素材。
3. 顶部与底部是否复用同一文物或类别徽记，且没有生肖错配；框顶左右祥云是否为水平镜像。
4. 文案是否彻底移除不相关的圆明园、生肖和喷泉内容。
5. 是否出现未经提供的馆名、年代、作者、来源或等级；出现即修正为中性表述。
6. 先检查原生输出比例；若为严格 3:4 且宽高均不低于目标，使用 `scripts/normalize-output.py` 生成 1K `768 × 1024` 或 2K `1536 × 2048` 交付版。任何 2:3、低于目标或脚本验证失败的输出均不合格，不得裁切或放大冒充合格成品。
7. 纸底是否固定暖象牙 #F0ECE3；所选主题色及 Hex 是否仅用于文字、框线、图标和装饰线，云纹是否为同色淡印；文物本色与暗朱砂小印是否保留。

## 局部修正 / Targeted correction

```text
Use case: precise-object-edit.
Change only <exact location and defect>. Replace it with <exact correction> in the same ink color, line weight, typography, and scale.
Keep absolutely everything else unchanged in appearance: the artifact, all unrelated text, layout, spacing, paper texture, border, seals, medallion, colors, and footer. Do not re-render unrelated text. No new elements or watermark.
```

若模型把文物改成青铜兽首，应重新生成整张，而不是局部修正，因为主体身份和材质已经整体失效。

局部修正最多一次。主体身份、整体材质、整套配色或画布比例错误属于全局失败，可重新生成一次，不计作可局部修正的小错误。原生输出为超规格的严格 3:4 时直接等比向下标准化，不为尺寸单独重生成；像素低于目标时不得放大冒充合格。全局重生成后仍不合格，报告未达标项目与实测尺寸；不得无限重试。
