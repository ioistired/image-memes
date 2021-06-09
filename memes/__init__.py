#!/usr/bin/env python3

from pathlib import Path

RES_DIR = Path(__file__).parent / 'res'

def _get_resource_dir(module_name):
	return RES_DIR.joinpath(*module_name.split('.')[1:])
