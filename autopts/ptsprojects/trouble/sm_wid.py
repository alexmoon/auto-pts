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

from autopts.ptsprojects.trouble.iutctl import get_iut
from autopts.pybtp import btp
from autopts.wid import generic_wid_hdl
from autopts.pybtp.types import WIDParams

log = logging.debug


def sm_wid_hdl(wid, description, test_case_name):
    log(f'{sm_wid_hdl.__name__}, {wid}, {description}, {test_case_name}')
    return generic_wid_hdl(wid, description, test_case_name, [__name__, 'autopts.wid.sm'])


# wid handlers section begin
def hdl_wid_108(params: WIDParams):
    """Please start pairing process."""

    # SM/CEN/JW/BV-01-C: AuthReq Bonding Flags set to '00' and the MITM flag set to '0'
    if params.test_case_name in ['SM/CEN/JW/BV-01-C', 'SM/CEN/JW/BI-06-C']:
        btp.gap_set_bondable_off()
        btp.gap_set_mitm_off()

    # SM/CEN/SCOB/BV-04-C: OOB pairing requires MITM flag set to '0'
    if params.test_case_name in ['SM/CEN/SCOB/BV-04-C']:
        btp.gap_set_mitm_off()

    btp.gap_pair()
    return True


def hdl_wid_143(_):
    """Confirm IUT readiness and read controller information."""
    troublectl = get_iut()

    troublectl.wait_iut_ready_event()
    btp.core_reg_svc_gap()
    btp.gap_read_ctrl_info()

    return True
