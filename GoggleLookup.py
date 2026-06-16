import json
DEFAULT_LIBRARY = "goggle_library.json"


def load_library(filepath):
    with open(filepath, "r", encoding = "utf-8") as f:
        library = json.load(f)
    return library

def find_goggles(library, wavelength) -> int:
    goggleList = [] #add goggle, OD, notes
    ODList = []
    for goggle in library:
        '''
        if theres 2 bands, for same goggle,
        pick the higher one. then put in
        jupyter notebook for ease of use. six seven.
        '''
        best_od = -1
        for band in goggle["bands"]:
            if(wavelength > band["start_nm"] and wavelength < band["stop_nm"]):
                if band["od"] > best_od:
                    best_od = band["od"]
        if best_od != -1:
            goggleList.append(goggle["product"])
            ODList.append(band["od"])
    return goggleList, ODList

def main():
    lib = load_library(DEFAULT_LIBRARY)
    tung = int(input("input wavelength: "))
    rizz, ODList = find_goggles(lib, tung)
    if rizz or ODList == []:
        print("no goggles found for that wavelength")
    for i in range(len(rizz)):
        print(f"goggle {i + 1}: {rizz[i]}, OD: {ODList[i]}")


main()
