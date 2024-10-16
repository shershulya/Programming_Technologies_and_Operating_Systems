#!/usr/bin/python3

import libtmux
import os
from tqdm import tqdm
import sys

def start(num_users, base_dir='./'):
    os.system('tmux new-session -d -s ipynb')
    server = libtmux.Server()
    session = server.find_where({'session_name': 'ipynb'})
    print('----------------------------------------------------------------------------')
    print('-------------------Creating tmux session with name: ipynb-------------------')
    print('----------------------------------------------------------------------------')
    init = session.attached_window
    init.rename_window('init')
    port_st = 11050
    port_end = 11055
    port_cur = port_st
    
    for i in tqdm(range(num_users)):
        inx = str(i + 1)
        os.system('mkdir -p ' + inx)
        win = session.new_window(attach=True, window_name=inx)
        pane = win.list_panes()[0]
        notebook_dir = base_dir + inx + '/'
        cmd = 'jupyter notebook'
        if (port_cur > port_end):
            port_cur = 8080
        args = ' --port ' + str(port_cur) + \
                ' --no-browser ' + \
                '--NotebookApp.notebook_dir=' + notebook_dir
        pane.send_keys(cmd + args)
        port_cur += 1
    
    session.kill_window('init')

def stop(session_name, num, base_dir='./'):
    server = libtmux.Server()
    session = server.find_where({'session_name': session_name})
    os.system('rm -rf ' + base_dir + num)
    session.kill_window(num)

def stop_all(session_name, base_dir='./'):
    try:
        server = libtmux.Server()
        session = server.find_where({'session_name': session_name})
        for win in session.list_windows():
            os.system('rm -rf ' + base_dir + win.name)
        session.kill_session()
    except:
        print('Err: No such tmux session :' , session_name)

def print_help():
    print ('Help:\nhw1.py cmd args\n \
    Possible values: \n \
        start     num_ipynb_env                base_dir=\'./\'\n \
        stop      session_name   num_of_window base_dir=\'./\' \n \
        stop_all  session_name                 base_dir=\'./\'')

def main():
    if len(sys.argv) < 2:
        print('Warning: No arguments')
        return 0
    cmd = sys.argv[1]
    if (cmd == '-h' or cmd == '--help'):
        print_help()
        return 0
    if (cmd == 'start'):
        if len(sys.argv) < 3:
            print_help()
            return 0
        num_users = int(sys.argv[2])
        start(num_users)
    elif (cmd == 'stop_all'):
        if len(sys.argv) < 3:
            print_help()
            return 0
        session_name = sys.argv[2]
        stop_all(session_name)
    elif (cmd == 'stop'):
        if len(sys.argv) < 3:
            print_help()
            return 0
        session_name = sys.argv[2]
        num = sys.argv[3]
        stop(session_name, num)
    else:
        print('Err: No such command;\n Print --help for command information')
    
if __name__ == '__main__':
    main()
