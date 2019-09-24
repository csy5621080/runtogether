import sys
import os
import argparse
import multiprocessing
import importlib
from runtogether.handles import Referee


parser = argparse.ArgumentParser()

parser.add_argument("-ro", "--path", help="app path.")

parser.add_argument("-mo", "--module", help='app file:app object.')

parser.add_argument("-ho", "--host", help="run host")

parser.add_argument("-po", "--port", help="run port")

parser.add_argument("-wo", "--workers", help="count of run worker.")

args = parser.parse_args()

if args.path:
    sys.path.append(args.path)
else:
    print('工作目录在%s' % os.path.abspath('.'))
    sys.path.append(os.path.abspath('.'))

if args.module:
    module, application = tuple(args.module.split(':'))
    app = getattr(importlib.import_module(module), application)
    # exec("from %s import %s as app" % tuple(args.module.split(':')))
else:
    raise argparse.ArgumentError('app relevant information must be provided.')

if args.host:
    host = args.host
else:
    host = '0.0.0.0'

if args.port:
    port = int(args.port)
else:
    port = 8899

if args.workers:
    workers = int(args.workers)
else:
    workers = multiprocessing.cpu_count() + 1


def main():
    server = Referee(app=app, workers=workers, host=host, port=port)
    server.run()


if __name__ == '__main__':
    main()