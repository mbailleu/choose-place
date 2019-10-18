#!/usr/bin/env python3
import glob
import os
import sys
import urllib.parse
from pathlib import Path
from typing import List, Union

import numpy as np
from flask import Flask, Markup, abort, render_template

app = Flask(__name__)
ROOT = Path(os.path.dirname(os.path.realpath(__file__)))


def get_occasions() -> List[str]:
    pattern = str(ROOT.joinpath("data", "*.csv"))
    occasions = []
    for path in glob.glob(pattern):
        occasion = os.path.splitext(os.path.basename(path))[0]
        occasions.append(occasion)
    return occasions


def choose_places(kind: str) -> List[str]:
    kind_csv = ROOT.joinpath("data", f"{kind}.csv")
    data = np.genfromtxt(kind_csv, dtype=None, delimiter=",", names=True, encoding=None)
    max_vec = np.vectorize(lambda x: max(0, x))
    data["Preference"] = max_vec(data["Preference"])
    p_v = data["Preference"] / data["Preference"].sum()
    return np.random.choice(data["Name"], 3, replace=False, p=p_v)


def create_app():
    return app


@app.route("/")
def index() -> str:
    return render_template("index.html", occasions=get_occasions())


@app.template_filter("urlencode")
def urlencode_filter(s: Union[Markup, str]) -> Markup:
    if isinstance(s, Markup):
        s = s.unescape()
    s = urllib.parse.quote(s)
    return Markup(s)


@app.route("/occasion/<kind>")
def choose_place_html(kind: str) -> str:
    if kind not in get_occasions():
        abort(404)
    places = choose_places(kind)
    return render_template("places.html", places=places)


def main() -> None:
    occasions = get_occasions()
    if len(sys.argv) == 1 or sys.argv[1] not in occasions:
        print(sys.argv[0], "|".join(occasions))
        sys.exit(1)
    for i, place in enumerate(choose_places(sys.argv[1])):
        print(f"{i}: {place}")


if __name__ == "__main__":
    main()
