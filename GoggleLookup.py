import json
DEFAULT_LIBRARY = "goggle_library.json"

#testing testing testing

def load_library(filepath):
    with open(filepath, "r", encoding = "utf-8") as f:
        library = json.load(f)
    return library

def find_goggles(library, wavelength) -> int:
    goggleList = [] #add goggle, OD, notes
    ODList = []
    for goggle in library:
        for band in goggle["bands"]:
            if(wavelength > band["start_nm"] and wavelength < band["stop_nm"]):
                goggleList.append(goggle["product"])
                ODList.append(band["od"])
                break 
                '''
                if theres 2 bands, pick the higher one. then put in
                jupyter notebook for ease of use. six seven.
                '''
    if goggleList:
        return goggleList, ODList
    else:
        return "there are no goggles that support this wavelength."

def main():
    lib = load_library(DEFAULT_LIBRARY)
    tung = int(input("input wavelength: "))
    rizz, ODList = find_goggles(lib, tung)
    for i in range(len(rizz)):
        print(f"goggle {i + 1}: {rizz[i]}, OD: {ODList[i]}")


main()
