import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.1.post155"
version_tuple = (0, 1, 1, 155)
try:
    from packaging.version import Version as V
    pversion = V("0.1.1.post155")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.1.post29"
data_version_tuple = (0, 1, 1, 29)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.1.post29")
except ImportError:
    pass
data_git_hash = "380b9fd6dff586d332886e0eaa875e9aafa54ca6"
data_git_describe = "0.1.1-29-g380b9fd"
data_git_msg = """\
commit 380b9fd6dff586d332886e0eaa875e9aafa54ca6
Merge: b6214af 2b0d849
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Wed Feb 16 14:11:58 2022 +0100

    Merge pull request #439 from Silabs-ArjanB/ArjanB_docm
    
    Fixing mtvec and mtvt alignment requirements. Better links for spec v…

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
