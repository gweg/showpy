# -------------------------------------------------------------------------------
# Name:        showpy
# Purpose:     list all version of python executable in the specified directory with directory recursivity
#
# Author:      catineau
#
# Created:     03/11/2021
# Copyright:   (c) Grégoire Catineau 2022
# Licence:     CC0
# -------------------------------------------------------------------------------
# keep to implemente:
#  TODO
#  Done - make an object from this tool : example a 'showpy' object , showpy.search("c:\",getversion=True)
#  - choose options to process and display: version , size hash path, sum of files size,
#  - return a tuple version, size, hash , path etc...
#  Done - passing directory argument : showpy c:\
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
import re


class PyExe:
    #TODO implement regex with for "python*.exe" or "py*.Exe"

    pythonExecutables = ["python.exe", "python3.exe", "py.exe", "python27.exe", "py3.exe", "py2.exe", "pypy3.exe",
                         "pypy.exe"]
    pythonBasedExecutables = ["py2.exe", "pypy3.exe", "cpython.exe", "ipython.exe"]
<<<<<<< HEAD
    
    pythonExecutablesRegex = ['python3.9.exe']

=======
    #TODO implement these options
>>>>>>> 5c2ad53666791fd3e590fd9536e7a74731d8a759
    appOptions = {"version": "-version", "hash": "-hash", "size": "-size", "path": "-path"}

    def __init__(self):
        self.current_file_size = 0
        self.current_fileNamePath = ""

    def detect_version(self,chaine,regex):


        if chaine.stderr.decode("utf-8") != "":
            versionInfo = str(chaine.stderr.decode("utf-8").strip("\r\n"))
        else:
            versionInfo = str(chaine.stdout)

        if len(str(chaine)) == 0:
            versionInfo = "[none]"



        regex = r"([1-9][0-9]|[0-9])(\.|)([1-9][0-9]|[0-9]|)(\.|)([1-9][0-9]|[0-9]|)"

        matches = re.search(regex, versionInfo)
        if matches:
            return str(matches.group(1)+"."+matches.group(3)+"."+matches.group(5))
        else:
            return ""

    def sha256sum(self, filename):
        if os.path.getsize(filename) > 0:
            h = hashlib.sha256()
            b = bytearray(128 * 1024)
            mv = memoryview(b)
            with open(filename, 'rb', buffering=0) as f:
                for n in iter(lambda: f.readinto(mv), 0):
                    h.update(mv[:n])
            return h.hexdigest()
        else:
            return "None"

    def get_root_path(self):
        return os.path.abspath(os.sep)

    def get_platform(self):
        return sys.platform

    def search(self, defaultrootpath):



        self.defaultrootpath = defaultrootpath

        if defaultrootpath == "":
            self.defaultrootpath = self.get_root_path()

        platform = self.get_platform()  # linux or win32


        nbpythonexe = 0

        for root, subFolder, files in os.walk(self.defaultrootpath):
            for item in files:
                if item in (self.pythonExecutables or self.pythonBasedExecutables):
                    version=""
                    # display hash of file . https://nitratine.net/blog/post/how-to-hash-files-in-python/
                    self.current_fileNamePath = str(os.path.join(root, item))
                    self.current_file_size = os.path.getsize(self.current_fileNamePath)
                    #print(nbpythonexe," ",self.current_fileNamePath)

                    if r"c:\Users\catineau\AppData\Local\Programs\Python\Python39\Lib\venv\scripts\nt\python.exe" == self.current_fileNamePath:
                        pass

                    if self.current_file_size == 0:
                        pass
                    line=""
                    try:
                        result = subprocess.run([self.current_fileNamePath, "--version"], capture_output=True)

                        version = self.detect_version(result,r"([1-9][0-9]|[0-9])(\.|)([1-9][0-9]|[0-9]|)(\.|)([1-9][0-9]|[0-9]|)")

                    except:
                        version="[None]"

                    finally:
                        #line = f" version: {version : <8} size: {self.current_file_size:>10} h(256): {self.sha256sum(self.current_fileNamePath):>65} path: {self.current_fileNamePath}"
                        line = f" version: {version : <8} size: {self.current_file_size:>10} h(256): ....{self.sha256sum(self.current_fileNamePath)[:10]:>10} path: {self.current_fileNamePath}"
                        print(line)

                        nbpythonexe += 1

        print("sum of python executable version found :{}".format(nbpythonexe))


def main():
<<<<<<< HEAD
    pyDir = PyDir()
    arg= sys.argv    
    #arg = "D:\\dev\\py\\showpy\\showpy\\showpy.py c:\\"
    if len(arg) > 1:

        defaultrootpath = str(arg[1])
        if "-notitle" in arg:
=======
    pyexe = PyExe()
    #sys.argv="c:\\"
    if len(sys.argv) > 1:
        
        defaultrootpath = sys.argv
        if "-notitle" in sys.argv:
>>>>>>> 5c2ad53666791fd3e590fd9536e7a74731d8a759
            print("ok")
        # TODO handle tile fields line showing optionnal
        print(f"showpy start process for [{defaultrootpath}]")
        pyexe.search(defaultrootpath)
    else:
        print("[showpy] [path]:")


if __name__ == "__main__":
    main()
