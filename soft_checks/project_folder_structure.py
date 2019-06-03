import os


# folder structure
def list_files(fileFolderPath):
    dirName = ''
    for root, dirs, files in os.walk(fileFolderPath):
        dirName = dirs[0]
        break
    path = fileFolderPath + dirName
    folderStructureStr = '<p> Here is your project folder structure: </p>'
    for root, dirs, files in os.walk(path):
        level = root.replace(fileFolderPath, '').count(os.sep)
        indent = '&nbsp' * 12 * level
        folderStructureStr += ('<p>{}{}/</p>'.format(indent, os.path.basename(root)))
        subindent = '&nbsp' * 12 * (level + 1)
        for f in files:
            folderStructureStr += ('<p>{}{}</p>'.format(subindent, f))
    folderStructureStr += '<p>' + '-'*110 + '</p>'
    return folderStructureStr
# end folder structure
