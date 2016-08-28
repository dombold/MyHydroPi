#!/usr/bin/env python

import subprocess


def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

restart()

