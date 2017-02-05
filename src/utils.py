"""
File: utils.py
Author: Raghu Sesha Iyengar (raghu.sesha@gmail.com)
Description: The core file for grokit.  Contains all the helper functions and logic
"""
import zipfile
import socket
import shutil
import os
import sys
import platform
import stat
import tarfile
import time
from bs4 import BeautifulSoup

import inspect
from compiler.ast import Const

DEBUG=False
if DEBUG==True:
    myself = lambda: inspect.stack()[1][3]
else:
    myself = lambda: ''

from platdefines import convert_to_os_path, tools_dict

def ospath(path):
    return convert_to_os_path(path)

def extract_war(src, dst):
    print myself()
    modified_war_dir = ospath(dst + "/modified_war")
    if os.path.isdir(modified_war_dir):
        for dirpath, dirnames, filenames in os.walk(modified_war_dir):
            for filename in filenames:
                os.chmod(os.path.join(dirpath, filename), stat.S_IWRITE)
        try:
            shutil.rmtree(modified_war_dir)
        except:
            print modified_war_dir+" is busy. Might be open in explorer.  Close and retry"
            return False
    try:
        os.mkdir(modified_war_dir)
        with zipfile.ZipFile(ospath(src+"/lib/source.war"), "r") as z:
            z.extractall(modified_war_dir)
        return True
    except:
        return False

def modify_war(tdir, ppath):
    print myself()
    def zip_files(path, dst):
        zipf = zipfile.ZipFile(dst, 'w')
        for root, dirs, files in os.walk(path):
            for f in files:
                fpath = os.path.join(root, f)
                zpath = fpath.split(path)[1]
                zipf.write(fpath, zpath)
        zipf.close()

    modified_war_dir = ospath(tdir + "/modified_war")
    webxml = ospath(modified_war_dir+'/WEB-INF/web.xml')
    data_root = ospath(tdir+"/data")
    src_root = ospath(ppath)
    config_file = ospath(tdir+"/etc/configuration.xml")

    f = open(webxml, "rb")
    html_doc = f.read()
    f.close()

    soup = BeautifulSoup(html_doc, "xml")
    try:
        for cp_tag in soup.find_all('context-param'):
            pn_tag = cp_tag.find('param-name')
            if pn_tag and pn_tag.string == "CONFIGURATION":
                pv_tag = cp_tag.find('param-value')
                if pv_tag:
                    pv_tag.string.replace_with(config_file)
                    break
        if cp_tag:
            new_cp_tag = soup.new_tag("context-param")
            new_pn_tag = soup.new_tag("param-name")
            new_pn_tag.string = "SCAN_REPOS"
            new_pv_tag = soup.new_tag("param-value")
            new_pv_tag.string = "false"
            new_d_tag = soup.new_tag("description")
            new_d_tag.string = "Set to true if using external repos"
            new_cp_tag.append(new_pn_tag)
            new_cp_tag.append(new_pv_tag)
            new_cp_tag.append(new_d_tag)
            cp_tag.insert_after(new_cp_tag)
            new_cp_tag = soup.new_tag("context-param")
            new_pn_tag = soup.new_tag("param-name")
            new_pn_tag.string = "SRC_ROOT"
            new_pv_tag = soup.new_tag("param-value")
            new_pv_tag.string = src_root
            new_d_tag = soup.new_tag("description")
            new_d_tag.string = "Full path of src"
            new_cp_tag.append(new_pn_tag)
            new_cp_tag.append(new_pv_tag)
            new_cp_tag.append(new_d_tag)
            cp_tag.insert_after(new_cp_tag)
            new_cp_tag = soup.new_tag("context-param")
            new_pn_tag = soup.new_tag("param-name")
            new_pn_tag.string = "DATA_ROOT"
            new_pv_tag = soup.new_tag("param-value")
            new_pv_tag.string = data_root
            new_d_tag = soup.new_tag("description")
            new_d_tag.string = "Full path of data"
            new_cp_tag.append(new_pn_tag)
            new_cp_tag.append(new_pv_tag)
            new_cp_tag.append(new_d_tag)
            cp_tag.insert_after(new_cp_tag)
    except:
        return False
    xml = soup.prettify()
    with open(webxml, "wb") as f:
        f.write(xml)
    zip_files(modified_war_dir, ospath(tdir+"/"+os.path.basename(ppath)+".war"))
    return True

