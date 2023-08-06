# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redlines']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'redlines',
    'version': '0.2.1',
    'description': 'Compare text, and produce human-readable differences or deltas which look like track changes in Microsoft Word.',
    'long_description': '# Redlines\n\n`Redlines` produces a Markdown text showing the differences between two strings/text. The changes are represented with\nstrike-throughs and underlines, which looks similar to Microsoft Word\'s track changes. This method of showing changes is\nmore familiar to lawyers and is more compact for long series of characters.\n\nRedlines uses [SequenceMatcher](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher)\nto find differences between words used.\n\n## Example\n\nGiven an original string:\n\n    The quick brown fox jumps over the lazy dog.`\n\nAnd the string to be tested with:\n\n    The quick brown fox walks past the lazy dog.\n\nThe library gives a result of:\n\n    The quick brown fox <del>jumps over </del><ins>walks past </ins>the lazy dog.\n\nWhich is rendered like this:\n\nThe quick brown fox <del>jumps over </del><ins>walks past </ins>the lazy dog.\n\n## Install\n\n```shell\npip install redlines\n```\n\n## Usage\n\nThe library contains one class: `Redlines`, which is used to compare text.\n\n```python\nfrom redlines import Redlines\n\ntest = Redlines("The quick brown fox jumps over the lazy dog.",\n                "The quick brown fox walks past the lazy dog.")\nassert test.output_markdown == "The quick brown fox <del>jumps over </del><ins>walks past </ins>the lazy dog."\n```\n\nAlternatively, you can create Redline with the text to be tested, and compare several times to see the results.\n\n```python\nfrom redlines import Redlines\n\ntest = Redlines("The quick brown fox jumps over the lazy dog.")\nassert test.compare(\n    \'The quick brown fox walks past the lazy dog.\') == "The quick brown fox <del>jumps over </del><ins>walks past </ins>the lazy dog."\n\nassert test.compare(\n    \'The quick brown fox jumps over the dog.\') == \'The quick brown fox jumps over the <del>lazy </del>dog.\'\n```\n\n## Roadmap / Contributing\n\nPlease feel free to post issues and comments. I work on this in my free time, so please excuse lack of activity.\n\n### Nice things to do\n\n* Style the way changes are presented\n* Other than Markdown, have other output formats (HTML? PDF?)\n* Associate changes with an author\n* Show different changes by different authors or times.\n\nIf this was useful to you, please feel free to [contact me](mailto:houfu@lovelawrobots.com)!\n\n## License\n\nMIT License\n\n',
    'author': 'houfu',
    'author_email': 'houfu@lovelawrobots.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/houfu/redlines',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
