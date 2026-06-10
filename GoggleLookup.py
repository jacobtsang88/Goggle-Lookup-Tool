import json
DEFAULT_LIBRARY = "goggle_library.json"

def load_library(filepath):
    with open(filepath, "r", encoding = "utf-8") as f:
        library = json.load(f)
    return library

def find_goggles(library, wavelength):
    results = []
    for goggle in library:
        for band in goggle["bands"]:
            if(wavelength > band["start_nm"] and wavelength < band["stop_nm"]):
                results.append(goggle["product"])
                break 
                '''
                alright, so essentially there are overlaps in the bands sometimes
                which means i gotta just make sure theres only one band per goggle
                but OD is diff for each band, even when theres overlap. (???)
                '''
    return results

lib = load_library(DEFAULT_LIBRARY)
print(find_goggles(lib, 600))
