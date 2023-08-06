'''
Module for working with "cfg" files

What does it have:
* class `Cfg`
'''
from .basic import start_with, split

class Cfg:
    '''
    Class for working with cfg files

    Parameters:
    * `path`: str - the path to the cfg file.

    Attributes:
    * `parameters`: dict - parameters with sections.

    Methods:
    * `open`
    * `get`

    Supported operations:
    * `self[i]` - getting data using an index.
    '''
    def __init__(self, path:str):
        self.parameters = {}

        with open(path, "r", encoding="utf-8") as file:
            section = None
            ignore = False
            for line in file.readlines():
                if start_with(line, ["!", "//"]): continue
                elif start_with(line, "/*"): ignore = True
                elif "*/" in line: 
                    ignore = False
                    continue
                    
                if start_with(line, "["): section = line[1:].split("]")[0]
                else: 
                    if not section is None and not ignore:
                        line = line.split("=")
                        # Проверка существования секции в списке.
                        try: self.parameters[section] 
                        except: self.parameters[section] = {}

                        if start_with(line[1], ["'", '"']): 
                            self.parameters[section][line[0]] = split(line[1], ["'", '"'])[1]
                        else: self.parameters[section][line[0]] = split(line[1], ["//", "!"])[0]
                    elif not ignore:
                        line = line.split("=")
                        if start_with(line[1], ["'", '"']): 
                            self.parameters[line[0]] = split(line[1], ["'", '"'])[1]
                        else: self.parameters[line[0]] = split(line[1], ["//", "!"])[0]

    def open(path:str):
        '''
        This is an alias to `self.__init__()`.

        Parameters:
        * `path`: str - the path to the cfg file.

        Returns:
        * Cfg - instance of the class.
        '''
        return Cfg(path)

    def get(self, key:int):
        '''
        Getting a parameter or section.

        Parameters:
        * `key`: int - the key of the parameter or section.

        Returns:
        * str|dict - parameter or section.
        '''
        return self.__getitem__(key)

    def __getitem__(self, key):
        return self.parameters[key]
