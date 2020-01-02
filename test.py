import os
import json
# folder structure

def list_files(fileLocationStr):
    fileLocationStr = fileLocationStr.rstrip(os.sep)
    def path_to_dict(path):
        d = {'value': 1000}
        d['name'] = os.path.basename(path)
        if os.path.isdir(path):
            children = [path_to_dict(path+"/"+x) for x in os.listdir(path)]
            relative_path = os.path.relpath(path, fileLocationStr)
            #d['path'] = relative_path
            d['path'] = relative_path.replace("\\","/")
            if len(children) > 0:
                d['children'] = children
        else:
            d['value'] = os.path.getsize(path)
            d['name'] = os.path.basename(path)
            relative_path = os.path.relpath(path, fileLocationStr)
            #d['path'] = relative_path
            d['path'] = relative_path.replace("\\","/")
        return d
    return path_to_dict(fileLocationStr)["children"]
# end folder structure


pathToDict = list_files("C:/Users/Michael/Dropbox/Business")

#print(pathToDict)
print(json.dumps(pathToDict))

