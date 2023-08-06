# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['daily_hn']
install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['daily_hn = daily_hn:main']}

setup_kwargs = {
    'name': 'daily-hn',
    'version': '0.1.2',
    'description': 'A command line tool for displaying and opening links to the current best stories from news.ycombinator.com (Hacker News)',
    'long_description': "# daily_hn\n\n![Tests](https://github.com/Rolv-Apneseth/daily_hn/actions/workflows/tests.yml/badge.svg)\n![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)\n![OSX](https://img.shields.io/badge/-OSX-black?logo=apple)\n![Python](https://img.shields.io/badge/Python-v3.9%5E-green?logo=python)\n\n![Demo aPNG](https://github.com/Rolv-Apneseth/Rolv-Apneseth.github.io/blob/4f0024e25168a57757d4631a6346275cb3f9cee7/assets/images/animated_images/daily-hn.png)\n\n## Description\n\nA command line tool for displaying and opening links to the current best stories from [news.ycombinator.com](https://news.ycombinator.com) (Hacker News).\n\nYou can find the best stories page this program parses [here](https://news.ycombinator.com/best)!\n\n## Dependencies\n\n- [Python](https://www.python.org/downloads/) v3.9+\n- [Beautiful Soup 4](https://pypi.org/project/beautifulsoup4/)\n- [Requests](https://pypi.org/project/requests/)\n- If you are on Windows: [Windows curses module](https://pypi.org/project/windows-curses/) (Python)\n\n## Installation\n\nTo download, click on 'Code' to the top right, then download as a zip file. You can unzip using your preferred program.\n\n> You can also clone the repository using:\n\n```bash\ngit clone https://github.com/Rolv-Apneseth/daily_hn.git\n```\n\nNext, install the requirements for the program.\n\n> In your terminal, navigate to the cloned directory and run:\n\n```bash\npython3 -m pip install requests beautifulsoup4\n```\n\nThen, to place the `daily_hn` script at `/usr/local/daily_hn`:\n\n```bash\nsudo make install\n```\n\nNow, to launch the program in your terminal simply run `daily_hn`\n\n### Windows\n\nInstall the requirements for the program.\n\n> In your terminal, navigate to the cloned directory and run:\n\n```bash\npip install beautifulsoup4 requests windows-curses\n```\n\nTo launch the program, navigate to the project directory and run:\n\n```bash\npython daily_hn.py\n```\n\n## Usage\n\nWith the curses UI (default), you can open up stories (uses the default browser) by pressing the shortcut key to the left of that story. Navigate up and down using either `j` and `k` for fine movements or `{` and `}` for bigger jumps. To quit, press `q`.\n\nTo simply print out a list of stories (links being clickable depends on your terminal emulator), provide the `-p` flag\n\n## License\n\n[MIT](https://github.com/Rolv-Apneseth/daily_hn/blob/2d40839e6e625c55075430bde5fef337a08e89ba/LICENSE)\n",
    'author': 'Rolv-Apneseth',
    'author_email': 'rolv.apneseth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Rolv-Apneseth/daily_hn/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
