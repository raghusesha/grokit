"""
File: grokit.py
Author: Raghu Sesha Iyengar (raghu.sesha@gmail.com)
Description: The main file for grokit.
"""
import sys
import os
import optparse
from textwrap import dedent
from utils import start_stop_server, validate_path, check_and_copy_tools, ospath, index_for_project

class MyParser(optparse.OptionParser):
    def format_epilog(self, formatter):
        return self.epilog

desc =\
"""
The primary purpose of this tool is to help you setup OpenGrok *quickly*
Typical Usage:
    1. Setup opengrok for a project
    grokit.exe --ppath=<path to project source> --action=setup

    2. Start/Stop Tomcat server
    grokit.exe --action=start
    grokit.exe --action=stop

    Please send your comments / suggestions to raghu.sesha@gmail.com
"""

ppath_help="""
Path to the location of source that should be cross-referenced
NOTE: Each directory inside this will be considered as a opengrok project
So, if you want single project, make sure that PPATH has only one child directory that contains all source files"""

action_help="""
Action to be performed.  Can be one of (setup|start|stop):
- setup: Setup opengrok for the project source present at PPATH.
- start: Start the tomcat server
- stop:  Stop the tomcat server"""

def setup(envs, opts):
    if opts.action == 'start' or opts.action == 'stop':
        start_stop_server(envs, opts.action)
    elif opts.action == 'setup':
        envs['ppath'] = ospath(os.path.expanduser(opts.ppath).rstrip("/").rstrip("\\"))
        if (index_for_project(envs, "setup") == True):
            print "Setup completed successfully"
        else:
            print "Setup failed to complete!"
    elif opts.action == 'reindex':
        envs['ppath'] = ospath(os.path.expanduser(opts.ppath).rstrip("/").rstrip("\\"))
        if (index_for_project(envs, "reindex") == True):
            print "Reindex completed successfully"
        else:
            print "Reindex failed to complete!"
    

def main(sysargv):
    envs = {'tpath': '', 'ppath': '', 'cpath':''}
    envs['ppath'] = ''
    envs['cpath'] = ospath(os.path.dirname(os.path.realpath(__file__)))
    envs['tpath'] = ospath(envs['cpath']+"/grokit_files")
    parser = MyParser(epilog=desc)
    parser.add_option('--ppath', help=dedent(ppath_help), dest='ppath', action='store')
    parser.add_option('--action', help=dedent(action_help), dest='action', action='store')

    (opts, args) = parser.parse_args()
    if opts.action not in ['start', 'stop', 'setup', 'reindex']:
        print "Should provide one of (setup|start|stop|reindex) for action"
        return
    if opts.action in ['setup'] and opts.ppath == None:
        print "--ppath is mandatory when --action=setup"
        return

    setup(envs, opts)


if __name__ == "__main__":
    basic_help =\
"""
The primary purpose of this tool is to help you setup OpenGrok *quickly*
Run with -h option to get more help:
    grokit.exe -h
"""
    if len(sys.argv) == 1:
        print basic_help
    else:
        main(sys.argv)

