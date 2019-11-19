import subprocess, stat, os, shutil
from app.config.config import *
from app.lib import fman
from app.lib.ssh.models.ssh import SSH
import random

class App:

    def __init__(self):
        self.GetHosts()
        self.GetConnections()
        # # Generate folders
        self.Generate()
        self.ShareFolder()
        masterfile, slavefile = self.CreateCluster()
        self.SendFiles([
            {
                "source" : masterfile, 
                "destinate": "."   
            },
            {
                "source" : slavefile,
                "destinate" : "."
            }
        ])
        self.RunService()
        self.RunMaster()
        self.AddSlaves()

    def GetHosts(self):
        self.hosts = list(config["hosts"].keys())

    def GetConnections(self):
        self.connectors = dict()
        for host in self.hosts:
            auth = config["hosts"][host]["auth"]
            self.connectors[host] = SSH(host, auth["username"], auth["password"])
            workingdir = config["hosts"][host]["working-dir"]
            self.connectors[host].setWorkingDirectory(workingdir)
        for host in self.hosts:
            self.connectors[host].checkAuthentication()

    def Generate(self):
        # Create run, fire and all folder port for nodes
        cluster_auth = config["cluster-auth"]["password"]
        config_name = config["conf-name"]
        for host in self.hosts:
            # Create host's folder
            currentDir = os.path.join(CLUPATH, host)
            fman.create_path(currentDir)
            ports = [
                config["hosts"][host]["master"]["port"], 
                config["hosts"][host]["slave"]["port"]
            ]
            for port in ports:
                fman.create_path(os.path.join(currentDir, port))
                filepath = os.path.join(currentDir, port, config_name)
                fman.search_replace(
                    TEMPATH, 
                    {
                        "__port__" : port,
                        "__pass__" : cluster_auth
                    }, 
                    filepath
                )
            
            filepath = os.path.join(currentDir, RUNNAME)
            fman.search_replace(
                RUNPATH, 
                {
                    "__port1__" : ports[0],
                    "__port2__" : ports[1],
                    "__name__" : config["conf-name"]
                }, 
                filepath
            )
            os.chmod(filepath, 0o777)
            filepath = os.path.join(currentDir, FIRNAME)
            fman.search_replace(
                FIRPATH, 
                {
                    "__port1__" : ports[0],
                    "__port2__" : ports[1],
                }, 
                filepath
            )
            os.chmod(filepath, 0o777)

    def CreateCluster(self):
        # Create master and add slave files
        files = []
        # Run master
        replace = dict()
        for i, host in enumerate(self.hosts):
            replace["__master%d__" % (i + 1)] = host
            replace["__port%d__" % (i + 1)] = config["hosts"][host]["master"]["port"]
        replace["__pass__"] = config["cluster-auth"]["password"]
        filepath = os.path.join(SHAPATH, "cluster", "master.sh")
        fman.search_replace(
            os.path.join(SHEPATH, "master.sh"), 
            replace, 
            filepath
        )
        os.chmod(filepath, 0o777)
        files.append(filepath)
        # Add slaves
        replace = dict({
            "__pass__" : config["cluster-auth"]["password"]
        })
        for i, host in enumerate(self.hosts):
            mport = config["hosts"][host]["master"]["port"]
            hslave = config["hosts"][host]["slave"]["host"]
            pslave = config["hosts"][host]["slave"]["port"]
            replace["__master%d__" % (i + 1)] = host
            replace["__mport%d__" % (i + 1)] = mport
            replace["__slave%d__" % (i + 1)] = hslave
            replace["__sport%d__" % (i + 1)] = pslave

        filepath = os.path.join(SHAPATH, "cluster", "add_slaves.sh")
        fman.search_replace(
            os.path.join(SHEPATH, "add_slaves.sh"), 
            replace, 
            filepath
        )
        os.chmod(filepath, 0o777)
        files.append(filepath)
        return files

    def sendCommands(self):
        for host in self.hosts:
            self.sendCmd(host, 'ls -la')

    def ShareFolder(self):
        for host in self.hosts:
            # Create host's folder
            os.rename(os.path.join(CLUPATH, host), os.path.join(CLUPATH, DEFNAME))
            self.connectors[host].sendFile(os.path.join(CLUPATH, DEFNAME), '.')
            # self.sendFile(host, os.path.join(CLUPATH, DEFNAME), '.')
            shutil.rmtree(os.path.join(CLUPATH, DEFNAME))
            # os.rename(os.path.join(CLUPATH, DEFNAME), os.path.join(CLUPATH, host))

    def SendFiles(self, list_of_files):
        hostIndex = random.randint(0, len(self.hosts) - 1)
        host = self.hosts[hostIndex]
        for item in list_of_files:
            src, des = item["source"], item["destinate"]
            self.connectors[host].sendFile(src, des)
        self.hostControl = self.connectors[host]

    def RunService(self):
        for host in self.hosts:
            self.connectors[host].sendCommand("cd %s && ./run.sh && sleep 10" % DEFNAME, wait=False)

    def RunMaster(self):
        self.hostControl.sendCommand("./master.sh && sleep 10", wait=False)

    def AddSlaves(self):
        self.hostControl.sendCommand("./add_slaves.sh && sleep 10", wait=False)

    # def sendFile(self, host, source, destination):
    #     shellfile = os.path.join(SHEPATH, 'send_files.sh')
    #     username = config["hosts"][host]["auth"]["username"]
    #     password = config["hosts"][host]["auth"]["password"]
    #     working_dir = config["hosts"][host]["working-dir"]
    #     subprocess.call([shellfile, host, username, password, source, os.path.join(working_dir, destination)])
    # def sendCmd(self, host, cmd):
    #     shellfile = os.path.join(SHEPATH, 'run.sh')
    #     username = config["hosts"][host]["auth"]["username"]
    #     password = config["hosts"][host]["auth"]["password"]
    #     working_dir = config["hosts"][host]["working-dir"]
    #     subprocess.call([shellfile, host, username, password, cmd])