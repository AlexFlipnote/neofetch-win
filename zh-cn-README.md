# neofetch-win
这是neofetch，但是为windows而写的。

#### | [ENGLISH](./README.md) | 简体中文 |

![PreviewImage](https://i.alexflipnote.dev/vfgQo1y.png)

这是为了使[Neofetch](https://github.com/dylanaraps/neofetch)在Windows上的CMD上可用。如果您愿意捐款，请随时捐款。
##### 译者提示：在Git Bash可能会出现错误，请尽量在Windows上的CMD或Powershell上使用。

## 警告！
**您的IP地址一般情况下不应该出现在截图中，如果想隐藏IP地址，请使用`--ignore`参数！（详细见[issues#14](https://github.com/AlexFlipnote/neofetch-win/issues/14)）**

## 安装需求
- Python 3.6或更高版本。

## 安装
- 使用管理员权限打开CMD。
- 输入以下命令：`pip install neofetch-win`。
- 现在你可以在CMD输入`neofetch`来查看结果。

### 可用的颜色
黑色，红色，绿色，黄色，蓝色，洋红色，青色，白色。(black,red, green, yellow, blue, magenta, cyan, white)
#### 译者提示：当然，您必须使用英语输入。

### 使用其他字符艺术文件
1. 文件可读。
2. 从不同路径使用文件时，请用\\替换`\`以使Windows理解它为`\`，而不是特殊字符
<br>**注意:** 记住使用完全路径, 例子：`neofetch --art C:\\Users\\AlexFlipnote\\art.txt`
3. Magic happens, yey

# 用法
```
$ neofetch --help
usage:  [-h] [-v] [-c COLOUR [COLOUR ...]] [-ac ARTCOLOUR [ARTCOLOUR ...]]
        [-a ART [ART ...]] [-na] [--ignore]

neofetch, but for Windows

optional arguments:
  -h, --help            显示帮助信息和退出
  -v, --version         显示版本号和退出
  -c COLOUR [COLOUR ...], --colour COLOUR [COLOUR ...]
                        修改文本颜色
  -ac ARTCOLOUR [ARTCOLOUR ...], --artcolour ARTCOLOUR [ARTCOLOUR ...]
                        修改ASCII文本颜色
  -a ART [ART ...], --art ART [ART ...]
                        更改ASCII艺术文件
  -na, --noart          关闭ASCII艺术文件
  --ignore              不显示IP地址
```
