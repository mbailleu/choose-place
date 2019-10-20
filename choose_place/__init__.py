#!/usr/bin/env python3
import glob
import os
import sys
import urllib.parse
import re
from pathlib import Path
from typing import List, Tuple, Dict, Union

import numpy as np
from flask import Flask, Markup, abort, render_template

app = Flask(__name__)
ROOT = Path(os.path.dirname(os.path.realpath(__file__)))


def get_occasions() -> Tuple[List[str], Dict[str,str]]:
    pattern = str(ROOT.joinpath("data", "*.csv"))
    occasions = []
    filenames : Dict[str,str] = {}
    for path in sorted(glob.glob(pattern)):
        m = re.search(r'\d+_(.*)\.csv$', path)
        if m:
            occasions.append(m.group(1))
            filenames[m.group(1)] = path
    return occasions, filenames


def choose_places(kind: str) -> List[str]:
    data = np.genfromtxt(kind, dtype=None, delimiter=",", names=True, encoding=None)
    max_vec = np.vectorize(lambda x: max(0, x))
    data["Preference"] = max_vec(data["Preference"])
    p_v = data["Preference"] / data["Preference"].sum()
    return np.random.choice(data["Name"], 3, replace=False, p=p_v)


def create_app():
    return app


@app.route("/")
def index() -> str:
    return render_template("index.html", occasions=get_occasions()[0])


@app.template_filter("urlencode")
def urlencode_filter(s: Union[Markup, str]) -> Markup:
    if isinstance(s, Markup):
        s = s.unescape()
    s = urllib.parse.quote(s)
    return Markup(s)


@app.route("/occasion/<kind>")
def choose_place_html(kind: str) -> str:
    occasions, files = get_occasions()
    if kind not in occasions:
        abort(404)
    places = choose_places(files[kind])
    return render_template("places.html", places=places)


def main() -> None:
    occasions, files = get_occasions()
    if len(sys.argv) == 1 or sys.argv[1] not in occasions:
        print(sys.argv[0], "|".join(occasions))
        sys.exit(1)
    for i, place in enumerate(choose_places(files[sys.argv[1]])):
        print(f"{i}: {place}")


if __name__ == "__main__":
    main()
