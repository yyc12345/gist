# fake-watermark

给照片打上一个"假"相机水印的小工具。它在原图底部拼接一个横条，显示相机品牌、型号、拍摄时间、焦距、光圈、曝光时间与 ISO，并把同样的信息写进照片的 EXIF 元数据中。

## 功能

- 使用 PIL 在图像底部添加白色横条，左侧贴 logo，右侧显示相机参数文本。
- 使用 pydantic + tomllib 校验并读取 TOML 格式的 manifest 配置。
- 使用内置 `argparse` 处理命令行参数。
- 使用 `exiftool` 先清空照片全部 EXIF，再写入水印对应的相机参数。

## 环境要求

- Python 3.13+
- 已安装 `pillow`、`pydantic`（见 `pyproject.toml`）
- 系统可调用 `exiftool` 命令（[ExifTool 官网](https://exiftool.org/)），或通过环境变量指定其路径

## 使用方式

先准备一个 manifest 配置文件（可参考仓库内的 `manifest.toml`）：

```bash
python main.py \
  -m manifest.toml \
  -i photo.jpg \
  -o watermarked.jpg
```

参数说明：

| 参数 | 必选 | 说明 |
| ---- | ---- | ---- |
| `-m, --manifest` | 是 | watermark 配置文件的路径（TOML） |
| `-i, --input` | 是 | 输入的原图路径 |
| `-o, --output` | 是 | 输出水印图的路径 |

处理流程：读取并校验 manifest → 在底部添加水印横条 → 用 exiftool 清空 EXIF → 写入相机水印数据。

## Manifest 配置

参见示例文件：`manifest.toml`

## 环境变量

| 环境变量 | 说明 |
| -------- | ---- |
| `FAKE_WATERMARK_EXIFTOOL_BIN` | 覆盖 exiftool 的可执行文件路径。默认使用 PATH 中的 `exiftool` |
