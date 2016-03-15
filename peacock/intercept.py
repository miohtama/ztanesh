# Copyright (c) 2011 Joshua D. Bartlett
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import array
import fcntl
import os
import pty
import select
import signal
import sys
import termios
import tty

class Interceptor(object):
    '''
    This class does the actual work of the pseudo terminal. The spawn()
          function is the main entrypoint.
    '''

    def __init__(self):
        self.master_fd = None

    def spawn(self, argv=None):
        '''
        Create a spawned process.
        Based on the code for pty.spawn().
        '''
        assert self.master_fd is None
        if not argv:
            argv = [os.environ['SHELL']]

        self.isatty = os.isatty(pty.STDOUT_FILENO)
        pid, master_fd = pty.fork()
        self.master_fd = master_fd
        if pid == pty.CHILD:
            os.execlp(argv[0], *argv)

        old_handler = signal.signal(signal.SIGWINCH, self._signal_winch)
        restore = 0
        if self.isatty:
            try:
                mode = tty.tcgetattr(pty.STDIN_FILENO)
                tty.setraw(pty.STDIN_FILENO)
                restore = 1

            except tty.error:    # This is the same as termios.error
                pass

        self._init_fd()
        try:
            self._copy()
        except (IOError, OSError):
            if restore:
                tty.tcsetattr(pty.STDIN_FILENO, tty.TCSAFLUSH, mode)

        os.close(master_fd)
        self.master_fd = None
        signal.signal(signal.SIGWINCH, old_handler)

    def _init_fd(self):
        '''
        Called once when the pty is first set up.
        '''
        self._set_pty_size()

    def _signal_winch(self, signum, frame):
        '''
        Signal handler for SIGWINCH - window size has changed.
        '''
        self._set_pty_size()

    def _set_pty_size(self):
        '''
        Sets the window size of the child pty based on the window size of
             our own controlling terminal.
        '''
        assert self.master_fd is not None

        # Get the terminal size of the real terminal, set it on the pseudoterminal.
        buf = array.array('h', [0, 0, 0, 0])
        if self.isatty:
            fcntl.ioctl(pty.STDOUT_FILENO, termios.TIOCGWINSZ, buf, True)
        else:
            # set default size...
            buf[0] = 25
            buf[1] = 80

        fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, buf)

    def _copy(self):
        '''
        Main select loop. Passes all data to self.master_read() or
              self.stdin_read().
        '''
        assert self.master_fd is not None
        master_fd = self.master_fd

        cached_master_data = ''

        while 1:
            try:
                timeout = 0.05 if cached_master_data else 0

                rfds, wfds, xfds = select.select([master_fd,
                      pty.STDIN_FILENO], [], [], timeout)
            except select.error, e:
                if e[0] == 4:   # Interrupted system call.
                    continue

            full_buffer = False
            if master_fd in rfds:
                data = os.read(self.master_fd, 1024)
                full_buffer = len(data) == 1024

                master_data = cached_master_data + data

            else:
                master_data = cached_master_data

            if master_data:
                cached_master_data = ''
                lines = master_data.splitlines(True)

                for i in lines:
                    if not full_buffer or i.endswith('\n'):
                        self.master_read(i)

                    else:
                        cached_master_data = i

            if pty.STDIN_FILENO in rfds:
                data = os.read(pty.STDIN_FILENO, 1024)
                self.stdin_read(data)

    def write_stdout(self, data):
        '''
        Writes to stdout as if the child process had written the data.
        '''
        if not self.isatty:
            data = data.replace('\r\n', '\n')

        os.write(pty.STDOUT_FILENO, data)

    def write_master(self, data):
        '''
        Writes to the child process from its controlling terminal.
        '''
        master_fd = self.master_fd
        assert master_fd is not None
        while data != '':
            n = os.write(master_fd, data)
            data = data[n:]

    def master_read(self, data):
        '''
        Called when there is data to be sent from the child process back to
             the user.
        '''
        data = self.do_process(data)
        self.write_stdout(data)

    def do_process(self, data):
        return data

    def stdin_read(self, data):
        '''
        Called when there is data to be sent from the user/controlling
             terminal down to the child process.
        '''
        self.write_master(data)
