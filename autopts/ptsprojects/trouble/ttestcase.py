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

"""Test case that manages TrouBLE IUT"""

from autopts.ptsprojects.stack import get_stack
from autopts.ptsprojects.testcase import TestCaseLT1, TestFunc, TestFuncCleanUp
from autopts.ptsprojects.trouble.iutctl import get_iut


class TTestCase(TestCaseLT1):
    """A TrouBLE test case that uses HW as DUT"""

    def __init__(self, *args, **kwargs):
        """Refer to TestCase.__init__ for parameters and their documentation"""

        super().__init__(*args, ptsproject_name="trouble", **kwargs)

        self.stack = get_stack()
        self.troublectl = get_iut()

        # Init stack.core to be able to receive IUT ready event
        self.cmds.insert(0, TestFunc(self.stack.core_init))
        # Open BTP socket and start IUT
        self.cmds.insert(1, TestFunc(self.troublectl.start, self))
        # Await IUT ready event
        self.cmds.insert(2, TestFunc(self.troublectl.wait_iut_ready_event, False))

        self.cmds.append(TestFuncCleanUp(self.stack.cleanup))

        # Last command is to stop HW.
        # This will trigger the HW reset and the IUT ready event.
        # The event will be used in the next test case, to skip double reset.
        self.cmds.append(TestFuncCleanUp(self.troublectl.stop))
