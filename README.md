# SCP-079-ID

With this program, you can create a Telegram bot to check the user ID, group ID, channel ID, and the Data Center to which the user belongs.

## How to use

- [Demo](https://t.me/SCP_079_ID_BOT)
- Read [the document](https://scp-079.org/id/) to learn more
- [README](https://scp-079.org/readme/) of the SCP-079 Project's demo bots
- Discuss [group](https://t.me/SCP_079_CHAT)

## Requirements

- Python 3.6 or higher
- pip: `pip install -r requirements.txt` 

## Files

- data
    - The folder will be generated when program starts
- examples
    - `config.ini` -> `../data/config/config.ini` : Configuration example
    - `start.txt` -> `../data/config/start.txt` : Start template example
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
        - `link.py` : Functions about Telegram link
        - `markup.py` : Get reply markup
        - `program.py` : Functions about program
        - `telegram.py` : Some telegram functions
        - `timers.py` : Timer functions
        - `user.py` : Functions about user
    - handlers
        - `command.py` : Handle commands
        - `message.py`: Handle messages
    - `__init__.py`
    - `checker.py` : Check the format of `config.ini`
    - `glovar.py` : Global variables
    - `start.py` : Execute before client start
    - `version.py` : Execute before main script start
- `.gitignore` : Specifies intentionally untracked files that Git should ignore
- `dictionary.dic` : Project's dictionary 
- `Dockerfile` : Assemble the docker image
- `LICENSE` : GPLv3
- `main.py` : Start here
- `pip.sh` : Script for updating dependencies
- `README.md` : This file
- `requirements.txt` : Managed by pip

## Contribution

Contributions are always welcome, whether it's modifying source code to add new features or bug fixes, documenting new file formats or simply editing some grammar.

You can also join the [discuss group](https://t.me/SCP_079_CHAT) if you are unsure of anything.

## Translation

- [Choose Language Tags](https://www.w3.org/International/questions/qa-choosing-language-tags)
- [Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry)

## License

Licensed under the terms of the [GNU General Public License v3](LICENSE).
