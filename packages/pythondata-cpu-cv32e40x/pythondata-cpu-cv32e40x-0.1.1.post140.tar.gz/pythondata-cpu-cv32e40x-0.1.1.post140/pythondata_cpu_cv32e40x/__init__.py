import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.1.post140"
version_tuple = (0, 1, 1, 140)
try:
    from packaging.version import Version as V
    pversion = V("0.1.1.post140")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.1.post14"
data_version_tuple = (0, 1, 1, 14)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.1.post14")
except ImportError:
    pass
data_git_hash = "e67f8e3449ba3c8fef4f3028fc6ea154efd824fa"
data_git_describe = "0.1.1-14-ge67f8e3"
data_git_msg = """\
commit e67f8e3449ba3c8fef4f3028fc6ea154efd824fa
Merge: 9de70dc d88a9a0
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Tue Feb 15 15:17:19 2022 +0100

    Merge pull request #432 from Silabs-ArjanB/ArjanB_doccl
    
    CLIC related documentation updates

"""

# Tool version info
tool_version_str = "0.0.post126"
tool_version_tuple = (0, 0, 126)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post126")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
