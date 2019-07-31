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

def list_files_json(fileLocationStr):
    diskTreeStr = "["
    print(fileLocationStr)

    for root, dirs, files in os.walk(fileLocationStr):
        for d in dirs:
            diskTreeStr += "\n" + d
        for f in files:
            diskTreeStr += "\n" + f


    return diskTreeStr

