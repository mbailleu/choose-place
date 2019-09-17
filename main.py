import sys
import numpy as np

from typing import List

def main(argv: List[str]) -> int:
    if len(argv) == 1:
        print(argv[0], "list")
        return 1

    data = np.genfromtxt(argv[1], dtype = None, delimiter = ',', names = True, encoding = None)
    max_vec = np.vectorize(lambda x: max(0, x))
    data["Preference"] = max_vec(data["Preference"])
    p_v = data["Preference"] / data["Preference"].sum()
    values = np.random.choice(data["Name"], 3, replace = False, p = p_v)
    for i, v in enumerate(values):
        print("%d: %s" % (i, v))
    return 0

if __name__ == "__main__":
    main(sys.argv)