def copy_war(tdir, tomdir, ppath):
    print myself()
    modified_war = ospath(tdir +"/"+os.path.basename(ppath)+".war")
    destfile = ospath(tomdir + "/webapps/")
    print modified_war
    print destfile
    try:
        shutil.copy(modified_war, destfile)
        return True
    except:
        return False

def start_stop_server(envs, action):
    print myself()
    def check_port_in_use(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(('localhost', int(port)))
            s.shutdown(2)
            return True
        except:
            return False
    inuse = check_port_in_use(8080)
    jredir = get_tool_dir('jre', envs)
    tomdir = get_tool_dir('tomcat', envs)
    if not os.path.isdir(jredir) or not os.path.isdir(tomdir):
        print "jre or tomcat directory missing.  you might not have setup index for any project yet."
        print "Run this tool again with --action=setup"
        return
    if action == 'start':
        if inuse == True:
            print "A server is already listening on port 8080, You may have to stop that and retry"
            tomcat_server('stop', jredir, tomdir)
        tomcat_server('start', jredir, tomdir)
        print "Server Started"
        print "\n\nFollowing Projects are available:"
        for file in os.listdir(ospath(tomdir+"/webapps")):
            if file.endswith(".war"):
                fname, fext = os.path.splitext(file)
                print "http://localhost:8080/"+fname
        print "\n"
    elif action == 'stop':
        if inuse == True:
            tomcat_server('stop', jredir, tomdir)
            print "Server Stopped"

def index_for_project(envs, command):
    if (command == "setup"):
        print "Setting up index..."
        if validate_path(envs) == False:
            print "Not a valid source path"
            return False
        if check_and_copy_tools(envs) == True:
            return index_a_project(envs)
    elif (command == "reindex"):
        print "Reindexing...."
        if validate_path(envs) == True:
            print "Empty folder found - run setup before reindex"
            return False
        if check_and_copy_tools(envs) == True:
            return index_a_project(envs)
    else:
        print "Invalid command!"
        return False

def index_a_project(envs):
    print myself()
    ppath = ospath(envs['ppath'])
    ogdir = ospath(get_tool_dir('opengrok', envs))
    tomdir = ospath(get_tool_dir('tomcat', envs))
    tempdir = get_temp_dir(envs)
    if extract_war(ogdir, tempdir) == False:
        print "Extracting source.war failed"
        return False

    if modify_war(tempdir, ppath) == False:
        print "Could not create source.war"
        return False

    if copy_war(tempdir, tomdir, ppath) == False:
        print "Copying source.war failed"
        return False

    start_stop_server(envs, 'stop')
    start_stop_server(envs, 'start')
    if index_og(envs) == True:
        start_stop_server(envs, 'stop')
        start_stop_server(envs, 'start')
        return True
    else:
        return False

def validate_path(envs):
    print myself()
    ppath = envs['ppath']
    abspath = ospath(os.path.expanduser(ppath))
    if  os.path.isdir(abspath):
        tdir = get_temp_dir(envs)
        if os.path.isdir(tdir):
            print "Project dir exists"
            return False
        else:
            os.makedirs(tdir)
        return True
    return False

def check_and_copy_tools(envs):
    print myself()
    if tools_present(envs) == True:
        if extract_and_copy(envs) == True:
            return True
    return False

def tools_present(envs):
    print myself()
    tpath = ospath(envs['cpath']+"/tools")
    tomcat_file = ospath(tpath+"/"+get_tool_property('tomcat','file_name'))
    opengrok_file = ospath(tpath+"/"+get_tool_property('opengrok','file_name'))
    jre_file = ospath(tpath+"/"+get_tool_property('jre','file_name'))
    ctags_file = ospath(tpath+"/"+get_tool_property('ctags','file_name'))
    if os.path.isfile(tomcat_file) and os.path.getsize(tomcat_file) == get_tool_property('tomcat', 'file_size') and \
       os.path.isfile(opengrok_file) and os.path.getsize(opengrok_file) == get_tool_property('opengrok', 'file_size') and \
       os.path.isfile(jre_file) and os.path.getsize(jre_file) == get_tool_property('jre', 'file_size') and \
       os.path.isfile(ctags_file) and os.path.getsize(ctags_file) == get_tool_property('ctags', 'file_size'):
        return True
    else:
        return False

def extract_and_copy(envs):
    print myself()
    for tool in tools_dict.keys():
        fname, fext = os.path.splitext(tools_dict[tool]['file_name'])
        if fext == ".gz" or fext == ".tar":
            untar_tool(tool, envs)
        elif fext == ".zip":
            unzip_tool(tool, envs)
    return True

def get_tool_property(name, prop):
    return tools_dict[name][prop]

def get_tool_dir(tool, envs):
    print myself()
    extract_dir = ospath(get_temp_dir(envs)+"/"+get_tool_property(tool,'extract_dir'))
    if envs['tpath'] != '':
        extract_dir = ospath(envs['tpath']+"/"+get_tool_property(tool,'extract_dir'))
    else:
        extract_dir = ospath(envs['cpath']+"/"+get_tool_property(tool,'extract_dir'))
    return extract_dir

def get_temp_dir(envs):
    if envs['tpath'] != '':
        tdir = ospath(envs['tpath']+"/projects/"+os.path.basename(envs['ppath']))
    else:
        tdir = ospath(envs['cpath']+"/projects/"+os.path.basename(envs['ppath']))
    return tdir

def unzip_tool(tool, envs):
    cdir = envs['cpath']
    tool_name = convert_to_os_path(cdir+"/tools/"+get_tool_property(tool,'file_name'))
    extract_dir = convert_to_os_path(get_tool_dir(tool, envs))
    if os.path.isdir(extract_dir):
        #os.system('rmdir /S /Q \"{}\"'.format(extract_dir))
        return
    extract_dir = os.path.dirname(extract_dir)
    if not os.path.isdir(extract_dir):
        os.makedirs(extract_dir)
    with zipfile.ZipFile(tool_name, "r") as z:
        z.extractall(extract_dir)

def untar_tool(tool, envs):
    cdir = envs['cpath']
    tool_name = convert_to_os_path(cdir+"/tools/"+get_tool_property(tool,'file_name'))
    extract_dir = convert_to_os_path(get_tool_dir(tool, envs))
    if os.path.isdir(extract_dir):
        #os.system('rmdir /S /Q \"{}\"'.format(extract_dir))
        return
    extract_dir = os.path.dirname(extract_dir)
    if tarfile.is_tarfile(tool_name):
        fhand = tarfile.open(tool_name)
        fhand.extractall(extract_dir)

def index_og(envs):
    print myself()
    etc = convert_to_os_path(get_temp_dir(envs)+"/etc")
    if not os.path.isdir(etc):
        os.mkdir(etc)
    java = convert_to_os_path(get_tool_dir('jre', envs)+"/bin/"+get_tool_property('jre','bin_file'))
    opengrok =   convert_to_os_path(get_tool_dir('opengrok', envs)+"/lib/"+get_tool_property('opengrok','bin_file'))
    config = convert_to_os_path(etc+"/configuration.xml")
    ctags = convert_to_os_path(get_tool_dir('ctags', envs)+"/"+get_tool_property('ctags','bin_file'))
    src = convert_to_os_path(envs['ppath'])
    data = convert_to_os_path(get_temp_dir(envs)+"/data")
    webapp = os.path.basename(envs['ppath'])
    cmd = java+" -jar "+opengrok+" -W "+config+" -c "+ctags+" -P -S -s "+src+" -d "+data+" -w "+webapp
    try:
        os.system(cmd)
        return True
    except:
        return False

def tomcat_server(action, jredir, tomdir):
    if action not in ['start', 'stop']:
        return
    if action == 'start':
        os.putenv('JRE_HOME',jredir)
        os.putenv('CATALINA_HOME',tomdir)
        cmd =  ospath(tomdir+'/bin/startup'+get_tool_property('tomcat', 'bin_file'))
        os.system(cmd)
    elif action == 'stop':
        os.putenv('JRE_HOME',jredir)
        os.putenv('CATALINA_HOME',tomdir)
        cmd =  ospath(tomdir+'/bin/shutdown'+get_tool_property('tomcat', 'bin_file'))
        os.system(cmd)
    time.sleep(5)
