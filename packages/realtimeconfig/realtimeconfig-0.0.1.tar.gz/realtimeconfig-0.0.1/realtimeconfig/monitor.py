import sys
from realtimeconfig import get_queue, startup
import argparse


def main():
    namespace = parser.parse_args(sys.argv[1:])
    startup(namespace.key, namespace.url)
    
    queue = get_queue()

    while True:
        k, v = queue.get()
        print(k, v, sep="\t")


parser = argparse.ArgumentParser(description='realtimeconfig-monitor')
parser.add_argument('--key',
                    required=True,
                    help='Your realtimeconfig API key')
parser.add_argument('--url',
                    default='wss://stream.realtimeconfig.com:1443/',
                    help='The realtimeconfig source.  Change this if you are using a proxy')


if __name__ == "__main__":
    main()
