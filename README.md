# SCP-079-ID

This bot is used to get the ID of user, channel, and group on Telegram.

## How to use

- [Demo](https://t.me/SCP_079_ID_BOT)
- Read [the document](https://scp-079.org/id/) to learn more
- [README](https://scp-079.org/readme/) of the SCP-079 Project's demo bots
- Discuss [group](https://t.me/SCP_079_CHAT)

## Requirements

- Python 3.6 or higher
- pip: `pip install -r requirements.txt` 

## Files

- languages
   - `cmn-Hans.yml` : Mandarin Chinese (Simplified)
- plugins
    - functions
        - `command.py` : Functions about command
        - `decorators.py` : Some decorators
        - `etc.py` : Miscellaneous
        - `file.py` : Save files
        - `filters.py` : Some filters
        - `group.py` : Functions about group
        - `telegram.py` : Some telegram functions
    - handlers
        - `command.py` : Handle commands
        - `message.py`: Handle messages
    - `checker.py` : Check the format of `config.ini`
    - `glovar.py` : Global variables
    - `session.py` : Manage `bot.session`
- `.gitignore` : Ignore
- `config.ini.example` -> `config.ini` : Configuration
- `LICENSE` : GPLv3
- `main.py` : Start here
- `README.md` : This file
- `start.txt.example` -> `start.txt` : Start template
- `requirements.txt` : Managed by pip

## Contribution

Contributions are always welcome, whether it's modifying source code to add new features or bug fixes, documenting new file formats or simply editing some grammar.

You can also join the [discuss group](https://t.me/SCP_079_CHAT) if you are unsure of anything.

## Translation

- [Choose Language Tags](https://www.w3.org/International/questions/qa-choosing-language-tags)
- [Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry)

## License

Licensed under the terms of the [GNU General Public License v3](LICENSE).
