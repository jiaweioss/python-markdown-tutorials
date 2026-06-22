"""Chapter 02 demo: string creation, search, replace, split, and slicing."""


def main() -> None:
    country = "China"
    name = "Python learner"
    age = 18

    print(f"My name is {name}, and I am {age} years old.")
    print("country:", country)
    print("country.lower():", country.lower())
    print("country.replace('China', 'Python City'):", country.replace("China", "Python City"))

    word = "huawei"
    print("\nword:", word)
    print("word[0]:", word[0])
    print("word[-1]:", word[-1])
    print("word[0:3]:", word[0:3])

    sentence = "song huan gong"
    print("\nsentence.split():", sentence.split())


if __name__ == "__main__":
    main()
