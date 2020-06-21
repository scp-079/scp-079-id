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

from pyrogram import Client, Filters, Message

from ..functions.command import command_error
from ..functions.etc import bold, code, get_forward_name, lang, thread
from ..functions.filters import from_user
from ..functions.telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(Filters.incoming & Filters.private & Filters.forwarded
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
            return command_error(client, message, lang("action_id"), lang("reason_privacy"), report=False)

        # User
        if message.forward_from:
            text = (f"{lang('action')}{lang('colon')}{code(lang('action_id'))}\n"
                    f"{lang('user_name')}{lang('colon')}{code(get_forward_name(message))}\n"
                    f"{lang('user_id')}{lang('colon')}{code(message.forward_from.id)}\n")
            return thread(send_message, (client, cid, text, mid))

        # Channel
        text = (f"{lang('action')}{lang('colon')}{code(lang('action_id'))}\n"
                f"{lang('channel_name')}{lang('colon')}{code(get_forward_name(message))}\n"
                f"{lang('channel_id')}{lang('colon')}{code(message.forward_from_chat.id)}\n")

        if not message.forward_from_chat.restrictions:
            return thread(send_message, (client, cid, text, mid))

        text += (f"{lang('restricted_channel')}{lang('colon')}{code('True')}\n"
                 f"{lang('restricted_reason')}{lang('colon')}" + code("-") * 24 + "\n\n")
        text += "\n\n".join(bold(f"{restriction.reason}-{restriction.platform}") + "\n" + code(restriction.text)
                            for restriction in message.forward_from_chat.restrictions)

        # Send the report message
        thread(send_message, (client, cid, text, mid))

        result = True
    except Exception as e:
        logger.warning(f"ID forward error: {e}", exc_info=True)

    return result
