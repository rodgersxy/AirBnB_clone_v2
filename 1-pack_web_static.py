#!/usr/bin/python3
"""
Compresses the web_static folder into a .tgz archive.
Returns the path to the created archive or None on failure.
"""
import os
from fabric.api import local, runs_once
from datetime import datetime


@runs_once
def do_pack():
    """
    .tgz the stattic file
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    now = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year,
        now.month,
        now.day,
        now.hour,
        now.minute,
        now.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, size))
    except Exception:
        output = None
    return output
