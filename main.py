from vlc import VLC
from Constants import Constants

def main():
    vlc = VLC()

    vlc.add(Constants.TEST_FILE)
    vlc.pause()
    vlc.play()
    while 1:
        pass

if __name__ == '__main__':
    main()
