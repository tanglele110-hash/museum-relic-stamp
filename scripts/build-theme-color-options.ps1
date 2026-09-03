param(
  [string]$SkillRoot = (Split-Path $PSScriptRoot -Parent),
  [string]$OutputDirectory = ''
)
$ErrorActionPreference = 'Stop'
if (-not $OutputDirectory) { $OutputDirectory = Join-Path $SkillRoot 'assets' }
Add-Type -AssemblyName System.Drawing
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$manifest = Get-Content -LiteralPath (Join-Path $SkillRoot 'assets\theme-examples\manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($manifest.examples.Count -ne 6) { throw 'Expected six theme examples.' }
$bmp = [System.Drawing.Bitmap]::new(1536, 2048)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$fontFamily = [System.Drawing.FontFamily]::new('华文楷体')
$numberFamily = [System.Drawing.FontFamily]::new('Georgia')
function Rect([float]$x,[float]$y,[float]$w,[float]$h,[string]$color) {
  $brush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($color))
  try { $g.FillRectangle($brush,$x,$y,$w,$h) } finally { $brush.Dispose() }
}
function Label([string]$text,[float]$x,[float]$y,[float]$size,[string]$color,[switch]$Number) {
  $family = if ($Number) { $numberFamily } else { $fontFamily }
  $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
  $format = [System.Drawing.StringFormat]::GenericTypographic.Clone()
  $brush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($color))
  try {
    $path.AddString($text,$family,0,$size,[System.Drawing.PointF]::new($x,$y),$format)
    $bounds = $path.GetBounds()
    if ($bounds.Right -gt 1472 -or $bounds.Bottom -gt 2020) { throw "Text exceeds safe bounds: $text" }
    $g.FillPath($brush,$path)
  } finally { $path.Dispose();$format.Dispose();$brush.Dispose() }
}
function Picture([string]$file,[float]$x,[float]$y,[float]$w,[float]$h) {
  $img = [System.Drawing.Image]::FromFile($file)
  try { $g.DrawImage($img,[System.Drawing.Rectangle]::new([int]$x,[int]$y,[int]$w,[int]$h),0,0,$img.Width,$img.Height,[System.Drawing.GraphicsUnit]::Pixel) } finally { $img.Dispose() }
}
try {
  Rect 0 0 1536 2048 '#F0ECE3'
  Label '博物馆图章' 72 62 76 '#343B3A'
  Label '六色印谱' 1160 92 46 '#343B3A'
  Rect 72 166 1392 2 '#D2CCC1'
  Label '选择主题印色' 72 194 36 '#343B3A'
  Label '暖象牙纸底 · 主题色用于文字、框线与图标' 584 201 28 '#626C69'
  $names = @('良渚文化玉琮王','五代鎏金纯银阿育王塔','辽代金盖鹅形水晶香囊','春秋伎乐铜屋','河姆渡文化木胎朱漆碗','元龙泉窑青瓷舟形砚滴')
  for ($i=0; $i -lt 6; $i++) {
    $e = $manifest.examples[$i]
    $source = Join-Path $SkillRoot ('assets\theme-examples\'+$e.file)
    if ((Get-FileHash -LiteralPath $source).Hash -ne $e.sha256) { throw 'Example source differs from manifest.' }
    $x = 72 + ($i % 3)*480
    $y = 286 + [math]::Floor($i/3)*784
    Picture $source $x $y 432 576
    Rect $x ($y+596) 432 22 $e.ink
    Label ('{0:D2}' -f ($i+1)) $x ($y+640) 27 '#626C69' -Number
    Label $e.theme ($x+60) ($y+630) 45 '#343B3A'
    Label $e.ink ($x+290) ($y+643) 25 '#626C69' -Number
    Label $names[$i] $x ($y+695) 28 '#626C69'
  }
  Rect 72 1840 1392 2 '#D2CCC1'
  Label '07' 72 1886 29 '#626C69' -Number
  Label '由你根据文物素材判断' 132 1876 38 '#343B3A'
  Label '优先选取与文物主体色系相近的主题色' 72 1940 29 '#626C69'
  Label '回复编号或色名即可' 1138 1940 29 '#626C69'
  $pngPath = Join-Path $OutputDirectory 'theme-color-options.png'
  $bmp.Save($pngPath,[System.Drawing.Imaging.ImageFormat]::Png)
  $evidence = [ordered]@{width=1536;height=2048;aspect='3:4';font='华文楷体 (STKaiti), rendered in PNG';number_font='Georgia';examples_used=6;source_images_unchanged=$true;output_png_sha256=(Get-FileHash -LiteralPath $pngPath).Hash}
  [System.IO.File]::WriteAllText((Join-Path $OutputDirectory 'theme-color-options-build-info.json'),($evidence|ConvertTo-Json),[System.Text.UTF8Encoding]::new($false))
  $evidence | ConvertTo-Json
} finally { $g.Dispose();$bmp.Dispose();$fontFamily.Dispose();$numberFamily.Dispose() }
