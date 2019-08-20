# used Python 3.7

import etcd3
from ab_incrementor import ABIncrementor
from ab_incrementor_test import ABIncrementorTest
from watcher import Watcher
from argparse import ArgumentParser

class ClientType:
    WATCHER = 0,
    COMMITER = 1


def create_test(etcd_client, client_type: int, test_name: str):
    if test_name == 'ab-incrementor':
        if client_type == ClientType.WATCHER:
            return ABIncrementorTest()

        elif client_type == ClientType.COMMITER:
            return ABIncrementor(etcd_client)

    raise Exception('Undefined client type')


def main():
    parser = ArgumentParser()

    parser.add_argument(
        '--type',
        help='Start me as etcd watcher or commiter',
        choices=['watcher', 'commiter', 'mrproper'],
        required=True)

    parser.add_argument(
        '--test',
        help='Select the test',
        choices=['ab-incrementor'],
        required=True
    )

    parser.add_argument(
        '--host',
        help='IP address of machine with the etcd',
        default='127.0.0.1')

    parser.add_argument(
        '--port',
        type=int,
        help='Peer port to connect to etcd',
        default=2379
    )

    args = parser.parse_args()
    etcd_client = etcd3.client(host=args.host, port=args.port)

    if args.type == 'watcher':
        watch_client = Watcher(etcd_client, create_test(etcd_client, ClientType.WATCHER, args.test))
        watch_client.start_watcher()
        watch_client.run()

    elif args.type == 'commiter':
        data_provider = create_test(etcd_client, ClientType.COMMITER, args.test)
        data_provider.run()

    else:
        etcd_client.delete_prefix('/')

    print('done')


if __name__ == '__main__':
    main()
