import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()
    
lib.editengine.bar_extract(os.path.join(os.getcwd(),"al00.ard"), os.path.join(os.getcwd(), "al00"))

evt_path = os.path.join(os.getcwd(), "al00", "evt.script")
lib.editengine.spawnscript_extract(evt_path, evt_path+".txt")