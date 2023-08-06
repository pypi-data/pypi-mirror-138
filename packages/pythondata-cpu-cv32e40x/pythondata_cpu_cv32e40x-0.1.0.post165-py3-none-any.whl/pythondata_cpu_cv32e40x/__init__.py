import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post165"
version_tuple = (0, 1, 0, 165)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post165")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post39"
data_version_tuple = (0, 1, 0, 39)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post39")
except ImportError:
    pass
data_git_hash = "ebbe1ecac502a5905347eee0e7430b6357710235"
data_git_describe = "0.1.0-39-gebbe1ec"
data_git_msg = """\
commit ebbe1ecac502a5905347eee0e7430b6357710235
Merge: b798165 3b7eba9
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Mon Feb 14 15:12:48 2022 +0100

    Merge pull request #429 from silabs-halfdan/finalized_core_interface
    
    Finalized core interface

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
