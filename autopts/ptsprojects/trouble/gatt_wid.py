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
from binascii import hexlify

from autopts.ptsprojects.stack import GattCharacteristicDescriptor
from autopts.ptsprojects.testcase import MMI
from autopts.pybtp import btp
from autopts.pybtp.types import WIDParams
from autopts.wid import generic_wid_hdl
from autopts.wid.gatt import gatt_server_fetch_db

log = logging.debug


def gatt_wid_hdl(wid, description, test_case_name):
    log(f'{gatt_wid_hdl.__name__}, {wid}, {description}, {test_case_name}')
    return generic_wid_hdl(wid, description, test_case_name, [__name__, 'autopts.wid.gatt'])


def hdl_wid_52(params: WIDParams):
    """Override: don't treat UUID.CEP specially — compare raw hex octets."""
    if params.test_case_name.startswith('GATT/CL'):
        return btp.verify_description(params.description)

    MMI.reset()
    MMI.parse_description(params.description)

    handle = int(MMI.args[0], 16)
    value = MMI.args[1]

    db = gatt_server_fetch_db()
    attr = db.attr_lookup_handle(handle)
    if attr is None:
        return False

    if not isinstance(attr, GattCharacteristicDescriptor):
        return False

    value_read_str = hexlify(attr.value).upper().decode('utf-8')

    # PTS may select characteristic with value bigger than MTU but asks to
    # verify only MTU bytes of data
    if value_read_str != value:
        if not value_read_str.startswith(value):
            return False

    return True
