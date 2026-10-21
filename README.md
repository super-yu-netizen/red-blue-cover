# 红蓝主题封面 · red-blue-cover

把主题或口播稿，变成真人出镜、红蓝光影、粗体大字与具体道具组成的视频封面。

你给内容，AI负责提炼标题、从已授权照片中选图、设计动作和构图、生成图片并检查。默认横版4:3、竖版3:4，也能按当次要求改比例。

## 示例

| 横版4:3 | 竖版3:4 |
| --- | --- |
| ![横版虚构人物示例](assets/style-landscape-4x3.png) | ![竖版虚构人物示例](assets/style-portrait-3x4.png) |

示例人物均为AI虚构，不是作者或真实使用者。样图只说明视觉语言；实际封面使用你自己提供或已授权的照片。

## 安装到Codex

将仓库克隆到你的Skills目录：

```bash
git clone https://github.com/super-yu-netizen/red-blue-cover.git ~/.codex/skills/red-blue-cover
```

如果该目录已有同名Skill，先保留已有版本，另选目录查看，不直接覆盖。也可以下载[Release安装包](https://github.com/super-yu-netizen/red-blue-cover/releases/latest)，解压后把其中的 `red-blue-cover` 文件夹放进Skills目录。在新对话中使用。

这是Skill指令与辅助脚本包，需要宿主提供图像生成能力；它不是独立生图软件，也不包含生图模型、API额度或个人照片。

## 调用

```text
使用 $red-blue-cover，做一张横版封面。
口播稿如下：……
人物照片使用我已经提供的图片。
```

```text
使用 $red-blue-cover，做一套横版和竖版封面。
主题：……
照片库：我已授权的本地照片文件夹。
```

```text
使用 $red-blue-cover，把这张封面的标题改为“新的准确标题”。
保留其他内容。
```

通常无需指定字体、颜色或照片编号。已给准确文案时逐字执行；只有必要信息无法自行解决时才提问。不要把仓库样图中的脸当成自己。

## 包含什么

- `SKILL.md`：制作、参考、横竖构图、修改和验收规则。
- `references/prompts.md`：新封面与局部编辑提示词。
- `assets/`：两张虚构人物风格样图与来源说明。
- `agents/openai.yaml`：Codex显示名称与调用示例。
- `scripts/cover_utils.py`：本地照片联系表、比例检查和QA缩略图。
- `tests/`：脚本行为检查。

仅使用指令与宿主图像工具时不要求安装Python依赖。需要辅助脚本时，在本仓库目录运行：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/cover_utils.py photos --library ./photos --exclude "do-not-use.jpg"
python3 scripts/cover_utils.py check ./output/cover.png --aspect 4:3 --review-dir ./review
python3 -m unittest discover -s tests -v
```

`photos`也可读取环境变量 `RED_BLUE_COVER_PHOTOS`。没有配置时要求明确照片库，不搜索整台电脑。默认缓存写到用户本机 `~/.cache/red-blue-cover/photos`；不联网、不上传图片。`--exclude`可重复，支持文件名通配符。被撤回授权的照片还应从当前可选库移除或按项目规则排除。

`check`不改变源图片像素，不自动裁切、拉伸或修复；退出码0为成功，1为比例不符，2为输入或读取错误。HEIC等未列为支持的格式，请先在本机另存为PNG/JPEG后使用。

## 来源与边界

本系列来自真实封面制作过程中的构图与检查经验。风格调研参考过[Oh My Cover Design](https://github.com/hongfamonvAI/oh-my-cover-design)；本包没有复制分发该项目文件、第三方截图或个人照片。公开版的指令、通用脚本和虚构人物示例在此单独整理。

公开仓库没有附加开源许可证；公开可见不等于另行授予开源许可。个人照片授权、第三方产品素材权利和对外发布范围，应以各使用者当前获得的授权为准。一次示例成功不代表每次生成零返工。

