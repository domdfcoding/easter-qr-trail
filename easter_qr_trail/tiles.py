#!/usr/bin/env python3
#
#  tiles.py
"""
Generate individual tiles from a source image.
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import os

# 3rd party
from domdf_python_tools.typing import PathLike
from split_image import split_image  # type: ignore[import-untyped]

# this package
from easter_qr_trail import IMAGES_DIR, TILE_COLS, TILE_ROWS

__all__ = ["generate_tiles", "split_egg_images"]


def _split_image(source_image: PathLike, rows: int, cols: int, suffix: str) -> None:
	split_image(
			source_image,
			rows,
			cols,
			should_square=False,
			should_cleanup=False,
			should_quiet=True,
			output_dir=IMAGES_DIR,
			)

	source_image_stem = os.path.splitext(source_image)[0]

	for filename in IMAGES_DIR.glob(f"{source_image_stem}*"):
		new_filename = filename.parent.joinpath(filename.name.replace(f"{source_image_stem}_", suffix))
		filename.rename(new_filename.with_suffix(".jpeg"))


def generate_tiles(source_image: PathLike) -> None:
	"""
	Generate tiles for the given image.

	:param source_image:
	"""

	_split_image(source_image, TILE_ROWS, TILE_COLS, '')


def split_egg_images(source_image: PathLike) -> None:
	"""
	Generate images for the individual easter eggs from the input atlas image.

	:param source_image:
	"""

	_split_image(source_image, 2, 4, "egg_")
