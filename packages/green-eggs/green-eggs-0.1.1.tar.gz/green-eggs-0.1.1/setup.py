# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['green_eggs', 'green_eggs.commands']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.1,<4.0.0',
 'aiologger[aiofiles]>=0.6.1,<0.7.0',
 'websockets>=10.1,<11.0']

setup_kwargs = {
    'name': 'green-eggs',
    'version': '0.1.1',
    'description': 'A framework to build a Twitch chatbot.',
    'long_description': "# Green Eggs\n\n### About\n\nThis is a library/framework that you can use to easily create a channel chatbot with Python code.\n\nIt is intended to be very quick and simple to set up and use, and either be stopped and started whenever, or stay running indefinitely.\n\n### Usage\n\nSee `example.py` for an example bot setup. That's all there is for now, more in-depth documentation is coming soon.\n- `bot.register_basic_commands` is a function that takes a mapping of first word invoke to response strings.\n- `bot.register_command` is a decorator that takes a first word invoke and decorates a function that's called when the command is run.\n  - Notice in the example that this can be a sync or async function.\n  - The parameters must be accessible by keyword, and the value depends on the name of the keyword.\n\n### Features\n\n- A robust IRC client that ensures that expected responses to actions have happened, such as joining and leaving a channel, and reconnects or fails as necessary.\n- A Helix API accessor with functions for each documented endpoint, fully typed for URL parameter and payload body values.\n- An expandable way of specifying how messages trigger command, beyond just the first word being `!command`.\n- A complete suite of dataclasses to represent all possible data that comes through the IRC chat. This allows for robust typings.\n\n### Features soon coming\n\n- Cooldowns on commands, per user and global.\n- Link detection and conditional deletion, so you don't have to disallow links in channel settings.\n\n### Eventual future features\n\n- A way to write the bot with a config file and/or a python file.\n- A suite of SQLAlchemy models to save incoming data from IRC, with columns to match the dataclasses.\n- API result caching.\n- A suite of CLI options to quickly make API calls and database queries.\n- Webhooks for handling events that don't come through in chat, and better handling of events that do.\n",
    'author': 'Hameed Gifford',
    'author_email': 'giff.h92@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hamstap85/green-eggs/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
