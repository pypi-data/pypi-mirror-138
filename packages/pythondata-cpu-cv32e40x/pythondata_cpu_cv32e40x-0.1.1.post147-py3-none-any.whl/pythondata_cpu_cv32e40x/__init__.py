import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.1.post147"
version_tuple = (0, 1, 1, 147)
try:
    from packaging.version import Version as V
    pversion = V("0.1.1.post147")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.1.post21"
data_version_tuple = (0, 1, 1, 21)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.1.post21")
except ImportError:
    pass
data_git_hash = "34bb6aa5261e8a1464125bfee1fef8015b3f48f4"
data_git_describe = "0.1.1-21-g34bb6aa"
data_git_msg = """\
commit 34bb6aa5261e8a1464125bfee1fef8015b3f48f4
Merge: 705ed19 276b3de
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Wed Feb 16 10:05:41 2022 +0100

    Merge pull request #436 from openhwgroup/silabs-hfegran-release-notes-cfg
    
    Create release.yaml (Release notes configuration)

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
