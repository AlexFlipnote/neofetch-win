import argparse
import sys


class Arguments(argparse.ArgumentParser):
    def error(self, message):
        raise RuntimeError(message)


def getarg():
    args = sys.argv
    args[0] = ""
    return " ".join(args)
