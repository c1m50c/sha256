from sha256 import encode


def main() -> None:
    inp = input(">>> ")
    print(encode(inp))


if __name__ == "__main__":
    main()