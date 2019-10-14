#!/usr/bin/env python3
import os
import sys
import urllib.parse
from pathlib import Path
from typing import List, Union

import numpy as np
from flask import Flask, Markup, abort, render_template

app = Flask(__name__)
ROOT = Path(os.path.dirname(os.path.realpath(__file__))).joinpath("..")

list_of_occasions = ["Breakfast", "Lunch", "Coffee", "Dinner", "Pub"]


def choose_places(kind: str) -> List[str]:
    kind_csv = ROOT.joinpath(kind)
    data = np.genfromtxt(kind_csv, dtype=None, delimiter=",", names=True, encoding=None)
    max_vec = np.vectorize(lambda x: max(0, x))
    data["Preference"] = max_vec(data["Preference"])
    p_v = data["Preference"] / data["Preference"].sum()
    return np.random.choice(data["Name"], 3, replace=False, p=p_v)


def create_app():
    return app


@app.route("/")
def index() -> str:
    return render_template("index.html", occasions=list_of_occasions)


@app.template_filter("urlencode")
def urlencode_filter(s: Union[Markup, str]) -> Markup:
    if isinstance(s, Markup):
        s = s.unescape()
    s = urllib.parse.quote(s)
    return Markup(s)


@app.route("/occasion/<kind>")
def choose_place_html(kind: str) -> str:
    if kind not in [x.lower() for x in list_of_occasions]:
        abort(404)
    places = choose_places(f"{kind}.csv")
    return render_template("places.html", places=places)


def main() -> None:
    if len(sys.argv) == 1:
        print(sys.argv[0], "list")
        sys.exit(1)
    for i, place in enumerate(choose_places(sys.argv[1])):
        print(f"{i}: {place}")


if __name__ == "__main__":
    main()
