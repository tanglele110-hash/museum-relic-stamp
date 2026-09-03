# 选色色卡维护

- `theme-color-options.png`：实际展示的 1536 × 2048、3:4 竖版色卡；包内不需要 SVG。
- 六张图章是用户确认的自制样例，只缩放排版，不重新绘制图章内文字。颜色映射来自 `theme-examples/manifest.json`。
- 中文标签使用华文楷体/STKaiti，数字和色号使用 Georgia，均已渲染在 PNG 内；字体文件不随包分发。[字体使用与商用条件](../references/rights-and-attribution.md#字体使用说明)。
- `theme-color-options-build-info.json` 记录 PNG 的构建尺寸、字体和校验值。
- 在具有相应字体使用许可且已安装字体的 Windows 环境中，运行 `../scripts/build-theme-color-options.ps1` 重建 PNG；用 `-OutputDirectory` 指定预览目录。脚本不联网、不安装字体、不生成 SVG。
- 色卡仅用于选色，不作为主体或风格参考输入。仍保留六种印色及第七项自主选色入口，固定纸底为暖象牙 `#F0ECE3`。

制作者：@木渡川（TANGLELE）。
