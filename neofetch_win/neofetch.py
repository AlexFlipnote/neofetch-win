import getpass
import psutil
import shutil
import socket
import time

from platform import release
from unicodedata import east_asian_width
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

    windows_10_blue = "\x1b[38;2;0;192;225m"
    windows_11_blue = "\x1b[38;2;0;120;212m"


class Neofetch:
    def __init__(
        self,
        art: str | None = None,
        display_art: bool = True,
        colour: str = "cyan",
        art_colour: str | None = None,
        only_ascii: bool = False,
        stdout: bool = False,
    ):
        self.wmi: _wmi_class = WMI()

        self.spacing: int = 0
        self.art = art
        self.display_art = display_art
        self.only_ascii = only_ascii

        self.stdout = stdout

        self.colour = self.colours(colour)
        self.art_colour = self.colours(art_colour)

    def readable(self, num: float, suffix: str = "B") -> str:
        """
        Convert Bytes into human readable formats.

        Parameters
        ----------
        num:
            The number to convert
        suffix:
            The suffix to use

        Returns
        -------
            The readable number
        """
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    def colourize(self, text: str) -> str:
        """
        Colourize text to a different colour.

        Parameters
        ----------
        text:
            The text to colourize

        Returns
        -------
            The colourized text
        """

        if self.stdout:
            return text

        return f"{self.colour}{text}{Ansi.reset}"

    def disk_space(self, partition: str) -> tuple[int, int, int]:
        """ Get the disk space of a given partition. """
        total, used, free = shutil.disk_usage(partition)
        return total, used, free

    def colours(self, colour: str | None = None) -> str:
        """
        Colour validator to use for printing.

        Parameters
        ----------
        colour:
            The colour to validate

        Returns
        -------
            The validated colour
        """
        clist = [
            "black", "red", "green", "yellow",
            "blue", "magenta", "cyan", "white",
            "windows_10_blue", "windows_11_blue"
        ]

        if colour:
            if colour.lower() not in clist:
                possible_colours = ", ".join(clist)
                print(f"Possible colours: {possible_colours}")
                return Ansi.reset

            return getattr(Ansi, colour.lower(), Ansi.reset)

        return Ansi.reset

    def get_str_width(self, text: str) -> int:
        """
        Calculate the display width of a string.

        Parameters
        ----------
        text:
            The text to calculate the width of

        Returns
        -------
            The width of the text
        """
        length = 0
        for c in text:
            if east_asian_width(c) in "FWA":
                length += 2
            else:
                length += 1
        return length

    def get_art(self) -> list[str]:
        """ Get a .txt art file. """
        system_version = release()
        try:
            ascii_art = (
                getattr(art, f"windows_{system_version}")
                if system_version in ["10", "11"] else
                art.windows_11
            )
        except AttributeError:
            ascii_art = art.windows_11

        lines = ascii_art

        if self.art:
            try:
                with open(self.art, encoding="utf-8") as f:
                    lines = f.read().splitlines()
            except FileNotFoundError:
                lines = ascii_art

        longest = sorted(lines, key=len, reverse=True)
        self.spacing = len(longest[0])

        return lines

    @property
    def colour_blocks(self) -> tuple[str, str]:
        """ Return the colour blocks. """

        if self.stdout:
            return "", ""

        rows_1 = []
        rows_2 = []

        for i in range(30, 38):
            rows_1.append(f"\033[{i}\033[{i + 10}m   ")
        rows_1.append("\033[m")

        for i in range(8, 16):
            rows_2.append(f"\033[38;5;{i}m\033[48;5;{i}m   ")
        rows_2.append("\033[m")

        return (
            "".join(rows_1),
            "".join(rows_2)
        )

    @property
    def local_ip(self) -> str:
        """ Gets the local IP on your curent machine. """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "Not found..."

    @property
    def username(self) -> str:
        """ Get the machine username. """
        return getpass.getuser()

    @property
    def hostname(self) -> str:
        """ Gets your lovely hostname, everyone loves that. """
        return socket.gethostname()

    @property
    def os(self) -> str:
        """ Finds out what OS you're currently on. """
        data = self.wmi.query("SELECT Name FROM Win32_OperatingSystem")

        try:
            return data[0].Name.split("|")[0]
        except Exception:
            return "Unknown windows?"

    @property
    def uptime(self) -> str:
        """ Get the device uptime. """
        delta = round(time.time() - psutil.boot_time())

        hours, remainder = divmod(int(delta), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        def include_s(text: str, num: int) -> str:
            return f"{num} {text}{'' if num == 1 else 's'}"

        d = include_s("day", days)
        h = include_s("hour", hours)
        m = include_s("minute", minutes)
        s = include_s("second", seconds)

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
        """ Obtains the current GPUs in use. """
        data = self.wmi.query("SELECT Name FROM Win32_VideoController")
        if not data:
            return ["Unknown GPU"]
        return [x.Name for x in data[:10]]

    @property
    def cpu(self) -> str:
        """ Get the current CPU you got. """
        data = self.wmi.query("SELECT Name FROM Win32_Processor")
        if not data:
            return "Not found...??"
        return data[0].Name

    @property
    def motherboard(self) -> str:
        """ Find the current motherboard you got. """
        data = self.wmi.query("SELECT Manufacturer, Product FROM Win32_BaseBoard")
        if not data:
            return "Not found...??"
        return f"{data[0].Manufacturer} {data[0].Product}"

    @property
    def ram(self) -> str:
        """ Get RAM used/free/total. """
        ram = psutil.virtual_memory()
        used = self.readable(ram.used)
        total = self.readable(ram.total)

        percent_used = round(ram.used / ram.total * 100, 2)

        return f"{used} / {total} ({percent_used}%)"

    @property
    def partitions(self) -> list[str]:
        """ Find the disk partitions on current OS. """
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

    def pretty_print(self, ignore_list: list[str] | None = None) -> str:
        """
        Print everything in a lovely cmd form.

        Parameters
        ----------
        ignore_list:
            A list of components to ignore, by default []

        Returns
        -------
            The pretty printed output
        """
        ignore_list = ignore_list or []
        art = self.get_art()

        headerline = f"{self.colourize(self.username)}@{self.colourize(self.hostname)}"
        headerline_nocolour = f"{self.username}@{self.hostname}"
        underlines = "".join(["-" for _ in range(self.get_str_width(headerline_nocolour))])

        components = []

        more_disk = self.partitions[1:] or None

        gpus = self.gpu
        more_gpus = gpus[1:] or None

        colours_row_1, colours_row_2 = self.colour_blocks

        components_list: list[tuple[str, str]] = [
            ("title", headerline),
            ("underline", underlines),
            ("os", f"{self.colourize('OS')}: {self.os}"),
            ("uptime", f"{self.colourize('Uptime')}: {self.uptime}"),
            ("ip", f"{self.colourize('Local IP')}: {self.local_ip}"),
            ("motherboard", f"{self.colourize('Motherboard')}: {self.motherboard}"),
            ("cpu", f"{self.colourize('CPU')}: {self.cpu}"),
            ("gpu", f"{self.colourize('GPU')}: {self.gpu[0]}"),
            ("ram", f"{self.colourize('Memory')}: {self.ram}"),
            ("disk", f"{self.colourize('Disk')}: {self.partitions[0].strip()}"),
            ("linebreak", ""),
            ("colours_1", colours_row_1),
            ("colours_2", colours_row_2)
        ]

        for name, info in components_list:
            if(name in ignore_list) or self.only_ascii:
                continue

            components.append(info)
            if name == "disk" and more_disk:
                for g in more_disk:
                    components.append(g)

            if name == "gpu" and more_gpus:
                for g in more_gpus:
                    components.append(f"     {g}")

        build_print = []
        spacing = 6 + self.spacing

        if self.display_art:
            if len(art) > len(components):  # Prefer the bigger array to iterate over
                for index, art_line in enumerate(art):
                    line = f"{art_line:<{spacing}}"

                    if not self.stdout:
                        line = f"{Ansi.reset}{line}{Ansi.reset}"

                    if index < len(components):
                        line += components[index]

                    build_print.append(line)

            else:
                for index, component in enumerate(components):
                    line = f"{art[index]:<{spacing}}" if index < len(art) else f"{'':<{spacing}}"

                    if not self.stdout:
                        line = f"{Ansi.reset}{line}{Ansi.reset}"

                    line += component

                    build_print.append(line)

        else:
            build_print = components

        return "\n".join(build_print)
