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

from pyrogram import Client, filters
from pyrogram.types import Message

from ..functions.command import command_error
from ..functions.etc import code, get_full_name, lang, thread
from ..functions.filters import from_user
from ..functions.telegram import send_message
from ..functions.user import get_info_channel, get_info_user

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(filters.incoming & filters.private & filters.contact
                   & from_user)
def id_contact(client: Client, message: Message) -> bool:
    # Get ID in private chat from contact card
    result = False

    try:
        # Basic data
        cid = message.chat.id
        mid = message.message_id

        # Check the message
        if not message.contact:
            return False

        # User
        text = (f"{lang('action')}{lang('colon')}{code(lang('action_id'))}\n"
                f"{lang('message_type')}{lang('colon')}{code(lang('con'))}\n"
                f"{lang('user_name')}{lang('colon')}{code(get_full_name(message.contact))}\n"
                f"{lang('user_id')}{lang('colon')}{code(message.contact.user_id)}\n")

        # Channel
        thread(send_message, (client, cid, text, mid))

        result = True
    except Exception as e:
        logger.warning(f"ID contact error: {e}", exc_info=True)

    return result


@Client.on_message(filters.incoming & filters.private & filters.forwarded
                   & from_user)
def id_forward(client: Client, message: Message) -> bool:
    # Get ID in private chat from forwarded message
    result = False

    try:
        # Basic data
        cid = message.chat.id
        mid = message.message_id

        # Check the message
        if not message.forward_from and not message.forward_from_chat:
            return command_error(client, message, lang("action_id"), lang("reason_privacy"),
                                 report=False, private=True)

        # User
        if message.forward_from:
            text = get_info_user(message.forward_from)
            return thread(send_message, (client, cid, text, mid))

        # Channel
        text = get_info_channel(message.forward_from_chat)
        thread(send_message, (client, cid, text, mid))

        result = True
    except Exception as e:
        logger.warning(f"ID forward error: {e}", exc_info=True)

    return result
