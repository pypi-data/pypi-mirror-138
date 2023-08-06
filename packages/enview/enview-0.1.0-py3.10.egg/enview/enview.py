#!/home/chivier/Projects/enview/env/bin/python
# -*- coding:utf-8 -*-

import sys
from nubia import Nubia, Options
import enviewcmd.commands


def main():
    shell = Nubia(
        name="enview",
        command_pkgs=enviewcmd.commands,
        options=Options(
            persistent_history=False, auto_execute_single_suggestions=False
        )
    )
    sys.exit(shell.run())
