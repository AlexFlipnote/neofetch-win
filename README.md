# neofetch-win
neofetch, but for Windows

This was made to have the command [neofetch](https://github.com/dylanaraps/neofetch) available on the Windows CMD.
If you wish to contribute, feel free to do so.

## Requirement
- Python 3.6 or up

## Install
- Open CMD as admin
- Type the following command: `pip install neofetch-win`
- Now you can type `neofetch` in CMD to see results

### Available colours
Black, red, green, yellow, blue, magenta, cyan, white

### Using ASCII art
1. File has to be readable
2. When targeting file from different path, replace `\` with `\\` in order for Windows to understand it
3. Magic happens, yey

# Usage
```
$ neofetch --help
usage:  [-h] [-v] [-c COLOUR [COLOUR ...]] [-ac ARTCOLOUR [ARTCOLOUR ...]]
        [-a ART [ART ...]] [-na]

neofetch, but for Windows

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show the version number and exit
  -c COLOUR [COLOUR ...], --colour COLOUR [COLOUR ...]
                        Change colour of the text
  -ac ARTCOLOUR [ARTCOLOUR ...], --artcolour ARTCOLOUR [ARTCOLOUR ...]
                        Change colour of the ascii
  -a ART [ART ...], --art ART [ART ...]
                        Change the ascii art
  -na, --noart          Turn off ascii art
```
