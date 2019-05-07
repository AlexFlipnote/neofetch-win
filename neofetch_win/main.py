import shlex
import neofetch_win
import sys

from . import argpar, neofetch


def shell():
    arguments = argpar.getarg()
    parser = argpar.Arguments(description="neofetch, but for Windows")
    parser.add_argument('-v', '--version', action='store_true', help='Show the version number and exit')
    parser.add_argument('-c', '--colour', nargs='+', help='Change colour of the text', default=None)
    parser.add_argument('-ac', '--artcolour', nargs='+', help='Change colour of the ascii', default=None)
    parser.add_argument('-a', '--art', nargs='+', help='Change the ascii art', default=None)
    parser.add_argument('-na', '--noart', action='store_true', help='Turn off ascii art')

    try:
        args = parser.parse_args(shlex.split(arguments))
    except Exception as e:
        print(e)
        sys.exit(0)

    if args.version:
        print(neofetch_win.__version__)
        sys.exit(0)

    if args.noart:
        display_art = False
    else:
        display_art = True

    if args.art:
        art = ' '.join(args.art)
    else:
        art = None

    if args.colour:
        colour = ' '.join(args.colour)
    else:
        colour = "cyan"

    if args.artcolour:
        artcolour = ' '.join(args.artcolour)
    else:
        artcolour = "cyan"

    nf = neofetch.Neofetch(
        colour=colour,
        art_colour=artcolour,
        art=art,
        display_art=display_art
    )

    print(nf.pretty_print(), file=nf.stream)


def main():
    try:
        shell()
    except KeyboardInterrupt:
        print('\nCancelling...')


if __name__ == '__main__':
    main()
