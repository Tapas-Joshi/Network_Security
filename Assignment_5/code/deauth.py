import os
import time
import subprocess
from os import system

wlan = "wlx9cefd5ff7501"
raw_out = ""

def tmux(command):
    system('tmux %s' % command)


def tmux_shell(command):
    tmux('send-keys "%s" "C-m"' % command)

def de_auth():
    raw_out = subprocess.check_output("ls /sys/class/net | grep ^w", shell=True)
    str(raw_out)
print([x.strip() for x in raw_out.split("\n")])

de_auth()