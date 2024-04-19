# -------------------------------------------------------------------------------
# Name:        showpy
# Purpose:     list the version of python executable in the from the specified root directory 
#
# Author:      Grégoire Catineau
#
# Created:     19/04/2021
# -------------------------------------------------------------------------------
# keep to implemente:
#  TODO
#  Done - make an object from this tool : example a 'showpy' object , showpy.search("c:\",getversion=True)
#  - choose options to process and display: version , size hash path, sum of files size,
#  - return a list : version, size, hash , path etc...
#  Done - passing directory argument : showpy c:\
#  - create a sub function for print informations  print("version: ", ..... get info(result)...
#  - get the better and fastest hash function :  source : https://stackoverflow.com/questions/61229719/hashing-file-within-drf-post-http-request
#  - show statistic ex: sum of files size, same hash, sort version, etc...
#

import subprocess
import os
import hashlib
import sys
import re



class PyExe:
    
    separator = " ; "
    
    #TODO implement regex with for "python*.exe" or "py*.Exe"

    pythonExecutables = ["python.exe", "python3.exe", "py.exe", "python27.exe", "py3.exe", "py2.exe", "pypy3.exe",
                         "pypy.exe"]
    pythonBasedExecutables = ["py2.exe", "pypy3.exe", "cpython.exe", "ipython.exe"]
    
    pythonExecutablesRegex = ['python3.9.exe']
    
    #TODO implement these options
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
            return None
    def calculate_md5(self,file_path):
        # Ouvrir le fichier en mode lecture binaire
        try:
            with open(file_path, "rb") as f:
                # Créer un objet hash MD5
                md5_hash = hashlib.md5()
                
                # Lire le fichier par blocs pour éviter la surcharge de la mémoire
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)
        
            # Retourner la somme de contrôle MD5 sous forme de chaîne hexadécimale    
        except:
            return ""
        return md5_hash.hexdigest()

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
            return None

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
        # print header
        line = f"{'version':<8}{self.separator}{'bytes':>10}{self.separator}{'MD5 Sum'.ljust(32)}{self.separator}path"
        print(line)
        for root, subFolder, files in os.walk(self.defaultrootpath):
            try:
                if str(files).index('.exe'):
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
                                line = f"{(version) or '[None]':<8}{self.separator}{"{:,}".format(self.current_file_size):>10}{self.separator}{self.calculate_md5(self.current_fileNamePath).ljust(32)}{self.separator}{self.current_fileNamePath}"
                                print(line)

                                nbpythonexe += 1
            except:
                pass # pas d'.exe dans la liste

        print("{}".format(nbpythonexe)+" version of Python was found")


def main():
    pyexe = PyExe()
    #sys.argv="c:\\"
    if len(sys.argv) > 1:
        
        defaultrootpath = sys.argv[1]
        
        if "-notitle" in sys.argv:

            print("ok")
        # TODO handle tile fields line showing optionnal
        print(f"showpy start process for [{defaultrootpath}]")
        pyexe.search(defaultrootpath)
    else:
        print("[showpy] [path]:")


if __name__ == "__main__":
    main()
