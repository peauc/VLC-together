# Thanks Marios Zindilis
# For his article and his code https://zindilis.com/blog/2016/10/23/control-vlc-with-python.html

import logging
import socket
import subprocess
import os
import time
import platform


class VLC:

    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = 8888
        self.SCREEN_NAME = f'vlc{self.PORT}'
        binary_name = 'vlc' if platform.platform() != 'Darwin' else '/Applications/VLC.app/Contents/MacOS/VLC'
        logging.debug(binary_name)
        # This will check if a screen with name self.SCREEN_NAME is running
        cmd = subprocess.run(
            ['screen', '-ls', self.SCREEN_NAME, ],
            stdout=subprocess.DEVNULL
        )
        
        # For now its either osx or linux
        logging.debug(f"Screen process {cmd.returncode}")
        if cmd.returncode:
            logging.debug(f"A screen has not been detected ")
            subprocess.run([
                'screen',
                '-dmS',
                self.SCREEN_NAME,
                binary_name,
                '-I',
                'rc',
                '--rc-host',
                '%s:%s' % (self.HOST, self.PORT)
            ])
        try:
            time.sleep(1)
            self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.SOCK.connect((self.HOST, self.PORT))
        except ConnectionRefusedError as e:
            logging.error(f"Connection failed to VLC's socket\n{e}")
            exit(1)
        logging.debug(f"Connection successful to vlc on {self.HOST}:{self.PORT}")

    def x(self, cmd):
        '''Prepare a command and send it to VLC'''
        logging.debug(f'user: {cmd}')
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode()
        self.SOCK.sendall(cmd)
