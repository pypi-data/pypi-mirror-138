# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['paintprint']
setup_kwargs = {
    'name': 'paintprint',
    'version': '1.0.3',
    'description': 'This module can colorize any text in your terminal',
    'long_description': '# PaintPrint\nThis module can colorize any text in your terminal\n\n# Installing\n```bat\npip install PaintPrint\n```\n\n# Quick start\n\n## Hello world\nThis is a simple hello world:\n```python\nfrom PaintPrint import *\n\nbprint("Hello world!", \n       FORMATTING.BOLD, \n       FOREGROUND.RED, \n       BACKGROUND.GREEN)\n```\nIn your console you can see something like this:\n\n<img src="https://sun9-51.userapi.com/impg/IT0eADkdwaa9P-ioqdvS5odxwRDkMQovT0Wflw/issddN7LQOs.jpg?size=1009x432&quality=96&sign=9ef43db819f6b795dea2736da8856808&type=album"/>\n\n## Unreadable symbols\nIf you see incomprehensible symbols instead of colors in the console, perform this function at the beginning of your code:\n```python\nfrom PaintPrint import *\nneutralizeColorProblem()\n```\n\n## Templates\nIn this module you can use some templates for beautiful print on terminal:\n\n```python\nfrom PaintPrint import *\n\nbprint("TEMPLATES", \n       FORMATTING.BORDERED, \n       FORMATTING.BOLD, \n       FOREGROUND.MAGENTA, \n       BACKGROUND.WHITE)\n\nprint("Template for links: " + bformat("python.org", TEMPLATE.URL))\nbprint("This is a `positive` template", TEMPLATE.POSITIVE)\nbprint("\\tAnd this is a `negative`", TEMPLATE.NEGATIVE)\nprint("You also can write " + bformat("yes", TEMPLATE.YES) + " and " + bformat("no", TEMPLATE.NO) + " like here")\nprint("If you like " + bformat("black and white", TEMPLATE.BLACKWHITE1) + " or " + bformat("white and black", TEMPLATE.BLACKWHITE2) + " you can using special templates!")\n```\n\n<img src="https://sun9-32.userapi.com/impg/LannX-z_IBqLVLfRX9wGq2xDy7CihWleznmfkw/M_3K9UTjZGA.jpg?size=1009x432&quality=96&sign=88fb94abe1bb88aa4426fb8cd3b14533&type=album"/>\n\n# All functions\n\n<img src="https://sun9-40.userapi.com/impg/xmSdO8_KIXiy1GmUuijwTmw4sLI9vlOW6UGs9Q/XTWsALYsDss.jpg?size=1009x964&quality=96&sign=f5955bd4b800f18ff5798d1d762d3bc9&type=album"/>\n',
    'author': 'tankalxat34',
    'author_email': 'tankalxat34@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tankalxat34/PaintPrint',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
