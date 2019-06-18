import os


# folder structure
def list_files(fileFolderPath):
    dirName = ''
    for root, dirs, files in os.walk(fileFolderPath):
        if (len(dirs) == 1) and (len(files) == 1):
            dirName = dirs[0]
            break
        elif (len(dirs) != 0) and (len(files) > 1):
            return "<h3> Project Folder Structure </h3> <div id='folder_struct'>" \
                   "<p>Please put all your files in a folder and zip it afterword.</p></div>"
        elif len(dirs) > 1:
            return "<h3> Project Folder Structure </h3> <div id='folder_struct'>" \
                   "<p>There are more than one folders in the zip file. " \
                   "Please zip them in one folder and try again.</p></div>"

    path = fileFolderPath + dirName
    folderStructureStr = "<h3> Project Folder Structure </h3> <div id='folder_struct'>"
    for root, dirs, files in os.walk(path):
        level = root.replace(fileFolderPath, '').count(os.sep)
        indent = '&nbsp' * 12 * level
        folderStructureStr += ('<p>{}{}/</p>'.format(indent, os.path.basename(root)))
        subindent = '&nbsp' * 12 * (level + 1)
        for f in files:
            folderStructureStr += ("<p>{}{}</p>".format(subindent, f))
    folderStructureStr += "</div>"
    return folderStructureStr

# end folder structure