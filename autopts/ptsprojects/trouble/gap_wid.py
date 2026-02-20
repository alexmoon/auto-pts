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

from autopts.pybtp import btp
from autopts.pybtp.types import WIDParams
from autopts.wid import generic_wid_hdl

log = logging.debug


def gap_wid_hdl(wid, description, test_case_name):
    log(f'{gap_wid_hdl.__name__}, {wid}, {description}, {test_case_name}')
    return generic_wid_hdl(wid, description, test_case_name, [__name__, 'autopts.wid.gap'])


def hdl_wid_104(_: WIDParams):
    return True


def hdl_wid_118(params: WIDParams):
    """
    Please press ok to disconnect the link.
    """

    # Directed connection test cases with privacy needs to
    # make sure that Central Address Resolution attribute is
    # received.
    if params.test_case_name in ['GAP/CONN/DCON/BV-04-C',
                                 'GAP/CONN/DCON/BV-05-C']:
        return btp.gap_wait_for_car_receive()

    return True



def hdl_wid_224(_: WIDParams):
    """
    Please configures the IUT into LE Secure Connections Only: Mode 1 Level 2.
    """
    btp.gap_set_mitm_off()
    return True


def hdl_wid_242(_: WIDParams):
    """
    Please send a Security Request.
    """
    btp.gap_pair()
    return True


def hdl_wid_550(_: WIDParams):
    """
    Please confirm that the established security is not sufficient
    to open the outgoing service.
    """
    return True
