import sys
import os

def Main():
    filetypes = []
    if len(sys.argv) >= 2:
        arg = sys.argv[1:]
        if '/?' in arg:
            print(f"usage: py ls.py [path] {{filetype}} \narguments: \n\t/? : returns this help message \n\t[path] : path to search for files\n\t{{filetype}} : any number of n filetypes that the program will show paths to")
            return
        path = arg[0]
        if len(arg) >= 2:
            for a in arg[1:]:
                filetypes.append(a)
    else:
        path = "."
    for root, dirs, files in os.walk(path):
        for f in files:
            if filetypes:
                if f.endswith(tuple(filetypes)):
                    print(os.path.join(root.replace(path, "{path}"), f))
            else:
                print(os.path.join(root.replace(path, "{path}"), f))
            
if __name__ == '__main__':
    Main()