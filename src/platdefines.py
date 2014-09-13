"""
File: platdefines.py
Author: Raghu Sesha Iyengar (raghu.sesha@gmail.com)
Description: Contains all the platform specific definitions.
In an ideal world, to support on a new platform or different version of tools,
changing this file should be good enough
"""
import platform

if 'Windows' in platform.platform():
    import ntpath

    def convert_to_os_path(path):
        newpath = ntpath.normpath(path)
        return newpath
    if platform.architecture()[0] == '32bit':
        tools_dict = \
        { 'tomcat' : { 'file_name': 'apache-tomcat-8.0.8.tar.gz',
                       'file_size': 9098084,
                       'extract_path': 'script_path',
                       'extract_dir' : 'apache-tomcat-8.0.8',
                       'bin_file': '.bat'
                      },
          'opengrok' : { 'file_name' : 'opengrok-0.12.1.tar.gz',
                         'file_size': 14506193,
                         'extract_path': 'script_path',
                         'extract_dir' : 'opengrok-0.12.1',
                         'bin_file': 'opengrok.jar'
                        },
          'jre': { 'file_name' : 'jre-7u65-windows-i586.gz',
                   'file_size': 41912320,
                   'extract_path': 'script_path',
                   'extract_dir' : 'jre1.7.0_65',
                   'bin_file': 'java.exe'
                  },
          'ctags': { 'file_name' : 'exuberant-ctags.zip',
                     'file_size': 571849,
                     'extract_path': 'script_path',
                     'extract_dir' : 'ctags58',
                     'bin_file': 'ctags.exe'
                    }
        }
    elif platform.architecture()[0] == '64bit':
        tools_dict = \
        { 'tomcat' : { 'file_name': 'apache-tomcat-8.0.8.tar.gz',
                       'file_size': 9098084,
                       'extract_path': 'script_path',
                       'extract_dir' : 'apache-tomcat-8.0.8',
                       'bin_file': '.bat'
                      },
          'opengrok' : { 'file_name' : 'opengrok-0.12.1.tar.gz',
                         'file_size': 14506193,
                         'extract_path': 'script_path',
                         'extract_dir' : 'opengrok-0.12.1',
                         'bin_file': 'opengrok.jar'
                        },
          'jre': { 'file_name' : 'jre-7u65-windows-x64.gz',
                   'file_size': 43704320,
                   'extract_path': 'script_path',
                   'extract_dir' : 'jre1.7.0_65',
                   'bin_file': 'java.exe'
                  },
          'ctags': { 'file_name' : 'exuberant-ctags.zip',
                     'file_size': 571849,
                     'extract_path': 'script_path',
                     'extract_dir' : 'ctags58',
                     'bin_file': 'ctags.exe'
                    }
        }
elif 'Linux' in platform.platform():
    import posixpath
    def convert_to_os_path(path):
        newpath = posixpath.normpath(path)
        return newpath

    tools_dict = \
    { 'tomcat' : { 'file_name': 'apache-tomcat-8.0.8.tar.gz',
                   'file_size': 9098084,
                   'extract_dir' : 'apache-tomcat-8.0.8',
                   'bin_file': '.sh'
                  },
      'opengrok' : { 'file_name' : 'opengrok-0.12.1.tar.gz',
                     'file_size': 14506193,
                     'extract_dir' : 'opengrok-0.12.1',
                     'bin_file': 'opengrok.jar'
                    },
      'jre': { 'file_name' : 'jre-7u65-linux-x64.tar.gz',
               'file_size': 47005094,
               'extract_dir' : 'jre1.7.0_65',
               'bin_file': 'java'
              },
      'ctags': { 'file_name' : 'exuberant-ctags.tar',
                 'file_size': 921600,
                 'extract_dir' : 'ctags58',
                 'bin_file': 'ctags'
                }
    }

