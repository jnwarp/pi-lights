import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Choose the Pi')

    parser.add_argument('--door', dest='piPlatform', action='store_const',
        const='door',
        help='runs the "door" Raspberry Pi')
    parser.add_argument('--lights', dest='piPlatform', action='store_const',
        const='lights',
        help='runs the "lights" Raspberry Pi')

    args = parser.parse_args()
    print(args.piPlatform)
