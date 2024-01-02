import os
import re

def process_markdown_files():
    # Get all markdown files
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)

                # open the file
                with open(file_path, 'r') as file:
                    content = file.read()

                    # reliably get the filepath and its parent dir
                    abspath = os.path.abspath(file_path)
                    parent_dir = abspath.split("/")[-2]

                    # Use a regular expression to find and replace image paths
                    updated_content = re.sub(r'\(\.\/([\w\-]*?\.(png|jpg|jpeg|gif))', fr'(/posts/{parent_dir}/\1', content)
#
                # Write the updated content back to the file
                with open(file_path, 'w') as file:
                    file.write(updated_content)
#
if __name__ == "__main__":
    process_markdown_files()
