# SCP-079-ID - Get Telegram ID
# Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-ID.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from typing import Optional, Union

from pyrogram import Client, User

from .. import glovar
from .telegram import get_users

# Enable logging
logger = logging.getLogger(__name__)


def get_user(client: Client, uid: Union[int, str], cache: bool = True) -> Optional[User]:
    # Get a user
    result = None

    try:
        the_cache = glovar.users.get(uid)

        if cache and the_cache:
            return the_cache

        result = get_users(client, [uid])

        if not result:
            return None

        glovar.users[uid] = result[0]
    except Exception as e:
        logger.warning(f"Get user error: {e}", exc_info=True)

    return result
