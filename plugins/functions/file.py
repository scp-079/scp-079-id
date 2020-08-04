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
from os import remove
from os.path import exists
from pickle import dump
from shutil import copyfile, move, rmtree

from .. import glovar
from .decorators import threaded

# Enable logging
logger = logging.getLogger(__name__)


def copy_file(src: str, dst: str) -> bool:
    # Copy a file
    result = False

    try:
        if not src or not exists(src) or not dst:
            return False

        result = copyfile(src, dst) or True
    except Exception as e:
        logger.warning(f"Copy file error: {e}", exc_info=True)

    return result


def delete_file(path: str) -> bool:
    # Delete a file
    result = False

    try:
        if not(path and exists(path)):
            return False

        result = remove(path) or True
    except Exception as e:
        logger.warning(f"Delete file error: {e}", exc_info=True)

    return result


def move_file(src: str, dst: str) -> bool:
    # Move a file
    result = False

    try:
        if not src or not exists(src) or not dst:
            return False

        result = bool(move(src, dst))
    except Exception as e:
        logger.warning(f"Move file error: {e}", exc_info=True)

    return result


def remove_dir(path: str) -> bool:
    # Remove a directory
    result = False

    try:
        if not path or not exists(path):
            return False

        result = rmtree(path) or True
    except Exception as e:
        logger.warning(f"Remove dir error: {e}", exc_info=True)

    return result


@threaded(daemon=False)
def save(file: str) -> bool:
    # Save a global variable to a file
    result = False

    try:
        if not glovar:
            return False

        with open(f"{glovar.PICKLE_BACKUP_PATH}/{file}", "wb") as f:
            dump(eval(f"glovar.{file}"), f)

        result = copyfile(f"{glovar.PICKLE_BACKUP_PATH}/{file}", f"{glovar.PICKLE_PATH}/{file}")
    except Exception as e:
        logger.warning(f"Save error: {e}", exc_info=True)

    return result
