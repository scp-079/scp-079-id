# SCP-079-ID - Get Telegram ID
# Copyright (C) 2019-2023 SCP-079 <https://scp-079.org>
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
from subprocess import run, PIPE

from pyrogram import Client, filters
from pyrogram.types import Message

from .. import glovar
from ..functions.command import command_error, get_command_type
from ..functions.etc import bold, code, general_link, get_int, get_readable_time, lang, mention_id, thread
from ..functions.filters import from_user, test_group
from ..functions.group import get_group
from ..functions.link import get_username
from ..functions.program import restart_program, update_program
from ..functions.markup import get_text_and_markup
from ..functions.telegram import resolve_username, send_message
from ..functions.user import get_user, get_info_channel, get_info_group, get_info_user

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(filters.incoming & filters.group & ~filters.forwarded & filters.command(["id"], glovar.prefix)
                   & ~test_group
                   & from_user)
def id_group(client: Client, message: Message) -> bool:
    # Get ID in group
    result = False

    try:
        # Basic data
        gid = message.chat.id
        uid = message.from_user.id
        mid = message.id

        # Get command type
        command_type = get_command_type(message)

        # Check the command type
        if command_type:
            return command_error(client, message, lang("action_id"), lang("error_private_para"), report=False)

        # Generate the text
        if message.reply_to_message and message.reply_to_message.from_user:
            text = get_info_user(message.reply_to_message.from_user, gid, uid, message.reply_to_message.from_user.id)
        else:
            text = get_info_user(message.from_user, gid, uid)

        if not message.chat.restrictions:
            return thread(send_message, (client, gid, text, mid))

        text += (f"{lang('restricted_group')}{lang('colon')}{code('True')}\n"
                 f"{lang('restricted_reason')}{lang('colon')}" + code("-") * 16 + "\n\n")
        text += "\n\n".join(bold(f"{restriction.reason}-{restriction.platform}") + "\n" + code(restriction.text)
                            for restriction in message.chat.restrictions)

        # Send the report message
        thread(send_message, (client, gid, text, mid))

        result = True
    except Exception as e:
        logger.warning(f"ID group error: {e}", exc_info=True)

    return result


@Client.on_message(filters.incoming & filters.private & ~filters.forwarded & filters.command(["id"], glovar.prefix)
                   & from_user)
def id_private(client: Client, message: Message) -> bool:
    # Get id in private chat by command
    result = False

    try:
        # Basic data
        cid = message.chat.id
        mid = message.id

        # Get command type
        command_type = get_command_type(message)
        username = get_username(command_type)
        username = username if username else command_type

        # Check the command
        if not username:
            text = get_info_user(message.from_user)
            return thread(send_message, (client, cid, text, mid))

        # Avoid privacy issue
        if username[0] in "-0123456789":
            return command_error(client, message, lang("action_id"), lang("command_para"),
                                 report=False, private=True)

        # Get the id
        the_type, the_id = resolve_username(client, username)

        # Check the id
        if not the_type or the_type not in {"channel", "user"} or not the_id:
            return command_error(client, message, lang("action_id"), lang("command_para"),
                                 report=False, private=True)

        # User
        if the_type == "user":
            user = get_user(client, the_id)
            text = get_info_user(user)
            return thread(send_message, (client, cid, text, mid))

        # Channel or group
        chat = get_group(client, the_id)

        if not chat:
            text = (f"{lang('action')}{lang('colon')}{code(lang('action_id'))}\n"
                    f"ID{lang('colon')}{code(the_id)}\n")
            return thread(send_message, (client, cid, text, mid))

        if chat.type == "channel":
            text = get_info_channel(chat)
        elif chat.type == "supergroup":
            text = get_info_group(chat)
        else:
            text = ""

        # Send the report message
        thread(send_message, (client, cid, text, mid))

        result = True
    except Exception as e:
        logger.warning(f"ID private error: {e}", exc_info=True)

    return result


@Client.on_message(filters.incoming & filters.group & filters.command(["restart"], glovar.prefix)
                   & test_group
                   & from_user)
