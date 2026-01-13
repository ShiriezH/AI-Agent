from functions.run_python_file import run_python_file


def main():
    print("Running calculator/main.py with no args:")
    print(run_python_file("calculator", "main.py"))
    print()

    print("Running calculator/main.py with expression:")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print("Running calculator/tests.py:")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Attempt to escape working directory:")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Attempt to run nonexistent file:")
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    print("Attempt to run non-Python file:")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()
