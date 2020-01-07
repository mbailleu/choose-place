#!/usr/bin/env python3
import csv
import glob
import os
import random
import re
import sys
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Union

from flask import Flask, Markup, abort, render_template, jsonify

app = Flask(__name__)
ROOT = Path(os.path.dirname(os.path.realpath(__file__)))


def get_occasions() -> Tuple[List[str], Dict[str, str]]:
    pattern = str(ROOT.joinpath("data", "*.csv"))
    occasions = []
    filenames: Dict[str, str] = {}
    for path in sorted(glob.glob(pattern)):
        m = re.search(r"\d+_(.*)\.csv$", path)
        if m:
            occasions.append(m.group(1))
            filenames[m.group(1)] = path
    return occasions, filenames


@dataclass(frozen=True)
class Place:
    name: str
    preference: float


def read_csv(filename: str) -> List[Place]:
    places = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", skipinitialspace=True)
        for row in reader:
            p = Place(row["Name"], float(row["Preference"]))
            places.append(p)
    return places


def choose_places(kind: str) -> List[Place]:
    places = read_csv(kind)
    weights = [place.preference for place in places]
    k = 3
    choices = set(random.choices(places, weights=weights, k=k))
    while len(choices) < k and not len(places) < k:
        choices |= set(random.choices(places, weights=weights, k=k - len(choices)))

    return list(choices)


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

@app.route("/api/occasion/<kind>")
def choose_place_json(kind: str) -> str:
    occasions, files = get_occasions()
    if kind not in occasions:
        abort(404)
    places = choose_places(files[kind])
    return jsonify(places)


def main() -> None:
    occasions, files = get_occasions()
    if len(sys.argv) == 1 or sys.argv[1] not in occasions:
        print(sys.argv[0], "|".join(occasions))
        sys.exit(1)
    for i, place in enumerate(choose_places(files[sys.argv[1]])):
        print(f"{i}: {place.name}")


if __name__ == "__main__":
    main()