def restart(client: Client, message: Message) -> bool:
    # Restart the program
    result = False

    try:
        # Basic data
        cid = message.chat.id
        aid = message.from_user.id
        mid = message.id

        # Get command type
        command_type = get_command_type(message)

        # Check the command type
        if command_type and command_type.upper() != glovar.sender:
            return False

        # Generate the text
        text = (f"{lang('admin')}{lang('colon')}{mention_id(aid)}\n\n"
                f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                f"{lang('action')}{lang('colon')}{code(lang('program_restart'))}\n"
                f"{lang('status')}{lang('colon')}{code(lang('command_received'))}\n")

        # Send the report message
        send_message(client, cid, text, mid)

        # Restart the program
        result = restart_program()
    except Exception as e:
        logger.warning(f"Restart error: {e}", exc_info=True)

    return result


@Client.on_message(filters.incoming & filters.private & ~filters.forwarded
                   & filters.command(["start", "help"], glovar.prefix)
                   & from_user)
def start(client: Client, message: Message) -> bool:
    # Start the bot
    result = False

    try:
        # Basic data
        cid = message.chat.id
        mid = message.id

        # Check started ids
        if cid in glovar.started_ids:
            return False

        # Add to started ids
        glovar.started_ids.add(cid)

        # Check aio mode
        if glovar.aio:
            return False

        # Generate the text and markup
        text, markup = get_text_and_markup(glovar.start_text)

        # Check start text
        if not text:
            return False

        # Send the report message
        thread(send_message, (client, cid, text, mid, markup))

        result = True
    except Exception as e:
        logger.warning(f"Start error: {e}", exc_info=True)

    return result


@Client.on_message(filters.incoming & filters.group & filters.command(["update"], glovar.prefix)
                   & test_group
                   & from_user)
def update(client: Client, message: Message) -> bool:
    # Update the program
    result = False

    try:
        # Basic data
        cid = message.chat.id
        aid = message.from_user.id
        mid = message.id

        # Get command type
        command_type = get_command_type(message)

        # Check the command type
        if command_type and command_type.upper() != glovar.sender:
            return False

        # Generate the text
        text = (f"{lang('admin')}{lang('colon')}{mention_id(aid)}\n\n"
                f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                f"{lang('action')}{lang('colon')}{code(lang('program_update'))}\n"
                f"{lang('status')}{lang('colon')}{code(lang('command_received'))}\n")

        # Send the report message
        send_message(client, cid, text, mid)

        # Update the program
        glovar.updating = True
        result = update_program()
    except Exception as e:
        logger.warning(f"Update error: {e}", exc_info=True)

    return result


@Client.on_message(filters.incoming & filters.group & filters.command(["version"], glovar.prefix)
                   & test_group
                   & from_user)
def version(client: Client, message: Message) -> bool:
    # Check the program's version
    result = False

    try:
        # Basic data
        cid = message.chat.id
        aid = message.from_user.id
        mid = message.id

        # Get command type
        command_type = get_command_type(message)

        # Check the command type
        if command_type and command_type.upper() != glovar.sender:
            return False

        # Check update status
        if glovar.updating:
            text = (f"{lang('admin')}{lang('colon')}{mention_id(aid)}\n\n"
                    f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                    f"{lang('status')}{lang('colon')}{code(lang('program_updating'))}\n")
            return thread(send_message, (client, cid, text, mid))

        # Version info
        git_change = bool(run("git diff-index HEAD --", stdout=PIPE, shell=True).stdout.decode().strip())
        git_date = run("git log -1 --format='%at'", stdout=PIPE, shell=True).stdout.decode()
        git_date = get_readable_time(get_int(git_date), "%Y/%m/%d %H:%M:%S")
        git_hash = run("git rev-parse --short HEAD", stdout=PIPE, shell=True).stdout.decode()
        get_hash_link = f"https://github.com/scp-079/scp-079-{glovar.sender.lower()}/commit/{git_hash}"
        command_date = get_readable_time(int(message.date.timestamp()), "%Y/%m/%d %H:%M:%S")

        # Generate the text
        text = (f"{lang('admin')}{lang('colon')}{mention_id(aid)}\n\n"
                f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                f"{lang('version')}{lang('colon')}{code(glovar.version)}\n"
                f"{lang('git_change')}{lang('colon')}{code(git_change)}\n"
                f"{lang('git_hash')}{lang('colon')}{general_link(git_hash, get_hash_link)}\n"
                f"{lang('git_date')}{lang('colon')}{code(git_date)}\n"
                f"{lang('command_date')}{lang('colon')}{code(command_date)}\n")

        # Send the report message
        result = bool(send_message(client, cid, text, mid))
    except Exception as e:
        logger.warning(f"Version error: {e}", exc_info=True)

    return result
