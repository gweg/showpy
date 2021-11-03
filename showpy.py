#-------------------------------------------------------------------------------
# Name:        module1
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
#  - chosse information de get from file : version , size hash path, 
#  - return a tuple version, size, hash , path etc...
#  - passing argument : showpy c:\
#  - convert path to Windows of linux  with detection of them
#  - create a sub function for print informations  print("version: ", ..... get info(result)...
#
#

import subprocess
import os
import hashlib

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def main():
    nbrversion=0
    for root, subFolder, files in os.walk("c:\\"):
        for item in files:
            if item in ("python.exe","python3.exe","py.exe","python27.exe","py3.exe","py2.exe") :
                # display hash of file . https://nitratine.net/blog/post/how-to-hash-files-in-python/
                fileNamePath = str(os.path.join(root,item))
                file_size = os.path.getsize(fileNamePath)
                if file_size==0:
                    print("size error for:",(fileNamePath)," size=",file_size)
                    continue
                try:
                    result=subprocess.run([fileNamePath,"--version"],capture_output=True)
                    if result.stdout.decode("utf-8")!="":
                        print("version: ",result.stdout.decode("utf-8").strip("\r\n").ljust(16)," size=",str(file_size).ljust(16)," hash=",sha256sum(fileNamePath).ljust(70)," path: ",fileNamePath)

                    else:
                        print("version: ",result.stderr.decode("utf-8").strip("\r\n").ljust(16)," size=",str(file_size).ljust(16)," hash=",sha256sum(fileNamePath).ljust(70)," path: ",fileNamePath)
                        
                except:
                    print("version : probleme",fileNamePath )

    print("total python executable version found :{}".format(nbrversion))

if __name__ == '__main__':

    main()
    
