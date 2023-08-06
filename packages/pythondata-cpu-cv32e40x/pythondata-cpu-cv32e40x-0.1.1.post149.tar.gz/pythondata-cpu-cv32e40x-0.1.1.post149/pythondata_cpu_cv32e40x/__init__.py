import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.1.post149"
version_tuple = (0, 1, 1, 149)
try:
    from packaging.version import Version as V
    pversion = V("0.1.1.post149")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.1.post23"
data_version_tuple = (0, 1, 1, 23)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.1.post23")
except ImportError:
    pass
data_git_hash = "9bba199df0fed5f48dd093040d36a0a3eea3446f"
data_git_describe = "0.1.1-23-g9bba199"
data_git_msg = """\
commit 9bba199df0fed5f48dd093040d36a0a3eea3446f
Merge: 34bb6aa 73c0aa6
Author: Henrik Fegran <henrik.fegran@silabs.com>
Date:   Wed Feb 16 11:09:29 2022 +0100

    Merge pull request #437 from openhwgroup/silabs-hfegran-release_yaml-update
    
    Update release.yaml

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
