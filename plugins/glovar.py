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
import pickle
from configparser import RawConfigParser
from os.path import exists
from typing import Dict, List, Set, Union

from pyrogram import emoji
from pyrogram.types import Chat, User
from yaml import safe_load

from .checker import check_all, raise_error
from .version import version_control

# Path variables
CONFIG_PATH = "data/config/config.ini"
CUSTOM_LANG_PATH = "data/config/custom.yml"
LOG_PATH = "data/log"
PICKLE_BACKUP_PATH = "data/pickle/backup"
PICKLE_PATH = "data/pickle"
SESSION_DIR_PATH = "data/session"
SESSION_PATH = "data/session/bot.session"
START_PATH = "data/config/start.txt"

# Version control
version_control()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename=f"{LOG_PATH}/log",
    filemode="a"
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [flag]
broken: bool = True

# [basic]
bot_token: str = ""
prefix: List[str] = []
prefix_str: str = "/!"

# [channels]
test_group_id: int = 0

# [language]
lang: str = "cmn-Hans"

# [mode]
aio: Union[bool, str] = "False"

try:
    not exists(CONFIG_PATH) and raise_error(f"{CONFIG_PATH} does not exists")
    config = RawConfigParser()
    config.read(CONFIG_PATH)

    # [basic]
    bot_token = config.get("basic", "bot_token", fallback=bot_token)
    prefix_str = config.get("basic", "prefix", fallback=prefix_str)
    prefix = [p for p in list(prefix_str) if p]

    # [channels]
    test_group_id = int(config.get("channels", "test_group_id", fallback=test_group_id))

    # [language]
    lang = config.get("language", "lang", fallback=lang)

    # [mode]
    aio = config.get("mode", "aio", fallback=aio)
    aio = eval(aio)

    # [flag]
    broken = False
except Exception as e:
    print(f"[ERROR] Read data from {CONFIG_PATH} error, please check the log file")
    logger.warning(f"Read data from {CONFIG_PATH} error: {e}", exc_info=True)

# Check
check_all(
    {
        "basic": {
            "bot_token": bot_token,
            "prefix": prefix
        },
        "channels": {
            "test_group_id": test_group_id
        },
        "language": {
            "lang": lang
        },
        "mode": {
            "aio": aio
        }
    },
    broken
)

# Language Dictionary
lang_dict: dict = {}
LANG_PATH = CUSTOM_LANG_PATH if exists(CUSTOM_LANG_PATH) else f"languages/{lang}.yml"

try:
    with open(LANG_PATH, "r", encoding="utf-8") as f:
        lang_dict = safe_load(f)
except Exception as e:
    logger.critical(f"Reading language YAML file failed: {e}", exc_info=True)
    raise SystemExit("Reading language YAML file failed")

# Init

all_commands: List[str] = [
    "help",
    "id",
    "restart",
    "start",
    "update"
]

chats: Dict[int, Chat] = {}
# chats = {
#     -10012345678: Chat
# }

emoji_set: Set[str] = {v for k, v in vars(emoji).items() if not k.startswith("_")}

sender: str = "ID"

started_ids: Set[int] = set()
# started_ids = {12345678}

usernames: Dict[str, Dict[str, Union[int, str]]] = {}
# usernames = {
#     "SCP_079": {
#         "peer_type": "channel",
#         "peer_id": -1001196128009
#     }
# }

users: Dict[int, User] = {}
# users = {
#     12345678: User
# }

version: str = "0.1.5"

updating: bool = False

# Load data from TXT file

if exists(START_PATH):
    with open(START_PATH, "r", encoding="utf-8") as f:
        start_text = f.read()
else:
    start_text = ""

# Load data from pickle

# Init data

current: str = ""
# current = "0.0.1"

token: str = ""
# token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

# Load data
file_list: List[str] = ["current", "token"]

for file in file_list:
    try:
        try:
            if exists(f"{PICKLE_PATH}/{file}") or exists(f"{PICKLE_BACKUP_PATH}/{file}"):
                with open(f"{PICKLE_PATH}/{file}", "rb") as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"{PICKLE_PATH}/{file}", "wb") as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)

            with open(f"{PICKLE_BACKUP_PATH}/{file}", "rb") as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
