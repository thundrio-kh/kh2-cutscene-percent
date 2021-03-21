import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

# For the logo screenshot goofys death
# In a "Has science gone too far...."

TITLE = "KH2 Cutscene Percent"

arddir = os.path.join(os.getcwd(), "extracted_ards")
spawndir = os.path.join("spawnscripts")

assets = []

for ard in os.listdir(spawndir):
    programs = []
    for fn in os.listdir(os.path.join(spawndir, ard)):
        programs.append(os.path.join(spawndir, ard, fn))

        
    a = {
        "name": "ard/{}".format(ard),
        "method": "binarc",
        "source": [
            {
                "name": "evt",
                "type": "AreaDataScript",
                "method": "areadatascript",
                "source": [            
                    {
                        "name": programs[i].replace("\\", "/"),
                    }
                    for i in range(len(programs))
                ]
            }
        ]
    }

    assets.append(a)

mod = {
    "originalAuthor": "Thundrio",
    "description": """Do you ever reminisce about how when you played vanilla KH1 you got to watch every cutscene, without worrying that you are being peer pressured by others into skipping the cutscene?
Well fear no more, because now that great feature is brought to KH2! Relive every exciting moment, from Goofy's death to Goofy's death!
Compatible with GOA mod. Report any bugs at https://github.com/thundrio-kh/kh2-cutscene-percent/issues""",
    "title": TITLE,
    "assets": assets,
    "logo": "logo.png"
}
import yaml
yaml.dump(mod, open("mod.yml", "w"))