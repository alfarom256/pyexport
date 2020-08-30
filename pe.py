import pefile
from pefile import PEFormatError

def get_exports_from_file(fname):
    retval = []
    pe = None
    try:
        pe = pefile.PE(fname)
    except PEFormatError:
        print("DLL pe format error: " + fname)
        return
    except Exception as ex:
        print("Error reading dll: " + str(ex))
        return
    try:
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            if exp.name is None:
                continue
            retval.append((hex(pe.OPTIONAL_HEADER.ImageBase + exp.address), bytes(exp.name).decode("utf-8"), exp.ordinal))
    except AttributeError as ex:
        print("DLL has no export table: " + fname)
        return
    except Exception as ex:
        print("Error reading dll " + fname +  ": " + str(ex))

    return retval