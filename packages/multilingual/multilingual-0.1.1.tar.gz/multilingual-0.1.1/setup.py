# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multilingual']

package_data = \
{'': ['*']}

install_requires = \
['googletrans>=4.0.0rc1,<5.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['multilingual = multilingual.main:app']}

setup_kwargs = {
    'name': 'multilingual',
    'version': '0.1.1',
    'description': 'A command line application that automatically translates the input sentence to multiple languages adds the translations to respective translation json files',
    'long_description': '# multilingual\n\n![Alt Text](https://media.giphy.com/media/TksBWToEdzfEtNymcb/giphy.gif)\n\nThis is a command line application that automatically translates the input sentence to multiple languages and adds the \ntranslations to respective translation json files\n\nYou must run this script in the root folder where you keep your translation files.\nFor now, this script assumes that you name your translations with the following patterns:\n```shell\n├───public  // translations root folder\n│   ├───de.json  // {country-iso}.json\n|   ├───main_de.json  // *_{country_iso}.json\n│   └───main-de.json  // *-{country_iso}.json\n```\n\n## Installation\n\n1. Make sure you have at least **Python v3.10.2** installed.\n\n2. Install the package:\n```shell\n$ pip install multilingual\n```\n\n3. Go to the project folder where you keep your translation json files and run **multilingual** command with the sentence you want to translate:\n```shell\n$ cd {YOUR_PROJECT}/{TRANSLATIONS_DIR}` \n\n$ multilingual "Sentence to be translated"\n\n# SENTENCE_TO_BE_TRANSLATED :  Sentence to be translated ---> en-gb.json\n# SENTENCE_TO_BE_TRANSLATED :  Frase a traducir ---> es.json\n# SENTENCE_TO_BE_TRANSLATED :  Phrase à traduire ---> fr.json\n# SENTENCE_TO_BE_TRANSLATED :  번역 될 문장 ---> ko.json\n# SENTENCE_TO_BE_TRANSLATED :  Satz, um übersetzt zu werden ---> de.json\n# SENTENCE_TO_BE_TRANSLATED :  Sentence to be translated ---> en.json\n# SENTENCE_TO_BE_TRANSLATED :  要翻译的句子 ---> zh.json\n```\n\n4. You can optionally specify your own key for your translation:\n```shell\n$ multilingual "Sentence to be translated" --key=TRANSLATION\n\n# TRANSLATION:  Sentence to be translated ---> main-en-gb.json\n# TRANSLATION:  Frase a traducir ---> main-es.json\n# TRANSLATION:  Phrase à traduire ---> main-fr.json\n# TRANSLATION:  번역 될 문장 ---> main-ko.json\n# TRANSLATION:  Satz, um übersetzt zu werden ---> main-de.json\n# TRANSLATION:  Sentence to be translated ---> main-en.json\n# TRANSLATION:  要翻译的句子 ---> main-zh.json\n```\n\n\n## Requirements\n\n* Python 3.10.2\n',
    'author': 'Furkan Tanyol',
    'author_email': 'ftanyol@securecodewarrior.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/furkantanyol/multilingual',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
