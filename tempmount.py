"""
This module handles the use case of needing to mount a device to a temporary
directory to do some work on it. It is motivated by the fact that doing this is
a two step process: first you must create a temporary directory, and then you
must clean up that directory. Cleaning up is also a two step process: first you
must unmount the directory, and then you must remove the temporary directory.

Doing all of this from shell scripts can be somewhat cumbersome, since there are
two cases to check for. Mistakes in your shell script can cause devices to
remain mounted, /tmp pollution, etc. This is especially bad for loopback mounts,
since usually on Linux there is only a very small number of loopback devices
available (by default, anyway); if you make mistakes and leave some open, you
can run out of loopback devices rather quickly. By handling this in Python using
a with block, all of the messy details can be abstracted and handled
automatically. (This is of course only useful if you're mixing Python and shell
scripts already.)
"""

import os
import subprocess
import tempfile

__author__ = 'Evan Klitzke <evan@eklitzke.org>'

class TempMount(object):
    """Context manager for a temporary mount.

    This handles the logic of creating a temporary directory and mounting a
    device to that directory. This allows you to then access the mounted
    directoy using Python's with statement. The device will intelligently be
    unmounted and the temporary directory cleaned up when the block is
    exited."""

    def __init__(self, device, loop=False):
        """
        Args:
            @device: path of the device you want to mount, e.g. '/dev/sda1'
            @loop: True for a loopback mount, False otherwise (default is False)
        Returns:
            @path: the path of the temporary directory
        """
        self.device = device
        self.loop = loop

    def __enter__(self):
        self.tempdir = tempfile.mkdtemp()
        prefix = ['mount']
        if self.loop:
            prefix += ['-o', 'loop']
        subprocess.check_call(prefix + [self.device, self.tempdir])
        return os.path.realpath(self.tempdir)

    def __exit__(self, exc_type, value, traceback):
        """Never swallows exceptions."""
        subprocess.call(['umount', self.tempdir])
        os.rmdir(self.tempdir)

__all__ = ['TempMount']
