import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.1.post135"
version_tuple = (0, 1, 1, 135)
try:
    from packaging.version import Version as V
    pversion = V("0.1.1.post135")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.1.post9"
data_version_tuple = (0, 1, 1, 9)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.1.post9")
except ImportError:
    pass
data_git_hash = "1d56e0e1eae6925c62fbbf2fea8a3fe155ac802a"
data_git_describe = "0.1.1-9-g1d56e0e"
data_git_msg = """\
commit 1d56e0e1eae6925c62fbbf2fea8a3fe155ac802a
Merge: ebbe1ec 21bc43e
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Tue Feb 15 07:59:49 2022 +0100

    Merge pull request #430 from silabs-oysteink/silabs-oysteink_UM-CSR-1
    
    Doc only: User manual CSR updates

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
