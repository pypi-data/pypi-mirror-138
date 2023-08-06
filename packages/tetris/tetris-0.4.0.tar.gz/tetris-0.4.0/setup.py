# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tetris', 'tetris.engine']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.4,<2.0.0', 'typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'tetris',
    'version': '0.4.0',
    'description': 'Simple and modular tetris library',
    'long_description': '# python-tetris: a simple and modular tetris library\n\n[![pypi](https://img.shields.io/pypi/v/tetris?logo=pypi&logoColor=f0f0f0&style=for-the-badge)](https://pypi.org/project/tetris/) ![versions](https://img.shields.io/pypi/pyversions/tetris?logo=python&logoColor=f0f0f0&style=for-the-badge) [![build](https://img.shields.io/github/workflow/status/dzshn/python-tetris/Test%20library?logo=github&logoColor=f0f0f0&style=for-the-badge)](https://github.com/dzshn/python-tetris/actions/workflows/test.yml) [![](https://img.shields.io/badge/contains-technical%20debt-009fef?style=for-the-badge)](https://forthebadge.com/)\n\n---\n\n## Intro\n\nA simple and modular library for implementing and analysing Tetris games, [guideline](https://archive.org/details/2009-tetris-variant-concepts_202201)-compliant by default\n\n```py\n>>> import tetris\n>>> game = tetris.BaseGame()\n>>> game.engine\nEngine(gravity=InfinityGravity, queue=SevenBag, rs=SRS, scorer=GuidelineScorer)\n>>> game.queue\nSevenBag([PieceType.J, PieceType.O, PieceType.Z, PieceType.I, PieceType.S, PieceType.T, PieceType.S])\n>>> print(game)\n\n\n          @\n      @ @ @\n```\n\n## Install\n\nThis package is available on [PyPI](https://pypi.org/project/tetris/), you can install it with pip:\n\n```sh\npip install tetris\n\n```\n\nOr, build from source using [poetry](https://python-poetry.org/):\n\n```sh\npoetry install\npoetry build\n```\n\n## Quickstart\n\n_For a simple implementation, see [examples/cli.py](https://github.com/dzshn/python-tetris/blob/main/examples/cli.py)_\n\nThe main API consists of `tetris.BaseGame` and `tetris.Engine`, which hold the game state and modular implementations respectively\n\nAn instance of `tetris.Engine` can be reused between `tetris.BaseGame`s, and contains the subclasses of `Gravity`, `Queue`, `RotationSystem` and `Scorer` that are instantiated within `tetris.BaseGame`. The library provides a default engine (namely `tetris.DefaultEngine`), which parts work roughly akin to modern games\n\nThe pseudocode for a standard implementation is the following\n\n```py\nimport tetris\nfrom tetris import Move\n\nkeymap = {\n    "a": Move.left(),   # or Move.drag(...)\n    "d": Move.right(),\n    "w": Move.hard_drop(),\n    "s": Move.soft_drop(),\n    ... # etc.\n}\n\ngame = tetris.BaseGame()\n\nwhile True:\n    game.tick()  # Let the library update things like gravity\n\n    render()  # Output the game as you wish\n    key = get_key()  # Get current input\n\n    if key in keymap:\n        game.push(keymap[key])\n```\n\nIt\'s only left to the developer to render and process input\n',
    'author': 'Sofia "dzshn" N. L.',
    'author_email': 'zshn@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dzshn/python-tetris',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
