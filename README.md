# ayachanbot

(Currently) an anime image searching Telegram bot

## Get Started

First setup Telegram bot token env:

```bash
export BOT_TOKEN=<your bot token>
```

Optionally setup proxy if you require it.

Ensure temp dir for images:

```bash
mkdir -p /tmp/ayachanbot
```

Then run the package directly to start the bot:

```bash
python3 -m ayachanbot
```

## Thanks

[Tsuk1ko/cq-picsearcher-bot](https://github.com/Tsuk1ko/cq-picsearcher-bot) shows how to request some popular image searching websites.

## License

GPL 3.0 or later

Copyright (c) myl7 2020

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
