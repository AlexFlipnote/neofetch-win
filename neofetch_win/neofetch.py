import getpass
import psutil
import shutil
import socket
import time

from typing import Optional
from wmi import WMI, _wmi_class

from . import art


class Ansi:
    reset = "\x1b[0m"

    blue = "\x1b[38;5;39m"
    cyan = "\x1b[38;5;51m"
    green = "\x1b[38;5;40m"
    grey = "\x1b[38;5;240m"
    magenta = "\x1b[38;5;201m"
    red = "\x1b[38;5;196m"
    white = "\x1b[38;21m"
    yellow = "\x1b[38;5;226m"


class Neofetch:
    def __init__(
        self,
        art: Optional[str] = None,
        display_art: bool = True,
        colour: str = "cyan",
        art_colour: Optional[str] = None
    ):
        self.wmi: _wmi_class = WMI()

        self.spacing: int = 0
        self.art = art
        self.display_art = display_art

        self.colour = self.colours(colour)
        self.art_colour = self.colours(art_colour)

    def get_property(
        self,
        class_name: str,
        *properties: str,
        limit: int = 1
    ) -> tuple[str, ...]:
        """ Generic method to fetch a property from a given WMI class """
        temp = []

        for i, x in enumerate(
            self.wmi.instances(class_name),  # type: ignore
            start=1
        ):
            if i > limit:
                break

            for prop in properties:
                try:
                    temp.append(x.wmi_property(prop).value)
                except Exception as e:
                    temp.append(f"Error fetching {prop} from {class_name}: {str(e)}")

        return tuple(temp)

    def readable(self, num: float, suffix: str = "B") -> str:
        """ Convert Bytes into human readable formats """
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, "Yi", suffix)

    def colourize(self, text: str) -> str:
        """ Colourize text to a different colour """
        template = f"{self.colour}{text}{Ansi.reset}"
        return template

    def disk_space(self, partition: str) -> tuple:
        total, used, free = shutil.disk_usage(partition)
        return total, used, free

    def colours(self, colour: Optional[str] = None) -> str:
        """ Colour validator """
        clist = [
            "black", "red", "green", "yellow",
            "blue", "magenta", "cyan", "white"
        ]

        if colour:
            if colour.lower() not in clist:
                possible_colours = ", ".join(clist)
                print(f"Possible colours: {possible_colours}")
                return Ansi.reset

            return getattr(Ansi, colour.lower(), Ansi.reset)

        return Ansi.reset

    def get_art(self) -> list[str]:
        """ Get a .txt art file """
        lines = art.windows_11

        if self.art:
            try:
                with open(self.art, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
            except FileNotFoundError:
                lines = art.windows_11

        longest = sorted(lines, key=len, reverse=True)
        self.spacing = len(longest[0])

        return lines

    @property
    def local_ip(self) -> str:
        """ Gets the local IP on your curent machine """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            getip = s.getsockname()[0]
            return getip
        except Exception:
            return "Not found..."

    @property
    def username(self) -> str:
        """ Get the machine username """
        name = getpass.getuser()
        return name

    @property
    def hostname(self) -> str:
        """ Gets your lovely hostname, everyone loves that """
        name = socket.gethostname()
        return name

    @property
    def os(self) -> str:
        """ Finds out what OS you're currently on """
        try:
            (get_os,) = self.get_property("win32_operatingsystem", "Name")
            return get_os.split("|")[0]
        except Exception:
            return "Unknown windows?"

    @property
    def uptime(self) -> str:
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
    def gpu(self) -> list[str]:
        """ Obtains the current GPUs in use """
        try:
            return list(
                self.get_property(
                    "Win32_VideoController", "Name",
                    limit=10
                )
            )
        except Exception:
            return ["Unknown GPU"]

    @property
    def cpu(self) -> str:
        """ Get the current CPU you got """
        try:
            (cpu_name,) = self.get_property("Win32_Processor", "Name")
            return cpu_name
        except Exception:
            return "Not found...??"

    @property
    def motherboard(self) -> str:
        """ Find the current motherboard you got """
        try:
            product, facture = self.get_property(
                "Win32_BaseBoard",
                "Product", "Manufacturer"
            )

            return f"{facture} {product}"
        except Exception:
            return "Not found...??"

    @property
    def ram(self) -> str:
        """ Get RAM used/free/total """
        ram = psutil.virtual_memory()
        used = self.readable(ram.used)
        total = self.readable(ram.total)

        percent_used = round(ram.used / ram.total * 100, 2)

        return f"{used} / {total} ({percent_used}%)"

    @property
    def partitions(self) -> list[str]:
        """ Find the disk partitions on current OS """
        parts = psutil.disk_partitions()
        listparts = []

        for g in parts:
            try:
                total, used, _ = self.disk_space(g.device)
                percent_used = round(used / total * 100, 2)
                listparts.append(
                    f"      {g.device[:2]} {self.readable(used)} / "
                    f"{self.readable(total)} ({percent_used}%)"
                )
            except PermissionError:
                continue

        return listparts

    def pretty_print(self, ignore_list: list = []) -> str:
        """ Print everything in a lovely cmd form """
        art = self.get_art()

        headerline = f"{self.colourize(self.username)}@{self.colourize(self.hostname)}"
        headerline_nocolour = f"{self.username}@{self.hostname}"
        underlines = "".join(["-" for g in range(0, len(headerline_nocolour))])

        components = [headerline, underlines]

        more_disk = self.partitions[1:] if self.partitions[1:] else None

        components_list: list[tuple[str, str]] = [
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
            if name in ignore_list:
                continue

            components.append(info)
            if name == "disk" and more_disk:
                for g in more_disk:
                    components.append(g)

        build_print = []
        spacing = 6 + self.spacing

        if self.display_art:
            if len(art) > len(components):  # Prefer the bigger array to iterate over
                for index, art_line in enumerate(art):
                    line = f"{self.art_colour}{art_line:<{spacing}}{Ansi.reset}"

                    if index < len(components):
                        line += components[index]

                    build_print.append(line)
            else:
                for index, component in enumerate(components):
                    if index < len(art):
                        line = f"{self.art_colour}{art[index]:<{spacing}}{Ansi.reset}"
                    else:
                        line = f"{'':<{spacing}}"

                    line += component

                    build_print.append(line)
        else:
            build_print = components

        return "\n".join(build_print)
