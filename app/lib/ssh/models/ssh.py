import os
import subprocess
from app.lib.ssh.config.config import *
from app.lib import fman

class SSH:
    """Required: SSHPASS"""
    SENDFILE = os.path.join(SHEPATH, "send_files.sh")
    SENDCMD = os.path.join(SHEPATH, "send_cmd.sh")
    SENDCMD_TMP = os.path.join(SHEPATH, "send_cmds.tmp.sh")
    SENDCMD_RUN = os.path.join(SHEPATH, "send_cmds.sh")

    def __init__(self, host, name, passwd):
        self.host = host
        self.name = name
        self.passwd = passwd
        self.workingdir = '/'
    
    def checkAuthentication(self):
        self.sendCommand("ls -la")

    def setWorkingDirectory(self, directory):
        # Create that folder if it does not exist!
        self.sendCommand(
            "mkdir %s" % self.workingdir,
            wait=False
        )
        self.workingdir = directory

    def sendFile(self, source, destinate):
        destinate = os.path.join(self.workingdir, destinate)
        subprocess.call([self.SENDFILE, self.host, self.name, self.passwd, source, destinate])

    def sendCommand(self, cmd, wait=True):
        cmd = "cd %s && %s" % (self.workingdir, cmd)
        if wait:
            subprocess.call([self.SENDCMD, self.host, self.name, self.passwd, cmd])
        else:
            subprocess.Popen([self.SENDCMD, self.host, self.name, self.passwd, cmd])

    def sendCommands(self, commands):
        commands = ["cd %s" % self.workingdir] + commands
        commands = "\n".join(commands)
        fman.search_replace(self.SENDCMD_TMP, {
            "__commands__" : commands
        }, self.SENDCMD_RUN)
        subprocess.call([self.SENDCMD_RUN, self.host, self.name, self.passwd])
        