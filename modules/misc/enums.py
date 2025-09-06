import winreg
from enum import Enum, auto


class RegistryType(Enum):
    REG_SZ = winreg.REG_SZ
    REG_DWORD = winreg.REG_DWORD
    REG_BINARY = winreg.REG_BINARY
    REG_QWORD = winreg.REG_QWORD
    REG_MULTI_SZ = winreg.REG_MULTI_SZ
    REG_EXPAND_SZ = winreg.REG_EXPAND_SZ


class WindowsActivationMethod(Enum):
    MASSGRAVE = auto()
    ACTIVATION_KEY = auto()


# very useless enum
class OpenModes(Enum):
    """
    ### Description of the `mode` param for Python's `open()` function:

    `mode` is a string that specifies the mode in which the file is opened.

    It defaults to `'r'` which means open for reading in text
    mode.

    Other common values are:
    - `'w'` for writing (truncating the file if it already exists)
    - `'x'` for creating and writing to a new file
    - `'a'` for appending

    All values:
    - `'r'`: open for reading (default)
    - `'w'`: open for writing, truncating the file first
    - `'x'`: create a new file and open it for writing
    - `'a'`: open for writing, appending to the end of the file if it exists
    - `'b'`: binary mode
    - `'t'`: text mode (default)
    - `'+'`: open a disk file for updating (reading and writing)
    """
    READ = 'r'
    WRITE = 'w'
    CREATE_AND_WRITE = 'x'
    APPEND = 'a'
    BINARY = 'b'
    TEXT = 't'
    READ_WRITE_UPDATE = '+'
