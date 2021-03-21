# Extract everything if not extracted

# Check all the flags to make sure I don't set one used by the game
import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

EXTRACT_ARDS=False


arddir = os.path.join(os.getcwd(), "extracted_ards")
if EXTRACT_ARDS:    
    if os.path.exists(arddir):
        shutil.rmtree(arddir)
    os.mkdir(arddir)

spawndir = os.path.join(os.getcwd(), "spawnscripts")
if os.path.exists(spawndir):
    shutil.rmtree(spawndir)
os.mkdir(spawndir)

ardinfo = {}
ignore_worlds = [
    "lm" # little mermaid is all cutscenes lol so it softlocks
]
ignore_ards = [
    "lk08.ard", # Entering jungle for second visit story crashes pcsx2
    "wi03.ard"
]
# These issues might all be related to GOA mod
# Check if the continue issue is due to GOA mod
# I need to know if there are any areas in the game where a mission starts without a cutscene beforehand
ignore_programs = {
    "tt27.ard": ["0x02"], # Talking to yen sid
    "tt28.ard": ["0x02"], # changing to kh2 sora
    "tr01.ard": ["0x33"], # causes entering SP the second time to go to data larxene
    "hb09.ard": ["0x33"], # causes first cutscene in merlin to not fire
    "hb05.ard": ["0x01"], # Causes you to be sent to SP instead of skipped, and makes demyx portal
}

SKIPLINE = "	SetProgressFlag 0xFFF\n"

def shouldIgnore(ard, program, eventtype):
    ignore = False
    if ard[:2] in ignore_worlds:
        ignore = True
    if ard in ignore_ards:
        ignore = True
    # NEEDED To make choosing weapons work
    if int(eventtype) >= 128:
        ignore = True
    if ard in ignore_programs:
        if program.strip() in ignore_programs[ard]:
            ignore = True
    if ignore:
        print("ignoring {}, {}".format(ard, program.strip()))
    return ignore

arddir_src = os.path.join(os.environ["USE_KH2_GITPATH"], "KH2", "ard")

eventtypes = []
for ard in os.listdir(arddir_src):
    fn = os.path.join(arddir_src, ard)

    out_pth = os.path.join(arddir, ard)
    if EXTRACT_ARDS:
        lib.editengine.bar_extract(fn, out_pth)
    
    evtname = None
    for f in [i for i in os.listdir(out_pth) if not i.endswith(".txt") and not i.endswith(".new")]:
        if f.startswith("evt."):
            evtname = f

    ardinfo[ard] = {
        "fn": fn,
        "out_pth": out_pth
    }
    if evtname == None:
        print("ARD {} has no evt".format(ard))
    else:
        evt_pth = os.path.join(out_pth, evtname)
        if EXTRACT_ARDS:
            lib.editengine.spawnscript_extract(evt_pth, evt_pth+".txt")
        
        lines = open(evt_pth+".txt")
        lines_new = []
        currentProgram = ''
        lines_program = []
        changesMade = False
        for line in lines:
            if line.startswith("Program"):
                if len(currentProgram) > 0:
                    if changesMade:
                        spawnscriptsdir = os.path.join(spawndir, ard)
                        if not os.path.exists(spawnscriptsdir):
                            os.mkdir(spawnscriptsdir)
                        programfn = os.path.join(spawnscriptsdir, "program-"+currentProgram.lower().replace(" ", "")[2:].strip())
                        with open(programfn, "w") as f:
                            f.write(''.join(lines_program))
                    lines_program = []
                    changesMade = False
                currentProgram = line.split(" ")[1]
            if len(currentProgram) > 0:
                if "SetEvent" in line:
                    eventtype = line.strip().split(" ")[3]
                    bitevent = '{:08b}'.format(int(eventtype))
                    bitevent = '1' + bitevent[1:]
                    neweventtype = int(bitevent, 2)
                    newline = '\tSetEvent {} Type {}\n'.format(line.strip().split(" ")[1], neweventtype)
                    lines_program.append(newline)
                    lines_new.append(newline)
                    changesMade = True
                else:
                    lines_program.append(line)
                    lines_new.append(line)
        # Changes made here need to happen up above too
        if changesMade:
            spawnscriptsdir = os.path.join(spawndir, ard)
            if not os.path.exists(spawnscriptsdir):
                os.mkdir(spawnscriptsdir)
            programfn = os.path.join(spawnscriptsdir, "program-"+currentProgram.lower().replace(" ", "")[2:].strip())
            with open(programfn, "w") as f:
                f.write(''.join(lines_program))
        open(evt_pth+".txt.new","w").write("".join(lines_new))