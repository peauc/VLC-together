import sys
import logging

from .client import Client

def setup_logging():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def main():
    """Main function for VLCTogether's client."""
    setup_logging()
    Client().run()


if __name__ == '__main__':
    main()
