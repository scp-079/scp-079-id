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

from pyrogram import Chat, Client, User

from .. import glovar
from .etc import bold, code, get_full_name, lang
from .telegram import get_users

# Enable logging
logger = logging.getLogger(__name__)


def get_info_channel(chat: Chat) -> str:
    # Get channel info text
    result = ""

    try:
        text = (f"{lang('action')}{lang('colon')}{code(lang('action_id'))}\n"
                f"{lang('channel_name')}{lang('colon')}{code(chat.title)}\n"
                f"{lang('channel_id')}{lang('colon')}{code(chat.id)}\n")

        if chat.is_verified:
            text += f"{lang('verified_channel')}{lang('colon')}{code('True')}\n"

        if chat.restrictions:
            text += (f"{lang('restricted_channel')}{lang('colon')}{code('True')}\n"
                     f"{lang('restricted_reason')}{lang('colon')}" + code("-") * 16 + "\n\n")
            text += "\n\n".join(bold(f"{restriction.reason}-{restriction.platform}") + "\n" + code(restriction.text)
                                for restriction in chat.restrictions)

        result = text
    except Exception as e:
        logger.warning(f"Get info channel error: {e}", exc_info=True)

    return result


def get_info_group(chat: Chat) -> str:
    # Get group info text
    result = ""

    try:
        text = (f"{lang('action')}{lang('colon')}{code(lang('action_id'))}\n"
                f"{lang('group_name')}{lang('colon')}{code(chat.title)}\n"
                f"{lang('group_id')}{lang('colon')}{code(chat.id)}\n")

        if chat.restrictions:
            text += (f"{lang('restricted_group')}{lang('colon')}{code('True')}\n"
                     f"{lang('restricted_reason')}{lang('colon')}" + code("-") * 16 + "\n\n")
            text += "\n\n".join(bold(f"{restriction.reason}-{restriction.platform}") + "\n" + code(restriction.text)
                                for restriction in chat.restrictions)

        result = text
    except Exception as e:
        logger.warning(f"Get info group error: {e}", exc_info=True)

    return result


def get_info_user(user: User, gid: int = 0, uid: int = 0, rid: int = 0) -> str:
    # Get user info text
    result = ""

    try:
        if gid and rid:
            text = (f"{lang('user_id')}{lang('colon')}{code(uid)}\n"
                    f"{lang('action')}{lang('colon')}{code(lang('action_id'))}\n"
                    f"{lang('replied_id')}{lang('colon')}{code(rid)}\n"
                    f"{lang('group_id')}{lang('colon')}{code(gid)}\n")
        elif gid:
            text = (f"{lang('user_id')}{lang('colon')}{code(uid)}\n"
                    f"{lang('action')}{lang('colon')}{code(lang('action_id'))}\n"
                    f"{lang('group_id')}{lang('colon')}{code(gid)}\n")
        else:
            text = (f"{lang('action')}{lang('colon')}{code(lang('action_id'))}\n"
                    f"{lang('user_name')}{lang('colon')}{code(get_full_name(user))}\n"
                    f"{lang('user_id')}{lang('colon')}{code(user.id)}\n")

        if user.is_scam:
            text += f"{lang('scam_user')}{lang('colon')}{code('True')}\n"

        if user.is_verified:
            text += f"{lang('verified_user')}{lang('colon')}{code('True')}\n"

        if user.restrictions:
            text += (f"{lang('restricted_user')}{lang('colon')}{code('True')}\n"
                     f"{lang('restricted_reason')}{lang('colon')}" + code("-") * 16 + "\n\n")
            text += "\n\n".join(bold(f"{restriction.reason}-{restriction.platform}") + "\n" + code(restriction.text)
                                for restriction in user.restrictions)
            text += "\n\n"

        result = text
    except Exception as e:
        logger.warning(f"Get info user error: {e}", exc_info=True)

    return result


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

        result = result[0]
        glovar.users[uid] = result
    except Exception as e:
        logger.warning(f"Get user error: {e}", exc_info=True)

    return result
