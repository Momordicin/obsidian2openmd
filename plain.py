import sys
from converter import read_markdown_file, preprocess_md

if __name__ == "__main__":
    # file_path = "test.md"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Type in file path or drag the file here, and press enter: \n")
    
    print(f"Processing file: {file_path}")

    # flag = input("Replace the original file? (y/n): ")
    # if flag.lower() == 'y' and input("Are you sure? This action cannot be undone. (y/n): ").lower() == 'y':
    #     result_path = file_path
    result_path = file_path[0:file_path.rfind('\\')+1] + 'Opensource_' + file_path[file_path.rfind('\\')+1:]

    md_file = read_markdown_file(file_path)
    md_file = preprocess_md(md_file)
    with open(result_path, 'w', encoding='utf-8') as file:
        file.write(md_file)
    print("Done!")
    print(f"Processed markdown file saved to '{result_path}'")
    input("Press Enter to exit...")