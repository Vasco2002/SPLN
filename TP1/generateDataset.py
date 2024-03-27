import os
import re
import pprint
import csv
import random
import sys

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
            if line != '':
                data = re.split(r'^([\w\s\W-]+?)\s+([-+]?\d*\.?\d+)(?:\s+\[.*\])?', line.strip())
                #print(data[1] + ' : ' + str(data[2]))
                if data[1] not in dataset.keys():
                    #TODO: -> Tipo
                    dataset[data[1]] = [data[1],float(data[2]),""]

def lexPT(file,dataset):
    # -4 a -0.1 | 0.1 a 4
    minN = -1.3
    maxN = -0.5
    minP = 1.3
    maxP = 0.5

    with open(file, 'r') as f:
        for line in f:
            if line != '':
                data = re.split(r'^([\w\s\W-]+?)\s+(\w+)', line.strip())
                #print(data)
                #print(data[1] + ' : ' + str(data[2]))
                if data[1] not in dataset.keys():
                    # Ativa polaridade mais agravada para palavrões e insultos
                    if data[1] == 'cú':
                        #print('MODO PALAVRAO')
                        minN = -3.4
                        maxN = -2.2

                    # Caso de exceção de trepa e trepar
                    if 'trepa' in data[1]:
                        #print('ENCONTREI TREPAR')
                        dataset[data[1]] = [data[1],0.6,""]
                    elif data[2] == 'POSITIVE' or data[2] == 'POSITIVO' or data[2] == 'POSITIV':
                        #print(data[2] + ': ' + data[1])
                        pol = round(random.uniform(minP, maxP), 1)
                        dataset[data[1]] = [data[1],pol,""]
                    elif data[2] == 'NEGATIVE' or data[2] == 'NEGATIVO':
                        #print(data[2] + ': ' + data[1])
                        pol = round(random.uniform(minN, maxN), 1)
                        dataset[data[1]] = [data[1],pol,""]
                    else:
                        print(data[2])
                        sys.exit()

                    #print(dataset[data[1]])

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

    if "lex_pt" in file:
        lexPT(file,dataset)

pprint.pprint(dataset)

makeCSV(dataset,rowList)