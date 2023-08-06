import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.1.post143"
version_tuple = (0, 1, 1, 143)
try:
    from packaging.version import Version as V
    pversion = V("0.1.1.post143")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.1.post17"
data_version_tuple = (0, 1, 1, 17)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.1.post17")
except ImportError:
    pass
data_git_hash = "cf8a85b7a25df497a9669cf0ad7cf3515eb4057e"
data_git_describe = "0.1.1-17-gcf8a85b"
data_git_msg = """\
commit cf8a85b7a25df497a9669cf0ad7cf3515eb4057e
Merge: e67f8e3 3ac62d6
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Tue Feb 15 15:46:29 2022 +0100

    Merge pull request #433 from silabs-halfdan/clic_if_update
    
    Updated CLIC interface signals and added them to documentation

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
