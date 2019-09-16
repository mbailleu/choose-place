import sys
import numpy as np

from typing import List

def main(argv: List[str]) -> int:
    if len(argv) == 1:
        print(argv[0], "list")
        return 1

    data = np.genfromtxt(argv[1], dtype = None, delimiter = ',', names = True, encoding = None)
    total = data["Preference"].sum()
    for i in range(3):
        print(i, np.random.choice(data["Name"], p = [ (x / total) for x in data["Preference"]]))
    return 0

if __name__ == "__main__":
    main(sys.argv)
