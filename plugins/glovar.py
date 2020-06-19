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
from os import mkdir
from os.path import exists
from shutil import rmtree
from typing import Dict, List, Union

from pyrogram import Chat
from yaml import safe_load

from .checker import check_all

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename="log",
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
lang: str = ""

# [mode]
aio: Union[bool, str] = ""

try:
    config = RawConfigParser()
    config.read("config.ini")

    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = [p for p in list(config["basic"].get("prefix", prefix_str)) if p]

    # [channels]
    test_group_id = int(config["channels"].get("test_group_id", str(test_group_id)))

    # [language]
    lang = config["language"].get("lang", lang)

    # [mode]
    aio = config["mode"].get("aio", aio)
    aio = eval(aio)

    # [flag]
    broken = False
except Exception as e:
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

sender: str = "ID"

usernames: Dict[str, Dict[str, Union[int, str]]] = {}
# usernames = {
#     "SCP_079": {
#         "peer_type": "channel",
#         "peer_id": -1001196128009
#     }
# }

version: str = "0.0.5"

# Load data from TXT file

with open("start.txt", "r", encoding="utf-8") as f:
    start_text = f.read()

# Load data from pickle

# Init dir
try:
    rmtree("tmp")
except Exception as e:
    logger.info(f"Remove tmp error: {e}")

for path in ["data", "tmp"]:
    not exists(path) and mkdir(path)

# Init data

token: str = ""

# Load data
file_list: List[str] = ["token"]

for file in file_list:
    try:
        try:
            if exists(f"data/{file}") or exists(f"data/.{file}"):
                with open(f"data/{file}", "rb") as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"data/{file}", "wb") as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)

            with open(f"data/.{file}", "rb") as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
