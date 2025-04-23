import sys

from platform import release
from argparse import ArgumentParser

from . import __version__, Neofetch


def shell():
    parser = ArgumentParser(description="neofetch, but for Windows")

    parser.add_argument(
        "-v", "--version",
        help="Show the version number and exit",
        action="store_true"
    )

    parser.add_argument(
        "-c", "--colour", "--color",
        help="Change colour of the text",
        nargs="+",
        default=None
    )

    parser.add_argument(
        "-ac", "--artcolour", "--artcolor",
        help="Change colour of the ascii",
        nargs="+",
        default=None
    )

    parser.add_argument(
        "-a", "--art",
        help="Change the ascii art",
        nargs="+",
        default=None
    )

    parser.add_argument(
        "-na", "--noart",
        help="Turn off ascii art",
        action="store_true"
    )

    parser.add_argument(
        "-i", "--ignore",
        help="Ignore components (os, uptime, ip, motherboard, cpu, gpu, ram, disk)",
        nargs="+",
        default=[]
    )

    args = parser.parse_args()

    if args.version:
        print(f"neofetch-win v{__version__}")
        sys.exit(0)

    # Default values
    display_art = True
    art = None

    # Check system version and set default colours
    system_version = release()

    if system_version in ["10", "11"]:
        colour = f"windows_{system_version}_blue"
        artcolour = f"windows_{system_version}_blue"
    else:
        colour = "cyan"
        artcolour = "cyan"

    if args.noart:
        display_art = False

    if args.art:
        art = " ".join(args.art)

    if args.colour:
        colour = " ".join(args.colour)

    if args.artcolour:
        artcolour = " ".join(args.artcolour)

    nf = Neofetch(
        colour=colour,
        art_colour=artcolour,
        art=art,
        display_art=display_art,
    )

    print(
        nf.pretty_print(ignore_list=args.ignore)
    )


def main():
    try:
        shell()
    except KeyboardInterrupt:
        print("\nCancelling...")


if __name__ == "__main__":
    main()
