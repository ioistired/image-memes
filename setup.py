#!/usr/bin/env python3

import re
import setuptools
from pathlib import Path

HERE = Path(__file__).parent

with open(HERE / 'README.md') as f:
	README = f.read()

with open(HERE / 'requirements.txt') as f:
	install_requires = f.readlines()

setuptools.setup(
	name='memes',
	url='https://github.com/ioistired/image-memes',
	version='0.0.0',
	packages=['memes'],
	license='EUPL-1.2',
	description='Generate meme images',
	long_description=README,
	long_description_content_type='text/markdown; variant=GFM',
	install_requires=install_requires,
	python_requires='>=3.9.0',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: End Users/Desktop',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'License :: OSI Approved :: MIT License',
		'License :: Other/Proprietary License',
	],
	package_data={'memes': [
		'res/this_your_admin/*.png',
	]},
	entry_points={
		'console_scripts': ['this-your-admin = memes.this_your_admin:main'],
	},
)
