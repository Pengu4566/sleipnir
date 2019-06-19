import os


# folder structure
def list_files(main_location):
    dirName = ''
    folder = "/".join(main_location.split("/")[:-1])
    print(folder)
    for root, dirs, files in os.walk(folder):
        if (len(dirs) == 1) and (len(files) == 0):
            break
        elif (len(dirs) != 0) and (len(files) > 0):
            return "<h3> Project Folder Structure </h3> <div id='folder_struct'>" \
                   "<p>Please put all your files in a folder and zip it afterword.</p></div>"
        elif len(dirs) > 1:
            return "<h3> Project Folder Structure </h3> <div id='folder_struct'>" \
                   "<p>There are more than one folders in the zip file. " \
                   "Please zip them into one folder and try again.</p></div>"


    folderStructureStr = "<h3> Project Folder Structure </h3> <div id='folder_struct'>"
    for root, dirs, files in os.walk(main_location):
        level = root.replace(folder, '').count(os.sep)
        indent = '&nbsp' * 12 * level
        folderStructureStr += ('<p>{}{}/</p>'.format(indent, os.path.basename(root)))
        subindent = '&nbsp' * 12 * (level + 1)
        for f in files:
            folderStructureStr += ("<p>{}{}</p>".format(subindent, f))
    folderStructureStr += "</div>"
    return folderStructureStr

# end folder structure