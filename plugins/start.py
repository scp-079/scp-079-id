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
from os import listdir, mkdir
from os.path import exists, isfile, join

from . import glovar
from .functions.file import delete_file, move_file, save

# Enable logging
logger = logging.getLogger(__name__)


def files(path):
    for file in listdir(path):
        if isfile(join(path, file)):
            yield file


def init() -> bool:
    # Init the data
    result = False

    try:
        # Check version
        if glovar.current == glovar.version:
            return True

        # First start
        if not glovar.current:
            glovar.current = glovar.version
            save("current")

        # Version check
        version_0_1_2()
    except Exception as e:
        logger.warning(f"Init error: {e}", exc_info=True)

    return result


def version_0_1_2() -> bool:
    result = False

    try:
        for path in ["data", "data/config", "data/pickle", "data/pickle/backup",
                     "data/log", "data/session", "data/tmp"]:
            not exists(path) and mkdir(path)

        move_file("config.ini", "data/config/config.ini")
        move_file("start.txt", "data/config/start.txt")
        move_file("log", "data/log/log")

        for file in files("data"):
            if file.startswith("."):
                file = file[1:]
                move_file(f"data/.{file}", f"data/pickle/backup/{file}")
            else:
                move_file(f"data/{file}", f"data/backup/{file}")

        move_file("bot.session", "data/session/bot.session")
    except Exception as e:
        logger.warning(f"Version 0.1.2 error: {e}", exc_info=True)

    return result


def renew() -> bool:
    # Renew the session
    result = False

    try:
        if not glovar.token:
            glovar.token = glovar.bot_token
            save("token")
            return False

        if glovar.token == glovar.bot_token:
            return False

        delete_file("/data/session/bot.session")
        glovar.token = glovar.bot_token
        save("token")

        result = True
    except Exception as e:
        logger.warning(f"Renew error: {e}", exc_info=True)

    return result
