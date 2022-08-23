#from asyncio import write
from posixpath import split
from statistics import variance
import sys
import os
from os import walk
import hashlib
import progressbar 
import time

v = "0.3"
author = "Samuel Sachs"
pname = "MD5-Dateilistengenerator"
module_name = __file__.split("\\")[-1][:-3]

build = "bin"
if build == "bin":
    execute_line = f"{module_name}.exe"
if build == "python":
    execute_line = f"python {module_name}.py"

def help():
        sys.exit(f'''{pname} v{v}
Copyright (c) {author}. Alle Rechte vorbehalten.

Das “{pname}”-Befehlszeilenprogramm ermöglicht das Erstellen einer Datei mit einer Auflistung aller Dateien in einem angegebenen Verzeichnis mitsamt MD5-Hashwerten mithilfe der Befehlszeile. Die Ausgabedatei wird im aktuellen Programmverzeichnis erstellt.

Nutzung: {execute_line} [<Ordnerpfad>] ODER [<Option>]

Beispiele:  {execute_line} "C:\Windows"
            {execute_line} --version 

Die folgenden Optionen stehen zur Verfügung:
    -v, --version    Version des Tools anzeigen
    -h, --help       Diese Hilfe anzeigen
          ''')
        
def vers():
    sys.exit(f"{pname} v{v}")

def error():
    sys.exit("[FEHLER] Es wurde kein gültiger Ordnerpfad angegeben.\nFür mehr Infos -h oder --help")
  
def generate_file_list(path: str) -> list:
    fl = []
    
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            #print(os.path.join(root, name))
            fl.append(os.path.join(root, name))

    return fl

def count_files_and_folders(path: str) -> dict:
    sum_files = 0
    sum_folders = 0
    
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            sum_files += 1

        for name in dirs:
            sum_folders += 1

    return {"folders": sum_folders, "files": sum_files}

def md5(fname: str) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == "__main__":
    try:    
        path = sys.argv[1]
    except IndexError as e:
        help()

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        help()
        
    if sys.argv[1] == "-v" or sys.argv[1] == "--version":
        vers()

    if path == " " or None or not os.path.isdir(path):
        error()
        
        
    file_list = generate_file_list(path)
    md5_file = "md5_list.txt"
    count = count_files_and_folders(path)

    widgets = [' [', 
            progressbar.Timer(format= 'vergangene Zeit: %(elapsed)s'), 
            '] ', 
            progressbar.Bar('█'),
            ' ',
            progressbar.RotatingMarker(),
            ' (', 
            progressbar.Percentage(format='%(percentage)3d%% ', na='N/A%%'),
            progressbar.ETA(), ') ', 
            ] 
    
    bar = progressbar.ProgressBar(max_value=int(len(file_list)),  
                                widgets=widgets).start()

    os.system('cls')
    print(f'Anzahl Ordner: {count["folders"]}\nAnzahl Dateien: {count["files"]}\nMD5-Dateiliste wird erstellt. Bitte warten...')


    with open(md5_file, "w", encoding="UTF-8") as file:
        file.writelines(f'# MD5-Dateiprüfsummenliste für ".{path[2:]}"\n--------------------------------------------------------------------\n')

    with open(md5_file, "a", encoding="UTF-8") as file:
        file.writelines(f'Anzahl Ordner: {count["folders"]} | Anzahl Dateien: {count["files"]}\n--------------------------------------------------------------------\n')

    progress = 0

    for element in file_list:
        
        with open(md5_file, "a", encoding="UTF-8") as file:
            line = f'MD5: "{md5(element)}" | Path: ".{element[2:]}"\n'
            file.writelines(line)
            progress += 1
            bar.update(progress)
        
    with open(md5_file, "a", encoding="UTF-8") as file:
        file.writelines('--------------------------------------------------------------------')
