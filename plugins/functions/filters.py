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
from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from .. import glovar

# Enable logging
logger = logging.getLogger(__name__)


def is_from_user(_, __, update: Union[CallbackQuery, Message]) -> bool:
    # Check if the message is sent from a user, or the callback is sent from a private chat
    result = False

    try:
        if (isinstance(update, CallbackQuery)
                and (not update.message or not update.message.chat or update.message.chat.id < 0)):
            return False

        if update.from_user and update.from_user.id != 777000:
            return True
    except Exception as e:
        logger.warning(f"Is from user error: {e}", exc_info=True)

    return result


def is_test_group(_, __, update: Union[CallbackQuery, Message]) -> bool:
    # Check if the message is sent from the test group
    result = False

    try:
        if isinstance(update, CallbackQuery):
            message = update.message
        else:
            message = update

        if not message.chat or message.chat.type != "supergroup":
            return False

        cid = message.chat.id

        if cid == glovar.test_group_id:
            return True
    except Exception as e:
        logger.warning(f"Is test group error: {e}", exc_info=True)

    return result


from_user = filters.create(
    func=is_from_user,
    name="From User"
)

test_group = filters.create(
    func=is_test_group,
    name="Test Group"
)
