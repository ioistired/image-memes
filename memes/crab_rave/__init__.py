#!/usr/bin/env python3
# SPDX-License-Identifier: EUPL-1.2

import io
import tempfile
import textwrap
import itertools
import subprocess
from typing import NamedTuple
from .. import _get_resource_dir
from PIL import ImageDraw, Image, ImageFont

class Dimensions(NamedTuple):
	width: int
	height: int

RESOURCE_DIR = _get_resource_dir(__name__)
FONT_PATH = RESOURCE_DIR / 'AvenirLTStd-Book.otf'
# have to hardcode because PIL doesn't work on videos and I don't want to run ffprobe in a subprocess just for this
CANVAS_SIZE = Dimensions(640, 360)

# lifted from https://github.com/khazhyk/dango.py/blob/7bfea895ff8422de166b1e2ccd05c22aca4b5cf8/dango/plugins/common/py
# and used under MIT license
def draw_text_dropshadow(
	draw: ImageDraw.Draw,
	location, text, color, shadow_color, shadow_offset, *args, **kwargs,
):
	"""Draw text with outline in the shittiest way possible."""
	# Remember - (0,0) is top left
	from_left, from_top = location
	if shadow_offset:
		shadow_left, shadow_top = shadow_offset
		draw.text((from_left + shadow_left, from_top + shadow_top), text, *args, fill=shadow_color, **kwargs)
	draw.text((from_left, from_top), text, *args, fill=color, **kwargs)

# lifted from https://github.com/khazhyk/dango.py/blob/7bfea895ff8422de166b1e2ccd05c22aca4b5cf8/dango/plugins/common/py
# and used under MIT license
def raster_font_textwrap(text, wrap_width, font) -> list:
	if not text:
		return [""]
	if "\n" in text:
		lines = text.split("\n")
		return list(itertools.chain(*(raster_font_textwrap(line, wrap_width, font) for line in lines)))
	else:
		avg_width, _ = font.getsize(text)
		px_per_char = max(avg_width / len(text), 1)
		return textwrap.wrap(text, int(wrap_width / px_per_char))

# lifted from https://github.com/khazhyk/dango.py/blob/7bfea895ff8422de166b1e2ccd05c22aca4b5cf8/dango/plugins/fun.py#L352-L412
def crab_rave(text, output_file_path) -> None:
	"""make crab rave video with your text overlayed. save to the path specified (must end in '.mp4')"""
	# Simple brute force font size selection...
	font_height = 48
	line_height = font_height * 1.2
	font = ImageFont.truetype(str(FONT_PATH), encoding='unic',size=font_height)
	lines = raster_font_textwrap(text, CANVAS_SIZE.width, font)
	estimated_height = line_height * len(lines)
	while estimated_height > CANVAS_SIZE.height and font_height > 1:
		font_height -= 1
		line_height = font_height * 1.2
		font = ImageFont.truetype(str(FONT_PATH), encoding='unic',size=font_height)
		lines = raster_font_textwrap(text, CANVAS_SIZE.width, font)
		estimated_height = line_height * len(lines)

	print(font_height)

	# Draw and save to temporary file for ffmpeg to read
	im = Image.new("RGBA", CANVAS_SIZE)
	draw = ImageDraw.Draw(im)

	center_x, center_y = (x/2 for x in CANVAS_SIZE)
	# Initial top pad to center vertically
	top_pad = -(line_height * len(lines) / 2) + (line_height - font_height)
	for line in lines:
		text_x, text_y = font.getsize(line)
		text_pos = (center_x - text_x/2, center_y + top_pad)
		top_pad += line_height
		# We draw one by one because it lets me do custom centering
		draw_text_dropshadow(
			draw, text_pos, line, "white", "#222", (1, 1), font=font)

	with tempfile.NamedTemporaryFile(suffix='.png') as text_img_file:
		im.save(text_img_file)

		subprocess.check_call([
				"ffmpeg", "-i", RESOURCE_DIR / 'cr.mp4', "-i", text_img_file.name,
				"-filter_complex", "[0:v][1:v] overlay=0:0",
				"-pix_fmt", "yuv420p", output_file_path,
			],
		)
