import colorama
import getpass
import psutil
import shutil
import socket
import traceback
import sys
import time
import re

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
        if colour:
            colour = colour.lower()
            if colour == "black":
                return colorama.Fore.BLACK
            elif colour == "red":
                return colorama.Fore.RED
            elif colour == "green":
                return colorama.Fore.GREEN
            elif colour == "yellow":
                return colorama.Fore.YELLOW
            elif colour == "blue":
                return colorama.Fore.BLUE
            elif colour == "magenta":
                return colorama.Fore.MAGENTA
            elif colour == "cyan":
                return colorama.Fore.CYAN
            elif colour == "white":
                return colorama.Fore.WHITE
            else:
                possible_colours = ", ".join(clist)
                print(f"Possible colours: {possible_colours}")
                return colorama.Fore.RESET
        else:
            return colorama.Fore.RESET

    def powershell(self, command: str):
        """ Fetch the wmic command to cmd """
        try:
            p = Popen(["powershell"] + command.split(" "), stdout=PIPE)
        except FileNotFoundError as err:
            print("PowerShell command failed to run, make sure you're running the latest version of Windows possible.")
            _traceback = ''.join(traceback.format_tb(err.__traceback__))
            error = ('{1}{0}: {2}').format(type(err).__name__, _traceback, err)
            print(error)
            sys.exit(0)

        stdout, stderror = p.communicate()

        output = stdout.decode("UTF-8", "ignore")
        output = output.replace("\n", "").replace("  ", "").replace("\x00", "")  # Just to make sure...
        return output

    def get_art(self):
        """ Get a .txt art file """
        if self.art:
            try:
                lines = open(self.art, "r").read().splitlines()
            except FileNotFoundError:
                lines = art.windows_11
        else:
            lines = art.windows_11

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
        ps = self.powershell("(Get-WMIObject win32_operatingsystem).name")
        os_fullname = ps.split("|")[0].replace("Microsoft ", "")
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
        ps = self.powershell("(Get-WMIObject win32_VideoController).name")
        return ps.split("\n")

    @property
    def cpu(self):
        """ Get the current CPU you got """
        ps = self.powershell("Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property name")
        find_cpu = re.compile(r"\rname\r[-]{1,}\r(.*?)\r").search(ps)
        return find_cpu.group(1) if find_cpu else "Not found...??"

    @property
    def motherboard(self):
        """ Find the current motherboard you got """
        mboard = self.powershell("Get-WmiObject win32_baseboard | Format-List Product,Manufacturer")
        find_mboard = re.compile(r"\r\rProduct: (.*?)\rManufacturer : (.*?)\r\r\r\r").search(mboard)
        if find_mboard:
            return f"{find_mboard.group(2)} ({find_mboard.group(1)})"
        else:
            return "Unknown..."

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

    def pretty_print(self, ignore_list: list = []):
        """ Print everything in a lovely cmd form """
        art = self.get_art()

        headerline = f"{self.colourize(self.username)}@{self.colourize(self.hostname)}"
        headerline_nocolour = f"{self.username}@{self.hostname}"
        underlines = "".join(["-" for g in range(0, len(headerline_nocolour))])

        components = [headerline, underlines]

        more_gpu = self.gpu[1:] if self.gpu[1:] else None
        more_disk = self.partitions[1:] if self.partitions[1:] else None

        components_list = [
            ("os", f"{self.colourize('OS')}: {self.os}"),
            ("uptime", f"{self.colourize('Uptime')}: {self.uptime}"),
            ("ip", f"{self.colourize('Local IP')}: {self.local_ip}"),
            ("motherboard", f"{self.colourize('Motherboard')}: {self.motherboard}"),
            ("cpu", f"{self.colourize('CPU')}: {self.cpu}"),
            ("gpu", f"{self.colourize('GPU')}: {self.gpu[0].strip()}"),
            ("ram", f"{self.colourize('Memory')}: {self.ram}"),
            ("disk", f"{self.colourize('Disk')}: {self.partitions[0].strip()}")
        ]

        for name, info in components_list:
            if name not in ignore_list:
                components.append(info)
                if name == "gpu" and more_gpu:
                    for g in more_gpu:
                        components.append(g)
                if name == "disk" and more_disk:
                    for g in more_disk:
                        components.append(g)

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
