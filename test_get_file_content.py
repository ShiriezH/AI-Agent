from functions.get_file_content import get_file_content
from config import MAX_FILE_CHARS


def main():
    print("Testing truncation with lorem.txt:")
    content = get_file_content("calculator", "lorem.txt")
    print(f"Length: {len(content)}")
    print("Truncated message present:",
          "truncated at" in content)
    print()

    print("Reading calculator/main.py:")
    print(get_file_content("calculator", "main.py"))
    print()

    print("Reading pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    print("Attempt to read /bin/cat:")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    print("Attempt to read non-existent file:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    main()
