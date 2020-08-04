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

from .. import glovar
from .etc import get_readable_time
from .file import move_file

# Enable logging
logger = logging.getLogger(__name__)


def interval_hour_01() -> bool:
    # Execute every hour
    result = False

    try:
        # Clear started ids
        glovar.started_ids = set()
    except Exception as e:
        logger.warning(f"Interval hour 01 error: {e}", exc_info=True)

    return result


def log_rotation() -> bool:
    # Log rotation
    result = False

    try:
        move_file(f"{glovar.LOG_PATH}/log", f"{glovar.LOG_PATH}/log-{get_readable_time(the_format='%Y%m%d')}")

        with open(f"{glovar.LOG_PATH}/log", "w", encoding="utf-8") as f:
            f.write("")

        result = True
    except Exception as e:
        logger.warning(f"Log rotation error: {e}", exc_info=True)

    return result
