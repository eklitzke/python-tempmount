import os
import subprocess
import tempfile

__author__ = 'Evan Klitzke <evan@eklitzke.org>'

class TempMount(object):
    """Context manager for a temporary mount

    This handles the logic of creating a temporary directory and mounting a
    device to that directory. This allows you to then access the mounted
    directoy using Python's with statement. The device will intelligently be
    unmounted and the temporary directory cleaned up when the block is
    exited."""

    def __init__(self, device, loop=False):
        self.device = device
        self.loop = loop

    def __enter__(self):
        self.tempdir = tempfile.mkdtemp()
        prefix = ['mount']
        if self.loop:
            prefix += ['-o', 'loop']
        subprocess.check_call(prefix + [self.device, self.tempdir])

    def __exit__(self, exc_type, value, traceback):
        """Never swallows exceptions."""
        subprocess.call(['umount', self.tempdir])
        os.rmdir(self.tempdir)

__all__ = ['TempMount']
