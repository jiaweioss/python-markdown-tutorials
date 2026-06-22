"""Chapter 02 demo: bool logic and number rounding."""

import math


def main() -> None:
    has_homework = True
    has_finished = False

    print("has_homework and has_finished:", has_homework and has_finished)
    print("has_homework or has_finished:", has_homework or has_finished)
    print("not has_finished:", not has_finished)

    values = [2.1, 2.5, 2.9, -2.1]
    print("\nRounding table")
    for value in values:
        print(
            value,
            "round=", round(value),
            "floor=", math.floor(value),
            "ceil=", math.ceil(value),
        )


if __name__ == "__main__":
    main()
