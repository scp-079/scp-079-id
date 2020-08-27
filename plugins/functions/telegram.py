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
from typing import Iterable, List, Optional, Union

from pyrogram import Client
from pyrogram.errors import ChatAdminRequired, ButtonDataInvalid, ButtonUrlInvalid, ChannelInvalid, ChannelPrivate
from pyrogram.errors import FloodWait, MessageDeleteForbidden, PeerIdInvalid,  UsernameInvalid, UsernameNotOccupied
from pyrogram.raw.types import InputPeerUser, InputPeerChannel
from pyrogram.types import Chat, ChatPreview, InlineKeyboardMarkup, ReplyKeyboardMarkup, Message, User

from .. import glovar
from .etc import delay, get_int
from .decorators import retry

# Enable logging
logger = logging.getLogger(__name__)


def delete_messages(client: Client, cid: int, mids: Iterable[int]) -> Optional[bool]:
    # Delete some messages
    result = None

    try:
        mids = list(mids)

        if len(mids) <= 100:
            return delete_messages_100(client, cid, mids)

        mids_list = [mids[i:i + 100] for i in range(0, len(mids), 100)]
        result = bool([delete_messages_100(client, cid, mids) for mids in mids_list])
    except Exception as e:
        logger.warning(f"Delete messages in {cid} error: {e}", exc_info=True)

    return result


@retry
def delete_messages_100(client: Client, cid: int, mids: Iterable[int]) -> Optional[bool]:
    # Delete some messages
    result = None

    try:
        mids = list(mids)
        result = client.delete_messages(chat_id=cid, message_ids=mids)
    except FloodWait as e:
        raise e
    except MessageDeleteForbidden:
        return False
    except Exception as e:
        logger.warning(f"Delete messages in {cid} error: {e}", exc_info=True)

    return result


@retry
def get_chat(client: Client, cid: Union[int, str]) -> Union[Chat, ChatPreview, None]:
    # Get a chat
    result = None

    try:
        result = client.get_chat(chat_id=cid)
    except FloodWait as e:
        raise e
    except (ChannelInvalid, ChannelPrivate, PeerIdInvalid):
        return None
    except Exception as e:
        logger.warning(f"Get chat {cid} error: {e}", exc_info=True)

    return result


@retry
def get_users(client: Client, uids: Iterable[Union[int, str]]) -> Optional[List[User]]:
    # Get users
    result = None

    try:
        result = client.get_users(user_ids=uids)
    except FloodWait as e:
        raise e
    except PeerIdInvalid:
        return None
    except Exception as e:
        logger.warning(f"Get users {uids} error: {e}", exc_info=True)

    return result


@retry
def resolve_peer(client: Client, pid: Union[int, str]) -> Union[bool, InputPeerChannel, InputPeerUser, None]:
    # Get an input peer by id
    result = None

    try:
        result = client.resolve_peer(pid)
    except FloodWait as e:
        raise e
    except (PeerIdInvalid, UsernameInvalid, UsernameNotOccupied):
        return False
    except Exception as e:
        logger.warning(f"Resolve peer {pid} error: {e}", exc_info=True)

    return result


def resolve_username(client: Client, username: str, cache: bool = True) -> (str, int):
    # Resolve peer by username
    peer_type = ""
    peer_id = 0

    try:
        username = username.strip("@")

        if not username:
            return "", 0

        the_cache = glovar.usernames.get(username)

        if cache and the_cache:
            return the_cache["peer_type"], the_cache["peer_id"]

        result = resolve_peer(client, username)

        if not result:
            glovar.usernames[username] = {}
            glovar.usernames[username]["peer_type"] = peer_type
            glovar.usernames[username]["peer_id"] = peer_id
            return peer_type, peer_id

        if isinstance(result, InputPeerChannel):
            peer_type = "channel"
            peer_id = result.channel_id
            peer_id = get_int(f"-100{peer_id}")
        elif isinstance(result, InputPeerUser):
            peer_type = "user"
            peer_id = result.user_id

        glovar.usernames[username] = {
            "peer_type": peer_type,
            "peer_id": peer_id
        }
    except Exception as e:
        logger.warning(f"Resolve username {username} error: {e}", exc_info=True)

    return peer_type, peer_id


@retry
def send_message(client: Client, cid: int, text: str, mid: int = None,
                 markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None) -> Union[bool, Message, None]:
    # Send a message to a chat
    result = None

    try:
        if not text.strip():
            return None

        result = client.send_message(
            chat_id=cid,
            text=text,
            parse_mode="html",
            disable_web_page_preview=True,
            reply_to_message_id=mid,
            reply_markup=markup
        )
    except FloodWait as e:
        raise e
    except (ButtonDataInvalid, ButtonUrlInvalid):
        logger.warning(f"Send message to {cid} - invalid markup: {markup}")
    except (ChannelInvalid, ChannelPrivate, ChatAdminRequired, PeerIdInvalid):
        return False
    except Exception as e:
        logger.warning(f"Send message to {cid} error: {e}", exc_info=True)

    return result


def send_report_message(secs: int, client: Client, cid: int, text: str, mid: int = None,
                        markup: InlineKeyboardMarkup = None) -> Optional[bool]:
    # Send a message that will be auto deleted to a chat
    result = None

    try:
        result = send_message(
            client=client,
            cid=cid,
            text=text,
            mid=mid,
            markup=markup
        )

        if not result:
            return None

        mid = result.message_id
        mids = [mid]
        result = delay(secs, delete_messages, [client, cid, mids])
    except Exception as e:
        logger.warning(f"Send report message to {cid} error: {e}", exc_info=True)

    return result
