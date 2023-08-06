import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.1.post145"
version_tuple = (0, 1, 1, 145)
try:
    from packaging.version import Version as V
    pversion = V("0.1.1.post145")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.1.post19"
data_version_tuple = (0, 1, 1, 19)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.1.post19")
except ImportError:
    pass
data_git_hash = "705ed1905461e4b9e0af7d727d62008c092e8ca0"
data_git_describe = "0.1.1-19-g705ed19"
data_git_msg = """\
commit 705ed1905461e4b9e0af7d727d62008c092e8ca0
Merge: cf8a85b e462c8d
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Wed Feb 16 07:36:58 2022 +0100

    Merge pull request #435 from silabs-halfdan/mcycle_in_integration_manual
    
    Added missing signal in user manual integration guide

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
