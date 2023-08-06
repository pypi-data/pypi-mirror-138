'''
...
'''

def get_directory() -> str:
    '''
    Get the directory of the current file.

    Returns:
    * str - path
    '''
    return "\\".join(__file__.split("\\")[:-2])
