import os
# folder structure

def list_files(fileLocationStr):
    fileLocationStr = fileLocationStr.rstrip(os.sep)
    def path_to_dict(path):
        d = {'value': os.path.getsize(path)}
        d['name'] = os.path.basename(path)
        if os.path.isdir(path):
            children = [path_to_dict(path+"/"+x) for x in os.listdir(path)]
            relative_path = os.path.relpath(path, fileLocationStr)
            #d['path'] = relative_path
            #d['itemStyle'] = {'color': 'rgb(12, 192, 242)'}
            d['path'] = relative_path.replace("\\","/")
            if len(children) > 0:
                d['children'] = children
        else:
            d['value'] = os.path.getsize(path)
            d['name'] = os.path.basename(path)
            d['itemStyle'] = {'color': 'rgb(234,106,113)'}
            relative_path = os.path.relpath(path, fileLocationStr)
            #d['path'] = relative_path
            d['path'] = relative_path.replace("\\","/")
        return d
    return path_to_dict(fileLocationStr)["children"]
# end folder structure
