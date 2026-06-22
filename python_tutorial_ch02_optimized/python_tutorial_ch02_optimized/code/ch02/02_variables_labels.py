"""Chapter 02 demo: variables are names bound to objects."""


def main() -> None:
    a = 2
    b = a
    print("a =", a, "id(a) =", id(a))
    print("b =", b, "id(b) =", id(b))
    print("a and b point to the same object:", id(a) == id(b))

    b = 3
    print("\nAfter b = 3")
    print("a =", a, "id(a) =", id(a))
    print("b =", b, "id(b) =", id(b))
    print("Now b points to a different object:", id(a) != id(b))


if __name__ == "__main__":
    main()
