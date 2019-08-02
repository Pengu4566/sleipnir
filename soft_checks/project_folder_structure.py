import os
from functools import reduce
# folder structure
def list_files(fileLocationStr):
   folderStructureStr = {}
   fileLocationStr = fileLocationStr.rstrip(os.sep)
   start = fileLocationStr.rfind(os.sep) + 1
   for path, dirs, files in os.walk(fileLocationStr):
       folders = path[start:].split(os.sep)
       subdir = dict.fromkeys(files)
       parent = reduce(dict.get, folders[:-1], folderStructureStr)
       parent[folders[-1]] = subdir
   return folderStructureStr
# end folder structure