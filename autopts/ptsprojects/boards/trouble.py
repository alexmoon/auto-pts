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

from autopts.ptsprojects.boards import pylink_reset
from autopts.rtt import RTT

log = logging.debug

supported_projects = ['trouble']


def reset_cmd(iutctl):
    """Return reset callable for TrouBLE DUT

    Uses the shared RTT JLink instance when RTT logging is active,
    otherwise falls back to opening a temporary JLink connection.
    """

    def reset():
        if RTT.jlink and RTT.jlink.connected():
            log('Resetting via shared RTT JLink instance')
            RTT.jlink.reset(ms=0, halt=False)
        else:
            pylink_reset(iutctl.debugger_snr, iutctl.device_core)

    return reset
