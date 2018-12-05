from vlc import VLC
from Constants import Constants

def main():
    vlc = VLC()
    vlc.add(Constants.TEST_FILE)
    vlc.play()

if __name__ == '__main__':
    main()
