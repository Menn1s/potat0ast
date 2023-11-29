import os
import re

files = os.listdir()
for file in files:
    if ".md" in file:
        with open(file, "r") as md_file:
            for line in md_file:
                links = re.findall('\[(\w*)]\(\s*(.*)\s*\)', line)
                if links:
                    description = links[0][0]
                    link = links[0][1]
                    print('{{<preview-link "' + link + '" ' + description + '>}}')
