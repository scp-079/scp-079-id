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
import re

# Enable logging
logger = logging.getLogger(__name__)


def get_username(text: str) -> str:
    # Get username from test
    result = ""

    try:
        if not text.strip():
            return ""

        text = text.strip()

        if "/joinchat/" in text:
            return ""

        pattern = (r"(?<![a-z0-9])(telegram\.(me|dog)|t\.me)/(?!proxy|socks|setlanguage|iv[/?])"
                   r"(?P<username>[a-z][0-9a-z_]{4,31})")
        match = re.search(pattern, text, re.I)

        if not match:
            return ""

        group_dict = match.groupdict()

        if not group_dict or not group_dict.get("username"):
            return ""

        result = group_dict["username"].lower()
    except Exception as e:
        logger.warning(f"Get username error: {e}", exc_info=True)

    return result
