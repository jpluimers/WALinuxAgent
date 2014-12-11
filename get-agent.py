#!/usr/bin/env python
#
# Copyright 2014 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Implements parts of RFC 2131, 1541, 1497 and
# http://msdn.microsoft.com/en-us/library/cc227282%28PROT.10%29.aspx
# http://msdn.microsoft.com/en-us/library/cc227259%28PROT.13%29.aspx
#

import sys
import os
import shutil
import imp
import subprocess
import time
import re
import platform

def upgrade():
    account = 'Azure'
    agentUri = ('https://raw.githubusercontent.com/{0}/'
                'WALinuxAgent/2.0/waagent').format(account)
    if os.path.isfile('waagent'):
        os.remove('waagent')
    print "Download WAAgent from: {0}".format(agentUri)
    try:
        import urllib2
        response = urllib2.urlopen(agentUri)
        html = response.read()
        with open("waagent", "w+") as F:
            F.write(html)
    except:
        subprocess.call(['wget', agentUri])

    print "Upgrade WAAgent"
    shutil.copyfile("waagent", "/usr/sbin/waagent")
    os.chmod("/usr/sbin/waagent", 0700)

    distro = platform.linux_distribution()
    cmd = ['service', 'waagent', 'restart']
    if "Ubuntu" in distro[0]:
        cmd[1]='walinuxagent'
    job = subprocess.Popen(cmd)
    job.wait()
    
if __name__ == '__main__':
    upgrade()