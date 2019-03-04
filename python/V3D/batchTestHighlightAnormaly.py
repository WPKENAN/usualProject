import os

def highlightAnormaly(swcFolder,resultFolder):
    print("highlightAnormaly start:")
    files = os.listdir(swcFolder)
    count = 0;
    for file in files:
        # print(file[-6:])
        if os.path.exists(resultFolder+"\\"+file):
            continue
        if file[-3:] == "swc":
            count = count + 1;
            print(file)
            commandStr = "D:/v3d_external/bin/vaa3d_msvc.exe " \
                         "/x highlightAnormaly.dll " \
                         "/f function " \
                         "/i {} /o {} /p 1 20 140 5 ".format(swcFolder+"\\"+file,resultFolder+"\\"+file)

            os.system(commandStr)


if __name__=="__main__":
    swcFolder="D:\soamdata\\released_annotations\\17302"
    resultFolder="D:\soamdata\\released_annotations\\org\\17302"
    highlightAnormaly(swcFolder,resultFolder)

    swcFolder = "D:\soamdata\\released_annotations\\18454"
    resultFolder = "D:\soamdata\\released_annotations\\org\\18454"
    highlightAnormaly(swcFolder, resultFolder)

    swcFolder = "D:\soamdata\\released_annotations\\17545"
    resultFolder = "D:\soamdata\\released_annotations\\org\\17545"
    highlightAnormaly(swcFolder, resultFolder)



