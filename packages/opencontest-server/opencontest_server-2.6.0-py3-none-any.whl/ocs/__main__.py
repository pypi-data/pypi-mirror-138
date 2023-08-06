#!/usr/bin/python

import sys
import os
import logging
from http.server import ThreadingHTTPServer

from ocs.args import args
from ocs.server import Server


def main():
    """Run the server"""
    
    httpd = ThreadingHTTPServer(('', args.port), Server)
    logging.info('Starting server')
    httpd.serve_forever()


if __name__ == '__main__':
    sys.exit(main())
