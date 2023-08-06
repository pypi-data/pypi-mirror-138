import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.1.post151"
version_tuple = (0, 1, 1, 151)
try:
    from packaging.version import Version as V
    pversion = V("0.1.1.post151")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.1.post25"
data_version_tuple = (0, 1, 1, 25)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.1.post25")
except ImportError:
    pass
data_git_hash = "b6214af00c698ef48e93fc040f733673b3590c5b"
data_git_describe = "0.1.1-25-gb6214af"
data_git_msg = """\
commit b6214af00c698ef48e93fc040f733673b3590c5b
Merge: 9bba199 28e2db9
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Wed Feb 16 13:40:26 2022 +0100

    Merge pull request #438 from silabs-oysteink/silabs-oysteink-UM-CSR-2
    
    Doc only: Tinfo and typos

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
