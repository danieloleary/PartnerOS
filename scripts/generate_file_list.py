import os, json

# List of directories to include
paths = ['docs', 'Source Materials']
files = []

for path in paths:
    for root, dirs, filenames in os.walk(path):
        for fn in filenames:
            if fn.lower().endswith('.md') or 'Blueprint' in fn:
                # include markdown files or the blueprint single file
                relpath = os.path.join(root, fn)
                # Make path relative to webapp directory
                relpath = relpath.replace('\\', '/')
                # Add leading slash to make it absolute from webapp
                relpath = '/' + relpath
                files.append(relpath)

files.sort()
with open('webapp/file_list.json', 'w') as f:
    json.dump(files, f, indent=2)
