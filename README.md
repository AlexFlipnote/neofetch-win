# neofetch_win
neofetch, but for Windows

![PreviewImage](https://i.alexflipnote.dev/vfgQo1y.png)

This was made to have the command [neofetch](https://github.com/dylanaraps/neofetch) available on the Windows CMD.
If you wish to contribute, feel free to do so.

## Requirement
- Python 3.11 or up

## Install
- Open CMD as admin
- Type the following command: `pip install neofetch-win`
- Now you can type `neofetch` in CMD to see results

### Available colours
black, red, green, yellow, blue, magenta, cyan, white, windows_10_blue, windows_11_blue

### Using ASCII art
1. File has to be readable
2. When targeting file from different path, replace `\` with `\\` in order for Windows to understand it
<br>**NOTE:** Remember to use entire path, example: `neofetch --art C:\\Users\\AlexFlipnote\\art.txt`
3. Magic happens, yey

# Usage
```
$ neofetch --help
usage:  [-h] [-v] [-c COLOUR [COLOUR ...]] [-l] [--stdout] [-ac ARTCOLOUR [ARTCOLOUR ...]]
                   [-a ART [ART ...]] [-na] [-i IGNORE [IGNORE ...]]

neofetch, but for Windows

options:
  -h, --help            show this help message and exit
  -v, --version         Show the version number and exit
  -c COLOUR [COLOUR ...], --colour COLOUR [COLOUR ...], --color COLOUR [COLOUR ...]
                        Change colour of the text
  -l, --logo            Hide the info text and only show the ascii logo
  --stdout              Turn off all colors
  -ac ARTCOLOUR [ARTCOLOUR ...], --artcolour ARTCOLOUR [ARTCOLOUR ...], --artcolor ARTCOLOUR [ARTCOLOUR ...]
                        Change colour of the ascii
  -a ART [ART ...], --art ART [ART ...]
                        Change the ascii art
  -na, --noart          Turn off ascii art
  -i IGNORE [IGNORE ...], --ignore IGNORE [IGNORE ...]
                        Ignore components (title, underline, os, uptime, ip, motherboard, cpu, gpu, ram, disk,
                        linebreak, colours_1, colours_2)
```
