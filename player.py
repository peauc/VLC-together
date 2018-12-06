from vlc import VLC

class Player:
    def __init__(self):
        self.vlc = VLC()

    def add(self, filepath):
        self.vlc.add(filepath)

    def __pause(self):
        self.vlc.pause()
