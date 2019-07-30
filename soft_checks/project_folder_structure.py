import os
from functools import reduce
import json


# folder structure
def list_files(fileLocationStr):
    folderStructureStr = "<h3> Project Folder Structure </h3> <div id='folder_struct'>"
    for root, dirs, files in os.walk(fileLocationStr):
        level = root.replace(fileLocationStr, '').count(os.sep)
        indent = '&nbsp' * 12 * level
        if os.path.basename(root) != '':
            folderStructureStr += ('<p>{}{}/</p>'.format(indent, os.path.basename(root)))
        subindent = '&nbsp' * 12 * (level + 1)
        for f in files:
            folderStructureStr += ("<p>{}{}</p>".format(subindent, f))
    folderStructureStr += "</div>"
    return folderStructureStr
# end folder structure

def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path, x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d

def list_files_json(fileLocationStr):
    #value = path_to_dict(fileLocationStr)
    #value = jsonify("")

    folderStructureJson = {}
    fileLocationStr = fileLocationStr.rstrip(os.sep)
    start = fileLocationStr.rfind(os.sep) + 1

    for path, dirs, files in os.walk(fileLocationStr):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], folderStructureJson)
        parent[folders[-1]] = subdir

    print(fileLocationStr)
    #print("THIS IS THE FOLDER TREE")
    return '''{
  "type": "directory",
  "name": "hello",
  "children": [
    {
      "type": "directory",
      "name": "world",
      "children": [
        {
          "type": "file",
          "name": "one.txt"
        },
        {
          "type": "file",
          "name": "two.txt"
        }
      ]
    },
    {
      "type": "file",
      "name": "README"
    }
  ]
}'''


