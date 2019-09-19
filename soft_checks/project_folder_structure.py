import os
# folder structure

def list_files(fileLocationStr):
    fileLocationStr = fileLocationStr.rstrip(os.sep)
    def path_to_dict(path):
        d = {'name': os.path.basename(path)}
        if os.path.isdir(path):
            children = [path_to_dict(path+"/"+x) for x in os.listdir(path)]
            d['itemStyle'] = {'color': 'rgb(233,97,111)'}
            if len(children) > 0:
                d['children'] = children
        else:
            d['value'] = os.path.getsize(path)
            d['itemStyle'] = {'color': 'rgb(243,165,130)'}
        return d
    return path_to_dict(fileLocationStr)["children"]
# end folder structure

