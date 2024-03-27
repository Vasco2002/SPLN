import os
import re
import pprint
import csv

def getFilesInDirectory(directory):
    filePaths = []
    for fileName in os.listdir(directory):
        filePath = os.path.join(directory, fileName)
        if os.path.isfile(filePath):
            filePaths.append(filePath)
    return filePaths[-1:] + filePaths[:-1]

def printFiles(filesList):
    filesListR =  [dir.replace(directoryPath,"") for dir in filesList]
    print(filesListR)

def leia(file,dataset):
    with open(file, 'r') as f:
        for line in f:
            data = re.split(r'^([\w\s\W-]+?)\s+([-+]?\d*\.?\d+)(?:\s+\[.*\])?', line.strip())
            #print(data[1] + ' : ' + str(data[2]))
            if data[0] not in dataset.keys():
                #TODO: TBD -> Tipo
                dataset[data[1]] = [data[1],float(data[2]),"TBD"]

def makeCSV(dataset,rowList):
    for pal in dataset:
        rowList.append(dataset[pal])
    
    with open('sentiment.csv','w',newline='') as f:
        writer = csv.writer(f)
        for row in rowList:
            writer.writerow(row)

directoryPath = os.getcwd() + "/datasets"
filesList = getFilesInDirectory(directoryPath)
#printFiles(filesList)
dataset = {}
rowList = [["palavra","polaridade","tipo"]]

for file in filesList:
    print(file.replace(directoryPath+"/",""))
    if 'vader_lexicon' in file:
        leia(file,dataset)
        pprint.pprint(dataset)


makeCSV(dataset,rowList)