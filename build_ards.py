import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

EXTRACT_ARDS=False

only_build = ["hb05.ard"]

arddir = os.path.join(os.getcwd(), "extracted_ards")

spawndir = os.path.join(os.getcwd(), "spawnscripts")

arddir_src = os.path.join(os.environ["USE_KH2_GITPATH"], "KH2", "ard")

for ard in os.listdir(arddir_src):
    if len(only_build) > 0 and ard not in only_build:
        continue
    fn = os.path.join(arddir_src, ard)

    out_pth = os.path.join(arddir, ard)

    evtname = "evt.script"#None
    for f in [i for i in os.listdir(out_pth) if not i.endswith(".txt") and not i.endswith(".new")]:
        if f.startswith("evt."):
            evtname = f

    if evtname == None:
        print("ARD {} has no evt".format(ard))
    else:
        evt_pth = os.path.join(out_pth, evtname)

        print("compiling script {} - {}".format(evt_pth+".txt", evt_pth))

        lib.editengine.spawnscript_compile(evt_pth+".txt.new", evt_pth)
        lib.editengine.bar_build(os.path.join(out_pth, ard+".json"), fn)