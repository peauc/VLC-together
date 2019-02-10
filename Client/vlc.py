# Thanks Marios Zindilis
# For his article and his code https://zindilis.com/blog/2016/10/23/control-vlc-with-python.html

import logging
import socket
import subprocess
import os


class VLC:

    # region Properties
    @property
    def commands(self):
        return self.__commands
# endregion

    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = 8888
        self.SCREEN_NAME = f'vlc{self.PORT}'

        cmd = subprocess.run(
            ['screen', '-ls', self.SCREEN_NAME,],
            stdout=subprocess.DEVNULL
        )
        if cmd.returncode:
            logging.debug(f"screen is running return code {cmd.returncode}")
            cmd = subprocess.run([
                'screen',
                '-dmS',
                self.SCREEN_NAME,
#                'vlc'
                '/Applications/VLC.app/Contents/MacOS/VLC',
                '-I',
                'rc',
                '--rc-host',
                '%s:%s' % (self.HOST, self.PORT)
            ])
            logging.debug(f"VLC is running, return code {cmd.returncode}")
        logging.debug(f"VLC is listening on HOST:{self.HOST} PORT:{self.PORT} {os.linesep}")
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCK.connect((self.HOST, self.PORT))
        logging.debug(f"Connection successful to {self.HOST}:{self.PORT}")

    def x(self, cmd):
        '''Prepare a command and send it to VLC'''
        logging.debug(f'Sending {cmd} to vlc')
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode()
        self.SOCK.sendall(cmd)
