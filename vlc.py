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
        self.SCREEN_NAME = 'vlc'
        self.HOST = '192.168.0.138'
        self.PORT = 8888
        self.__commands = [
            "pause",
            "play",
            "stop",
            "prev",
            "next",
            "add",
            "enqueue",
            "clear",
            "shutdown",
        ]

        cmd = subprocess.run(
            ['screen', '-ls', self.SCREEN_NAME,],
            stdout=subprocess.DEVNULL
        )
        logging.debug("subprocess screen is running")
        if cmd.returncode:
            logging.debug("subprocess vlc is runing")
            subprocess.run([
                'screen',
                '-dmS',
                self.SCREEN_NAME,
                'vlc',
                '-I',
                'rc',
                '--rc-host',
                '%s:%s' % (self.HOST, self.PORT)
            ])
        logging.debug(f"Listening on HOST:{self.HOST} PORT:{self.PORT} {os.linesep}")

    def x(self, cmd):
        '''Prepare a command and send it to VLC'''
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode()
        self.SOCK.sendall(cmd)
