import colorama
import getpass
import psutil
import shutil
import socket
import sys
import time

from . import art
from subprocess import Popen, PIPE


class Neofetch:
    def __init__(self, art: str = None, display_art: bool = True, colour: str = "cyan", art_colour: str = None):
        self.spacing = 0
        self.art = art
        self.display_art = display_art

        self.colour = self.colours(colour)
        self.art_colour = self.colours(art_colour)

        self.bright = colorama.Style.BRIGHT
        self.resetc = colorama.Style.RESET_ALL

        self.stream = colorama.AnsiToWin32(sys.stdout).stream
        colorama.init(wrap=False)

    def readable(self, num, suffix='B'):
        """ Convert Bytes into human readable formats """
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def colourize(self, text: str):
        """ Colourize text to a different colour """
        template = f"{self.bright}{self.colour}{text}{self.resetc}"
        return template

    def disk_space(self, partition: str):
        total, used, free = shutil.disk_usage(partition)
        return total, used, free

    def colours(self, colour: str = None):
        """ Colour validator """
        clist = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        if colour and colour in clist:
            if colour.lower() == "black":
                return colorama.Fore.BLACK
            elif colour.lower() == "red":
                return colorama.Fore.RED
            elif colour.lower() == "green":
                return colorama.Fore.GREEN
            elif colour.lower() == "yellow":
                return colorama.Fore.YELLOW
            elif colour.lower() == "blue":
                return colorama.Fore.BLUE
            elif colour.lower() == "magenta":
                return colorama.Fore.MAGENTA
            elif colour.lower() == "cyan":
                return colorama.Fore.CYAN
            elif colour.lower() == "white":
                return colorama.Fore.WHITE
            else:
                return colorama.Fore.RESET
        else:
            return colorama.Fore.RESET

    def wmic(self, command: str):
        """ Fetch the wmic command to cmd """
        p = Popen(command.split(" "), stdout=PIPE)
        stdout, stderror = p.communicate()

        output = stdout.decode("UTF-8", "ignore")
        lines = output.split("\r\r")
        lines = [g.replace("\n", "").replace("  ", "") for g in lines if len(g) > 2]
        return lines

    def get_art(self):
        """ Get a .txt art file """
        if self.art:
            try:
                lines = open(self.art, "r").read().splitlines()
            except FileNotFoundError:
                lines = art.default_art
        else:
            lines = art.default_art

        longest = sorted(lines, key=len, reverse=True)
        self.spacing = len(longest[0])

        return lines

    @property
    def local_ip(self):
        """ Gets the local IP on your curent machine """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            getip = s.getsockname()[0]
            return getip
        except Exception:
            return "Not found..."

    @property
    def username(self):
        """ Get the machine username """
        name = getpass.getuser()
        return name

    @property
    def hostname(self):
        """ Gets your lovely hostname, everyone loves that """
        name = socket.gethostname()
        return name

    @property
    def os(self):
        """ Finds out what OS you're currently on """
        lines = self.wmic("wmic os get Caption")
        os_fullname = lines[-1].replace("Microsoft ", "")
        return os_fullname

    @property
    def uptime(self):
        """ Get the device uptime """
        delta = round(time.time() - psutil.boot_time())

        hours, remainder = divmod(int(delta), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        def includeS(text: str, num: int):
            return f"{num} {text}{'' if num == 1 else 's'}"

        d = includeS("day", days)
        h = includeS("hour", hours)
        m = includeS("minute", minutes)
        s = includeS("second", seconds)

        if days:
            output = f"{d}, {h}, {m} and {s}"
        elif hours:
            output = f"{h}, {m} and {s}"
        elif minutes:
            output = f"{m} and {s}"
        else:
            output = s

        return output

    @property
    def gpu(self):
        """ Get the current GPU you got """
        lines = self.wmic("wmic path win32_VideoController get name")
        return [f'     {gpu.strip()}' for gpu in lines[1:]]

    @property
    def cpu(self):
        """ Get the current CPU you got """
        lines = self.wmic("wmic cpu get name")
        return lines[-1]

    @property
    def motherboard(self):
        """ Find the current motherboard you got """
        mboard_name = self.wmic("wmic baseboard get Manufacturer")
        mboard_module = self.wmic("wmic baseboard get product")
        return f"{mboard_name[-1]} ({mboard_module[-1]})"

    @property
    def ram(self):
        """ Get RAM used/free/total """
        ram = psutil.virtual_memory()
        used = self.readable(ram.used)
        total = self.readable(ram.total)

        percent_used = round(ram.used / ram.total * 100, 2)

        return f"{used} / {total} ({percent_used}%)"

    @property
    def partitions(self):
        """ Find the disk partitions on current OS """
        parts = psutil.disk_partitions()
        listparts = []

        for g in parts:
            try:
                total, used, free = self.disk_space(g.device)
                percent_used = round(used / total * 100, 2)
                listparts.append(f"      {g.device[:2]} {self.readable(used)} / {self.readable(total)} ({percent_used}%)")
            except PermissionError:
                continue

        return listparts

    def pretty_print(self):
        """ Print everything in a lovely cmd form """
        art = self.get_art()

        headerline = f"{self.colourize(self.username)}@{self.colourize(self.hostname)}"
        headerline_nocolour = f"{self.username}@{self.hostname}"
        underlines = "".join(["-" for g in range(0, len(headerline_nocolour))])

        components = [
            headerline, underlines,
            f"{self.colourize('OS')}: {self.os}",
            f"{self.colourize('Uptime')}: {self.uptime}",
            f"{self.colourize('Local IP')}: {self.local_ip}",
            f"{self.colourize('Motherboard')}: {self.motherboard}",
            f"{self.colourize('CPU')}: {self.cpu}",
            f"{self.colourize('GPU')}: {self.gpu[0].strip()}",
            *self.gpu[1:],
            f"{self.colourize('Memory')}: {self.ram}",
            f"{self.colourize('Disk')}: {self.partitions[0].strip()}",
            *self.partitions[1:]
        ]

        build_print = []
        spacing = 6 + self.spacing

        if self.display_art:
            if len(art) > len(components):  # Prefer the bigger array to iterate over
                for index, art_line in enumerate(art):
                    line = f'{self.bright}{self.art_colour}{art_line:<{spacing}}{self.resetc}'

                    if index < len(components):
                        line += components[index]

                    build_print.append(line)
            else:
                for index, component in enumerate(components):
                    if index < len(art):
                        line = f'{self.bright}{self.art_colour}{art[index]:<{spacing}}{self.resetc}'
                    else:
                        line = f'{"":<{spacing}}'

                    line += component

                    build_print.append(line)
        else:
            build_print = components

        return "\n".join(build_print)
