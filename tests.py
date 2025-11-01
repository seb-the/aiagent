if __name__ == "__main__":  # python
    from functions import write_files
    print(write_files("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_files("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_files("calculator", "/tmp/temp.txt", "this should not be allowed"))