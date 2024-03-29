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

from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import Client, idle

from plugins import glovar
from plugins.functions.timers import interval_hour_01, log_rotation
from plugins.start import init, renew

# Enable logging
logger = logging.getLogger(__name__)

# Init
init()

# Renew session
renew()

# Config session
app = Client(
    name="bot",
    api_id=glovar.api_id,
    api_hash=glovar.api_hash,
    ipv6=glovar.ipv6,
    bot_token=glovar.bot_token,
    plugins={
        "root": "plugins",
        "include": [
            "handlers.command",
            "handlers.message"
        ]
    },
    proxy=glovar.proxy,
    workdir=glovar.SESSION_DIR_PATH,
    sleep_threshold=0
)
app.start()

# Timer
scheduler = BackgroundScheduler(job_defaults={"misfire_grace_time": 60})
scheduler.add_job(interval_hour_01, "interval", hours=1)
scheduler.add_job(log_rotation, "cron", hour=23, minute=59)
scheduler.start()

# Hold
idle()

# Stop
app.stop()
