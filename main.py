#!/usr/bin/env python3
import sys
import numpy as np
from typing import List
from flask import Flask
app = Flask(__name__)

def choose_place(kind: str) -> List[str]:
    data = np.genfromtxt(kind, dtype = None, delimiter = ',', names = True, encoding = None)
    max_vec = np.vectorize(lambda x: max(0, x))
    data["Preference"] = max_vec(data["Preference"])
    p_v = data["Preference"] / data["Preference"].sum()
    values = np.random.choice(data["Name"], 3, replace = False, p = p_v)
    resp = []
    for i, v in enumerate(values):
        resp.append("%d: %s" % (i, v))
    return resp

def choose_place_html(kind: str) -> str:
    places = choose_place(f"{kind}.csv")
    resp = "<html><ul>"
    for place in places:
        resp += f"<li>{place}</li>"
    resp += "</ul></html>"
    return resp

def create_app():
    return app

@app.route('/')
def index() -> str:
    return """
<html>
<head>
</head>
<body>
  <ul>
  <li> <a href="/pub">Pub</a></li>
  <li> <a href="/lunch">Lunch</a></li>
  <li> <a href="/dinner">Dinner</a></li>
  </li>
  </ul>
</body>
</html>
    """

@app.route("/pub")
def pub() -> str:
    return choose_place_html("pub")

@app.route("/lunch")
def lunch() -> str:
    return choose_place_html("lunch")

@app.route("/dinner")
def dinner() -> str:
    return choose_place_html("dinner")

def main(argv: List[str]) -> int:
    if len(argv) == 1:
        print(argv[0], "list")
        return 1
    print("\n".join(choose_place(argv[1])))

if __name__ == "__main__":
    main(sys.argv)
