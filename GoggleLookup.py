import json
DEFAULT_LIBRARY = "goggle_library.json"

#testing testing testing

def load_library(filepath):
    with open(filepath, "r", encoding = "utf-8") as f:
        library = json.load(f)
    return library

def find_goggles(library, wavelength) -> int:
    goggleList = [] #add goggle, OD, notes
    for goggle in library:
        for band in goggle["bands"]:
            if(wavelength > band["start_nm"] and wavelength < band["stop_nm"]):
                goggleList.append(goggle["product"])
                break 
                '''
                alright, so essentially there are overlaps in the bands sometimes
                which means i gotta just make sure theres only one band per goggle
                but OD is diff for each band, even when theres overlap. (???)
                '''
    if goggleList:
        return goggleList
    else:
        return "there are no goggles that support this wavelength."

def main():
    lib = load_library(DEFAULT_LIBRARY)
    tung = int(input("input wavelength: "))
    rizz = find_goggles(lib, tung)
    for i in range(len(rizz)):
        print(f"goggle {i + 1}: {rizz[i]}")


main()
