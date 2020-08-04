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
from codecs import getdecoder
from configparser import RawConfigParser
from os.path import exists
from typing import Dict, List, Set, Union

from emoji import UNICODE_EMOJI
from pyrogram import Chat, User
from yaml import safe_load

from .checker import check_all, raise_error
from .version import version_control

# Path variables
CONFIG_PATH = "data/config/config.ini"
LOG_PATH = "data/log/log"
START_PATH = "data/config/start.txt"

# Version control
version_control()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename=LOG_PATH,
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

# [emoji]
emoji_ad_single: int = 15
emoji_ad_total: int = 30
emoji_many: int = 15
emoji_protect: Union[bytes, str] = "\\U0001F642"
emoji_wb_single: int = 10
emoji_wb_total: int = 15

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

    # [emoji]
    emoji_ad_single = int(config.get("emoji", "emoji_ad_single", fallback=emoji_ad_single))
    emoji_ad_total = int(config.get("emoji", "emoji_ad_total", fallback=emoji_ad_total))
    emoji_many = int(config.get("emoji", "emoji_many", fallback=emoji_many))
    emoji_protect = config.get("emoji", "emoji_protect", fallback=emoji_protect).encode()
    emoji_protect = getdecoder("unicode_escape")(emoji_protect)[0]
    emoji_wb_single = int(config.get("emoji", "emoji_wb_single", fallback=emoji_wb_single))
    emoji_wb_total = int(config.get("emoji", "emoji_wb_total", fallback=emoji_wb_total))

    # [language]
    lang = config.get("language", "lang", fallback=lang)

    # [mode]
    aio = config.get("mode", "aio", fallback=aio)
    aio = eval(aio)

    # [flag]
    broken = False
except Exception as e:
    print("[ERROR] Read data from config.ini error, please check the log file")
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

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
        "emoji": {
            "emoji_ad_single": emoji_ad_single,
            "emoji_ad_total": emoji_ad_total,
            "emoji_many": emoji_many,
            "emoji_protect": emoji_protect,
            "emoji_wb_single": emoji_wb_single,
            "emoji_wb_total": emoji_wb_total
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

try:
    with open(f"languages/{lang}.yml", "r", encoding="utf-8") as f:
        lang_dict = safe_load(f)
except Exception as e:
    logger.critical(f"Reading language YAML file failed: {e}", exc_info=True)
    raise SystemExit("Reading language YAML file failed")

# Init

all_commands: List[str] = [
    "help",
    "id",
    "start"
]

chats: Dict[int, Chat] = {}
# chats = {
#     -10012345678: Chat
# }

emoji_set: Set[str] = set(UNICODE_EMOJI)

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

version: str = "0.1.3"

# Load data from TXT file

if exists(START_PATH):
    with open(START_PATH, "r", encoding="utf-8") as f:
        start_text = f.read()
else:
    start_text = ""

# Load data from pickle

# Init data

current: str = ""

token: str = ""

# Load data
file_list: List[str] = ["current", "token"]

for file in file_list:
    try:
        try:
            if exists(f"data/pickle/{file}") or exists(f"data/pickle/backup/{file}"):
                with open(f"data/pickle/{file}", "rb") as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"data/pickle/{file}", "wb") as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)

            with open(f"data/pickle/backup/{file}", "rb") as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
