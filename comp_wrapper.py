import pathlib

def context_is_windows() -> bool:
    """Returns True or False if python context returns a WindowsPath object
    TODO: Check if pathlib.PurePath() returns a Unix path or a Windows path in cygwin
        Replace below code if so"""
    return type(pathlib.Path().resolve()) == pathlib.WindowsPath

def context_is_unix() -> bool:
    """Returns True or False if python context returns a PosixPath object
    TODO: Check if pathlib.PurePath() returns a Unix path or a Windows path in cygwin
        Replace below code if so"""
    return type(pathlib.Path().resolve()) == pathlib.PosixPath

def path_is_unix(path : str) -> bool:
    return path[0] == '/'

def path_is_windows(path : str) -> bool:
    return (path[1:3] == ':\\') or (path[1:3] == ':/')

def path_is_relative(path : str) -> bool:
    return (path[0:2] == './') or (path[0:2] == '.\\') or (path[0:3] == '../') or (path[0:3] == '..\\')

def path_type(path : str) -> str:
    """Returns 'windows', 'unix', 'relative', or 'unknown'"""
    if path_is_unix(path):
        return 'unix'
    elif path_is_windows(path):
        return 'windows'
    elif path_is_relative(path):
        return 'relative'
    else:
        return 'unknown'

def auto_convert_path(path : str) -> str:
    """Determines the context and path type, then converts accordingly.
    Currently only handles cygwin drive paths."""
    if context_is_unix() and (path_type(path) == 'unix'):
        return path
    elif context_is_windows() and (path_type(path) == 'windows'):
        return path
    elif context_is_unix() and (path_type(path) == 'windows'):
        # convert windows path to unix
        p = pathlib.PureWindowsPath(path)
        
        return None
    elif context_is_windows() and (path_type(path) == 'unix'):
        # convert unix path to windows
        if 'cygdrive' in path:
            temp = path.split('/cygdrive/')
            drive_letter = temp[0]
            file_path = temp[2:]
            win_path = pathlib.PureWindowsPath(drive_letter + ':' + file_path)
            return str(win_path)
        else:
            raise ValueError('cygdrive not in unix path ' + path)
    elif path_type(path) == 'relative':
        # convert to context
        return None
    else:
        raise ValueError('Unknown file path for ' + path)