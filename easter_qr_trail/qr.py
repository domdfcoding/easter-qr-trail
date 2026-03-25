#!/usr/bin/env python3
#
#  qr.py
"""
Generate QR codes.
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
import random
import uuid

# 3rd party
import qrcode

# this package
from easter_qr_trail import NUM_FINDS, STATIC_DIR, UUID_DATA_FILE

__all__ = ["generate_qr_codes", "generate_starter_qr"]


def generate_qr_codes(server_address: str) -> None:
	"""
	Generate QR codes for each spot on the trail.

	:param server_address: The address of the server hosting the trail.
	"""

	STATIC_DIR.maybe_make()

	server_address = server_address.rstrip('/')

	finds_data = {}

	qr_filenames = list(range(NUM_FINDS))
	qr_data = list(range(NUM_FINDS))

	random.shuffle(qr_filenames)
	random.shuffle(qr_data)

	for filename, data_idx in zip(qr_filenames, qr_data):
		finds_data[data_idx] = uuid.uuid4().hex

		url = f"{server_address}/qr/{finds_data[data_idx]}"
		_make_qr_code(url, f"qr_{filename}.png")

	UUID_DATA_FILE.dump_json(finds_data)


def generate_starter_qr(server_address: str) -> None:
	"""
	Generate the QR code taking the user to the landing page.

	:param server_address: The address of the server hosting the trail.
	"""

	STATIC_DIR.maybe_make()

	server_address = server_address.rstrip('/')

	url = f"{server_address}/qr/"
	_make_qr_code(url, "starter_qr.png")


def _make_qr_code(url: str, filename: str) -> None:
	img = qrcode.make(url)
	img.save(STATIC_DIR / filename)  # type: ignore[arg-type]  # False positive
