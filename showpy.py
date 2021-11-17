#-------------------------------------------------------------------------------
# Name:        showpy
# Purpose:
#
# Author:      catineau
#
# Created:     03/11/2021
# Copyright:   (c) catineau 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# keep to implemente:
#
#  - make an object from this tool : example a 'showpy' object , showpy.search("c:\",getversion=True)
#  - chosse information de get from file : version , size hash path, sum of files size,
#  - return a tuple version, size, hash , path etc...
#  - passing argument : showpy c:\
#  - convert path to Windows of linux  with detection of them example : 'posix', 'nt', 'java'
#  - create a sub function for print informations  print("version: ", ..... get info(result)...
#  - get the better and fastest hash function :  source : https://stackoverflow.com/questions/61229719/hashing-file-within-drf-post-http-request
# -  possibility have separator :  version:  Python 3.9.1;size= 923192 ; hash= d1542dbd731960ec3636047de092f09d7fba4da5252acca4dd9be1d6a4600caf;  path:  c:\Windows\py.exe
# - show statistic ex: sum of files size, same hash, sort version, etc...
#

import subprocess
import os
import hashlib
import sys


class PyDir:

    pythonExecutables=["python.exe","python3.exe","py.exe","python27.exe","py3.exe","py2.exe","pypy3.exe","pypy.exe"]
    pythonBasedExecutables = ["py2.exe", "pypy3.exe","cpython.exe"]

    appOptions={"version":"-version","hash":"-hash"}

    def __init__(self):
        pass

    def sha256sum(self,filename):
        h  = hashlib.sha256()
        b  = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def get_root_path(self):
        return os.path.abspath(os.sep)

    def get_platform(self):
        return  sys.platform

    def process(self,defaultrootpath):

        self.defaultrootpath=defaultrootpath

        if defaultrootpath=="":
            self.defaultrootpath = self.get_root_path()

        platform = self.get_platform()  # linux or win32

        nbrversion=0
        nbpythonexe=0

        for root, subFolder, files in os.walk(self.defaultrootpath):
            for item in files:
                if item in (self.pythonExecutables or self.pythonBasedExecutables):
                    # display hash of file . https://nitratine.net/blog/post/how-to-hash-files-in-python/
                    fileNamePath = str(os.path.join(root,item))
                    file_size = os.path.getsize(fileNamePath)
                    if file_size==0:
                        print("size error for file:",(fileNamePath)," size=",file_size)
                        continue
                    try:
                        result=subprocess.run([fileNamePath,"--version"],capture_output=True)

                    except:
                        print("version : probleme",fileNamePath )

                    else:

                        if result.stdout.decode("utf-8")!="":
                            print("version: ",result.stdout.decode("utf-8").strip("\r\n").ljust(19)," size:",str(file_size).ljust(16)," hash:",self.sha256sum(fileNamePath).ljust(70)," path: ",fileNamePath)

                        else:
                            print("version: ",result.stderr.decode("utf-8").strip("\r\n").ljust(19)," size:",str(file_size).ljust(16)," hash:",self.sha256sum(fileNamePath).ljust(70)," path: ",fileNamePath)
                    finally:
                        nbpythonexe += 1


        print("total python executable version found :{}".format(nbpythonexe))

def main():

    pyDir=PyDir()

    if len(sys.argv) > 1:
        defaultrootpath = str(sys.argv[1])
        pyDir.process(defaultrootpath)
    else:
        print("[showpy]:")
        print("Available subcommands:")




if __name__ == '__main__':

    main()
