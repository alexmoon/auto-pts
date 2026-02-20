#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2025, Tactile Engineering.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#

import logging

from autopts.ptsprojects.iutctl import IutCtl

log = logging.debug
TROUBLE = None
CLI_SUPPORT = ['tty']


class TrouBLECtl(IutCtl):
    """TrouBLE IUT Control Class"""

    def __init__(self, args):
        super().__init__(args)
        self._rtt_logger_name = 'defmt'


def get_iut():
    return TROUBLE


def init(args):
    """IUT init routine

    tty_file -- Path to TTY file. BTP communication with HW DUT will be done
    over this TTY.
    board -- HW DUT board to use for testing.
    """
    global TROUBLE

    TROUBLE = TrouBLECtl(args)


def cleanup():
    """IUT cleanup routine"""
    global TROUBLE

    if TROUBLE:
        TROUBLE.stop()
        TROUBLE = None
