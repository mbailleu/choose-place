#!/usr/bin/env python3
import sys
import os
from pathlib import Path
from typing import List

import numpy as np
from flask import Flask, abort

app = Flask(__name__)
ROOT = Path(os.path.dirname(os.path.realpath(__file__))).joinpath("..")


def choose_place(kind: str) -> List[str]:
    kind_csv = ROOT.joinpath(kind)
    data = np.genfromtxt(kind_csv, dtype=None, delimiter=",", names=True, encoding=None)
    max_vec = np.vectorize(lambda x: max(0, x))
    data["Preference"] = max_vec(data["Preference"])
    p_v = data["Preference"] / data["Preference"].sum()
    values = np.random.choice(data["Name"], 3, replace=False, p=p_v)
    resp = []
    for i, v in enumerate(values):
        resp.append("%d: %s" % (i, v))
    return resp


def create_app():
    return app


@app.route("/")
def index() -> str:
    return """
<html>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<head>
</head>
<body style="font-size:5vw">
  <ul>
  <li> <a href="/occasion/pub">Pub</a></li>
  <li> <a href="/occasion/lunch">Lunch</a></li>
  <li> <a href="/occasion/dinner">Dinner</a></li>
  <li> <a href="/occasion/breakfast">Breakfast</a></li>
  </li>
  </ul>
</body>
</html>
    """


@app.route("/occasion/<kind>")
def choose_place_html(kind: str) -> str:
    if kind not in ["pub", "lunch", "dinner", "breakfast"]:
        abort(404)
    places = choose_place(f"{kind}.csv")
    resp = """
    <html>
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <ul style="font-size:5vw">"""
    for place in places:
        resp += f"<li>{place}</li>"
    resp += "</ul></html>"
    return resp


def main() -> None:
    if len(sys.argv) == 1:
        print(sys.argv[0], "list")
        sys.exit(1)
    print("\n".join(choose_place(sys.argv[1])))


if __name__ == "__main__":
    main()
