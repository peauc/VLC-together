import traceback
import logging
import sys

from server.src.server import Server

def set_log():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def main():
    """Main function for the VLCTogether server."""
    set_log()
    try:
        Server().run()
    except Exception as e:
        print(traceback.format_exc())


if __name__ == '__main__':
    main()
