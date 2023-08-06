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
    'version': '0.1.0',
    'description': 'A command line application that automatically translates the input sentence to multiple languages adds the translations to respective translation json files',
    'long_description': '# multilingual\n\nThis is a command line application that automatically translates the input sentence to multiple languages and adds the \ntranslations to respective translation json files\n\nYou must run this script in the root folder where you keep your translation files.\nFor now, this script assumes that you name your translations with the following patterns:\n```shell\n{country-iso}.json --> de.json \n*-{country_iso}.json --> main-de.json\n```\n\n![Alt Text](https://media.giphy.com/media/TksBWToEdzfEtNymcb/giphy.gif)\n\n## Installation\n\n* Install **python 3.10.2**\n\n* Clone this repo: \n```shell\n$ git clone https://github.com/furkantanyol/multilingual.git\n```\n\n* There are 2 ways to run this command line application:\n\n1. Run the script file in your local directly:\n```shell\n# 1. Go to the project folder where you keep your translation json files: \n$ cd {YOUR_PROJECT}/{TRANSLATIONS_DIR}` \n\n# 2. Point to the correct directory where this project is installed and run \n$ python {CLONED_ROOT}/multilingual/multilingual.py "Sentence to be translated"\n# SENTENCE_TO_BE_TRANSLATED :  Sentence to be translated ---> main-en-gb.json\n# SENTENCE_TO_BE_TRANSLATED :  Frase a traducir ---> main-es.json\n# SENTENCE_TO_BE_TRANSLATED :  Phrase à traduire ---> main-fr.json\n# SENTENCE_TO_BE_TRANSLATED :  번역 될 문장 ---> main-ko.json\n# SENTENCE_TO_BE_TRANSLATED :  Satz, um übersetzt zu werden ---> main-de.json\n# SENTENCE_TO_BE_TRANSLATED :  Sentence to be translated ---> main-en.json\n# SENTENCE_TO_BE_TRANSLATED :  要翻译的句子 ---> main-zh.json\n```\n\n2. Install & run the distribution in your local:\n```shell\n# 1. Install build tool: \n$ pip install build\n\n# 2. In the project root, run: \n$ python -m build \n# This will result in two output files in the dist directory: \n# - dist/multilingual-0.0.1.tar.gz \n# - dist/multilingual-0.0.1-py3-none-any.whl\n\n# 3. Install the distribution you just created:\n$ pip install dist/multilingual-0.0.1-py3-none-any.whl \n# This should create the CLI shortcuts in the current Python environment’s bin directory.\n# - {Python Path}/bin/my-application\n# - {Python Path}/bin/another-application\n\n# 4. Go to the project folder where you keep your translation json files: \n$ cd {YOUR_PROJECT}/{TRANSLATIONS_DIR}\n\n# 5. Run:\n$ multilingual "Sentence to be translated"\n# SENTENCE_TO_BE_TRANSLATED :  Sentence to be translated ---> main-en-gb.json\n# SENTENCE_TO_BE_TRANSLATED :  Frase a traducir ---> main-es.json\n# SENTENCE_TO_BE_TRANSLATED :  Phrase à traduire ---> main-fr.json\n# SENTENCE_TO_BE_TRANSLATED :  번역 될 문장 ---> main-ko.json\n# SENTENCE_TO_BE_TRANSLATED :  Satz, um übersetzt zu werden ---> main-de.json\n# SENTENCE_TO_BE_TRANSLATED :  Sentence to be translated ---> main-en.json\n# SENTENCE_TO_BE_TRANSLATED :  要翻译的句子 ---> main-zh.json\n```\n     \n* For a clean environment: \n\n```shell\n# create virtual environment\n$ python -m venv .env/fresh-install-test\n\n# activate your virtual environment\n$ . .env/fresh-install-test/bin/activate\n\n# install your package into this fresh environment\n$ pip install dist/multilingual-0.0.1-py3-none-any.whl\n\n# your shortcuts are now in the venv bin directory\n$ ls .env/fresh-install-test/bin/\nmultilingual\n\n# so you can run it directly from the cli\n$ multilingual "Sentence to be translated"\n# SENTENCE_TO_BE_TRANSLATED :  Sentence to be translated ---> main-en-gb.json\n# SENTENCE_TO_BE_TRANSLATED :  Frase a traducir ---> main-es.json\n# SENTENCE_TO_BE_TRANSLATED :  Phrase à traduire ---> main-fr.json\n# SENTENCE_TO_BE_TRANSLATED :  번역 될 문장 ---> main-ko.json\n# SENTENCE_TO_BE_TRANSLATED :  Satz, um übersetzt zu werden ---> main-de.json\n# SENTENCE_TO_BE_TRANSLATED :  Sentence to be translated ---> main-en.json\n# SENTENCE_TO_BE_TRANSLATED :  要翻译的句子 ---> main-zh.json\n```\n\nYou can optionally specify your own key for your translation:\n```shell\n$ multilingual "Sentence to be translated" --key=TRANSLATION\n# TRANSLATION:  Sentence to be translated ---> main-en-gb.json\n# TRANSLATION:  Frase a traducir ---> main-es.json\n# TRANSLATION:  Phrase à traduire ---> main-fr.json\n# TRANSLATION:  번역 될 문장 ---> main-ko.json\n# TRANSLATION:  Satz, um übersetzt zu werden ---> main-de.json\n# TRANSLATION:  Sentence to be translated ---> main-en.json\n# TRANSLATION:  要翻译的句子 ---> main-zh.json\n```\n\n\n## Requirements\n\n* python 3.10.2\n',
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
