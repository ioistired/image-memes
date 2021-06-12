#!/usr/bin/env python3

from pathlib import Path

_RES_DIR = Path(__file__).parent / 'res'

def _get_resource_dir(module_name):
	return _RES_DIR.joinpath(*module_name.split('.')[1:])

from .this_your_admin import this_your_admin
from .timecard import timecard
from .crab_rave import crab_rave
