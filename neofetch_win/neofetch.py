import colorama
import getpass
import psutil
import shutil
import socket
import sys
import time
import wmi

from . import art


class Neofetch:
    def __init__(self, art: str = None, display_art: bool = True, colour: str = "cyan", art_colour: str = None):
        self.spacing = 0
        self.art = art
        self.display_art = display_art

        self.wmi = wmi.WMI()
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
            if colour.lower() in clist:
                return colorama.Fore.__getattribute__(colour.upper())
            else:
                possible_colours = ", ".join(clist)
                print(f"Possible colours: {possible_colours}")
                return colorama.Fore.RESET
        else:
            return colorama.Fore.RESET

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
        try:
            get_os = self.wmi.instances("win32_operatingsystem")[0].wmi_property("Name").value
            return get_os.split("|")[0]
        except Exception:
            return "Unknown windows?"

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
        """ Obtains the current GPUs in use """
        try:
            return [x.wmi_property("Name").value for x in self.wmi.instances("Win32_VideoController")]
        except Exception:
            return "Unknown GPU"

    @property
    def cpu(self):
        """ Get the current CPU you got """
        try:
            return self.wmi.instances("Win32_Processor")[0].wmi_property("Name").value
        except Exception:
            return "Not found...??"

    @property
    def motherboard(self):
        """ Find the current motherboard you got """
        try:
            data = self.wmi.instances("win32_baseboard")[0]
            product = data.wmi_property("Product").value
            facture = data.wmi_property("Manufacturer").value
            return f"{facture} {product}"
        except Exception:
            return "Not found...??"

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

        more_disk = self.partitions[1:] if self.partitions[1:] else None

        components_list = [
            ("os", f"{self.colourize('OS')}: {self.os}"),
            ("uptime", f"{self.colourize('Uptime')}: {self.uptime}"),
            ("ip", f"{self.colourize('Local IP')}: {self.local_ip}"),
            ("motherboard", f"{self.colourize('Motherboard')}: {self.motherboard}"),
            ("cpu", f"{self.colourize('CPU')}: {self.cpu}"),
            *[("gpu", f"{self.colourize('GPU')}: {x}") for x in self.gpu],
            ("ram", f"{self.colourize('Memory')}: {self.ram}"),
            ("disk", f"{self.colourize('Disk')}: {self.partitions[0].strip()}")
        ]

        for name, info in components_list:
            if name not in ignore_list:
                components.append(info)
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
