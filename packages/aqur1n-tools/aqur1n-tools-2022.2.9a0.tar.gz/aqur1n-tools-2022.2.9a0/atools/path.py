'''
Easy work with paths.

What does it have:
* class `Path`
* class `File`

## MIT License

Copyright (c) 2022 aqur1n-lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from sys import platform
import os.path

class File:
    '''
    Initializes the file class.

    Parameters:
    * `file`: str - file name.
    * `path`: str|None - path to file.

    Attributes:
    * `file`: list - full file name.
    * `name`: str - file name.
    * `extension`: str|None - file extension.
    '''
    def __init__(self, file:str, path:str|None=None):
        self.path = path
        self.file = file.split(".")
        self.name = self.file[0]
        try: self.extension = self.file[1]
        except: self.extension = None

class Win_path:
    '''
    Initializes the path class.

    Parameters:
    * `path`: str - full path.

    Attributes:
    * `all`: list - full path.
    * `file`: atools.path.file|None - file.
    * `directory`: list - directory to file.
    * `disk`: str|None - the drive letter.

    Supported operations:
    * `str(x)` - returns all path
    * `x + y` - connects the paths into one.
    '''
    def __init__(self, path:str):
        self.all = path.replace("/", "\\").split("\\")

        if os.path.isfile(path): 
            self.file = File(self.all[len(self.all)-1])
            self.directory = self.all[:-1]
        else:
            self.file = None
            self.directory = self.all

        try: 
            if self.directory[0][-1:] == ":": 
                self.disk = self.all[0]
            else: self.disk = None
        except: pass

    def add(self, path:str) -> None:
        '''
        Adds another path to the path.

        Parameters:
        * `path`: str - path.
        '''
        self = self.__add__(Win_path(path))
    
    def __str__(self): return "\\".join(self.all)

    def __add__(self, other): 
        if isinstance(other, Win_path):
            directory = self.directory
            for i in other.directory:
                if i[-1:] == ":": pass
                else: directory.append(i)
            return Win_path("\\".join(directory))

if platform == "win32": Path = Win_path
else: print("This platform has not been checked for errors in this module.")
