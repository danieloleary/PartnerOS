import os, json

# List of directories to include
paths = ['partner_blueprint', 'Source Materials']
files = []

for path in paths:
    for root, dirs, filenames in os.walk(path):
        for fn in filenames:
            if fn.lower().endswith('.md') or 'Blueprint' in fn:
                # include markdown files or the blueprint single file
                relpath = os.path.join(root, fn)
                files.append(relpath.replace('\\', '/'))

files.sort()
with open('webapp/file_list.json', 'w') as f:
    json.dump(files, f, indent=2)
