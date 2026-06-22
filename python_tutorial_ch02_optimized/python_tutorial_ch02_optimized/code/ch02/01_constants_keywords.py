"""Chapter 02 demo: constants and Python keywords."""

import keyword
import math


def main() -> None:
    print("Python built-in constants")
    print("True:", True)
    print("False:", False)
    print("None:", None)
    print("math.pi:", round(math.pi, 4))

    print("\nA few Python keywords")
    for word in keyword.kwlist[:12]:
        print("-", word)

    print("\nKeyword count:", len(keyword.kwlist))


if __name__ == "__main__":
    main()
