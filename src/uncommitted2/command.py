"""The 'uncommitted2' command-line tool itself."""

import os
import sys
from optparse import OptionParser
from subprocess import Popen, PIPE

from . import scanner

USAGE = '''usage: %prog [options] path [path...]

  Checks the status of all Version Control repositories beneath the paths
  given on the command line.  Any repositories with uncommitted changes
  are printed to standard out, along with the status of the files inside.'''

def main():
    parser = OptionParser(usage=USAGE)
    parser.add_option('-l', '--locate', dest='use_locate', action='store_true',
                      help='use locate(1) to find repositories')
    parser.add_option('-v', '--verbose', action='store_true',
                      help='show repository status')
    parser.add_option('-a', '--all', action='store_true', dest='print_all',
                      help='print every repository whether changed or not')
    parser.add_option('-w', '--walk', dest='use_walk', action='store_true',
                      help='manually walk file tree to find repositories')
    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        exit(2)

    if options.use_locate and options.use_walk:
        sys.stderr.write('Error: you cannot specify both "-l" and "-w"\n')
        exit(2)

    if options.use_walk:
        find_repos = scanner.find_repos_by_walking
    else:
        find_repos = scanner.find_repos_with_locate

    repos = set()

    for path in args:
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            sys.stderr.write('Error: not a directory: %s\n' % (path,))
            continue
        repos.update(find_repos(path))

    repos = sorted(repos)
    scanner.scan(repos, options.print_all, options.verbose)

if __name__ == '__main__':
    main()