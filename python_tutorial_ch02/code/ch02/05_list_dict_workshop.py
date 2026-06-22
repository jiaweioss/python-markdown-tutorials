"""Chapter 02 demo: list and dict operations."""


def main() -> None:
    words = ["I", "love", "you", "my", "dear"]
    print("words:", words)
    print("words[1]:", words[1])
    print("words[0:2]:", words[0:2])

    words.append("Python")
    print("after append:", words)

    del words[2]
    print("after del words[2]:", words)

    favorite_color = {"小美": "粉色", "小明": "黄色", "小东": "绿色"}
    print("\nfavorite_color:", favorite_color)
    print("小美 likes:", favorite_color["小美"])

    favorite_color["小红"] = "紫色"
    favorite_color["小明"] = "绿色"
    del favorite_color["小东"]
    print("after add/update/delete:", favorite_color)


if __name__ == "__main__":
    main()
