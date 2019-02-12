import spur
import sys
import os
config = {"Linux":{"apt":['apt','list','--installed'],
                    "osversion":['uname','-mrs']},
          "redhat":{"apt":["yum","list","installed"]},
          "suse":{"apt":["rpm","-qa","--last"]},
          "aix":{"apt":["lslpp","-l"]},
          "solaris":{"apt":["pkginfo","-l"]}}


class SecCheck():

    def __init__(self,server,user,passw):
         self.ssh = spur.SshShell(server,username=user,password=passw,missing_host_key=spur.ssh.MissingHostKey.accept)
         self.ostype = {"os":"",
                        "os_name":"",
                        "os_fullname":"",
                        "os_version":"",
                        "linux_version":"",
                        "hardware":"",
                        "kernel_version":""}
         self.packages = []               
  
    def _RedHatPackageList(self):
        result = self.ssh.run(["yum","list","installed"])
        mylen = result.output.split("\n")
        for i in range(len(mylen)):
          if i <= 5:
             pass
          else:
             p = []
             t = {}
             c = mylen[i].split(" ")
             for b in c:
                  if b == '':
                     pass
                  else:
                    p.append(b)
             for h in range(len(p)): 
                 t['name'] = p[0].split(".")[0]
                 t['version'] = p[1]
                 self.packages.append(t) 

    def _UbuntuPackageList(self):
        result = self.ssh.run(['apt','list','--installed'])
        mylen = result.output.split("\n")
        for i in range(len(mylen)):
            if i == 0:
                pass
            elif i == len(mylen) - 1:
                pass
            else:    
               t = {}
               c = mylen[i].split(",")
               t['name'] = c[0].split("/")[0]
               for b in c:
                   if "now" in b:
                      t['version'] = b.split(" ")[1]
               self.packages.append(t)

    def _doLinux(self):
        r = self.ssh.run(['uname','-mrs'])
        d = r.output.strip("\n").split(" ")
        self.ostype['os'] = d[0]
        self.ostype['hardware'] = d[2]
        self.ostype['kernel_version'] = d[1]
        f = self.ssh.run(['cat','/etc/os-release'])
        c = f.output
        
        if "ubuntu" in c:
            self.ostype['linux_version'] = "Ubuntu"
            self.ostype['os_name'] = "Ubuntu Linux"
            self.ostype['ipaddress'] = self.ssh.run(['hostname','-I']).output.strip('\n').strip(" ")
            self.ostype['hostname'] = self.ssh.run(['hostname']).output.strip('\n')
            for i in c.split('\n'):
                if "PRETTY_NAME" in i:
                    self.ostype['os_fullname'] = i.split("=")[1].strip("\"")
                if "VERSION_ID" in i:
                    self.ostype['os_version'] = i.split("=")[1].strip("\"")
                self._UbuntuPackageList()
        
        if "debian" in c:
            self.ostype['linux_version'] = "Debian"
            self.ostype['os_name'] = "Debian Linux"
            self.ostype['ipaddress'] = self.ssh.run(['hostname','-I']).output.strip('\n').strip(" ")
            self.ostype['hostname'] = self.ssh.run(['hostname']).output.strip('\n')
            for i in c.split('\n'):
                if "PRETTY_NAME" in i:
                    self.ostype['os_fullname'] = i.split("=")[1].strip("\"")
                if "VERSION_ID" in i:
                    self.ostype['os_version'] = i.split("=")[1].strip("\"")
                self._UbuntuPackageList()

        if "centos" in c:
            self.ostype['linux_version'] = "CentOS"
            self.ostype['os_name'] = "CentOS Linux"
            self.ostype['ipaddress'] = self.ssh.run(['hostname','-I']).output.strip('\n').strip(" ")
            self.ostype['hostname'] = self.ssh.run(['hostname']).output.strip('\n')
            for i in c.split('\n'):
                if "PRETTY_NAME" in i:
                    self.ostype['os_fullname'] = i.split("=")[1].strip("\"")
                if "VERSION_ID" in i:
                    self.ostype['os_version'] = i.split("=")[1].strip("\"")
                self._RedHatPackageList()

        if "arch" in c:
            self.ostype['linux_version'] = "Arch Linux"
            self.ostype['os_fullname'] = "Arch Linux"
            self.ostype['os_version'] = "Rolling Release"
        
        if "manjaro" in c:
            self.ostype['linux_version'] = "Manjaro Linux"
            self.ostype['os_fullname'] = "Manjaro Linux"
            self.ostype['os_version'] = "Rolling Release"
        
        if "coreos" in c:
            self.ostype['linux_version'] = "CoreOS"
            self.ostype['CoreOS Linux']
            for i in c.split('\n'):
                if "PRETTY_NAME" in i:
                    self.ostype['os_fullname'] = i.split("=")[1].strip("\"") 
                if "VERSION_ID" in i:
                    self.ostype['os_version'] = i.split("=")[1].strip("\"")    

    def osDetection(self):
        r = self.ssh.run(["uname"])
        if "Linux" in r.output:
           self._doLinux()
           self._UbuntuPackageList()

if __name__ == '__main__':
    servers = ["someipofservers"]
    for i in servers:
         t = SecCheck(i,'username','password')
         t.osDetection()
         print (t.ostype)
         print t.packages



