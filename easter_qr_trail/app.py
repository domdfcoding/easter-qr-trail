#!/usr/bin/env python3
#
#  app.py
"""
Flask webapp.
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
from typing import Tuple

# 3rd party
from domdf_python_tools.paths import PathPlus
from flask import Flask, render_template, request

# this package
from easter_qr_trail import NUM_FINDS, UUID_DATA_FILE

__all__ = ["home", "qr", "starter"]

app = Flask(__name__)

uuid_to_image = {v: k for k, v in UUID_DATA_FILE.load_json().items()}

print(uuid_to_image)

state_directory = PathPlus("state")
state_directory.maybe_make()


@app.route('/')
def home() -> str:
	return render_template("home.html")


@app.route("/qr/")
def starter() -> str:
	return render_template("starter.html")


@app.route("/qr/<uuid>")
def qr(uuid: str) -> Tuple[str, int]:
	user = request.remote_addr

	if user is None:
		return "Could not determine user", 400

	# Create state file
	user_state_dir = state_directory / user
	(user_state_dir).maybe_make()
	(user_state_dir / uuid_to_image[uuid]).touch()

	# Build current state
	current_state = [f.name for f in user_state_dir.iterdir()]
	kwargs = {}

	for n in range(NUM_FINDS):
		kwargs[f"img_{n}"] = False

	# for image in state[user]:
	for image in current_state:
		kwargs[f"img_{image}"] = True

	return render_template("image.html", **kwargs), 200
