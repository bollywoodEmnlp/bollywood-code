##----------------------------------------------------------------------------------------------------------##
##     													    ##
##  code for running the "Bollywood related artists"						            ##
##													    ##
##  this code needs package tabulate,  please install the package via:					    ##
##													    ##
##         --------------------------								            ##
##        |   pip install tabulate   |									    ##
##         --------------------------									    ##
##   													    ##
##  type in command in the command line:								    ##
##													    ##	
##     -------------------------------------------------------------------------------------------------    ##
##    |  python calcFscore.py standard.txt miOut116.txt degree116.txt spec116.txt id_bollyArtist.map    |   ##	
##     -------------------------------------------------------------------------------------------------    ##
##   													    ##
##  standard.txt          :   gold_standard_set.txt						            ##
##  miOut116.txt          :   co-occurrence results for 116 artists					    ##
##  degree116.txt         :   degree results for 116 artists						    ##
##  spec116.txt           :   spectral mean vector distance for 116 artsts  			            ##
##  id_bollyArtist.map    :   map of artists, integer to string 					    ##
##													    ##
##----------------------------------------------------------------------------------------------------------##




import operator
from tabulate import tabulate
import numpy
import math
import re
import sys
import random
from collections import namedtuple


#######    >> definition of tuples


Item = namedtuple("Item", ['name', 'coScore', 'degree', 'spectral', 'clas'])
Fscore = namedtuple("Fscore", ['name', 'precision', 'recall', 'fscore'])



def ReadIn(filename):
    item = []
    fp = open(filename)
    while 1:
        line = fp.readline()
	if not line:
	    break
	line = line.rstrip('\n').strip()
	#line = line.lower()
	item.append(line.strip('|'))
    fp.close()
    return item


def avg(nameout):
    precision = 0.0
    recall = 0.0
    f1score = 0.0
    
    for n in nameout:
	precision += float(n.precision)
	recall += float(n.recall)
	f1score += float(n.fscore)
    precision /= len(nameout)
    recall /= len(nameout)
    f1score /= len(nameout)
    
    return Fscore("avg",precision, recall, f1score)




####     Sigmoid functon



def h(theta, item):
    tmp = theta[0] * 1.0 + theta[1] * float(item.coScore) + theta[2] * float(item.degree) + theta[3] * float(item.spectral)
    if -tmp > 700:
        return 0
    else:
        return 1 / (1 + math.exp(-tmp))



#########################

def linear(theta, item):
    return theta[1] * float(item.coScore) - theta[2] * float(item.spectral)
      

#########################

####       testing <<  


def test(index, nameList, theta, goldList, indexMap, choice):

    items = nameList[index]

    m = len(items)
    g = len(goldList[index])
    
    acc = 0
    trueOnes = 0
    myOnes   = 0
    nameSelect = []
    itemSelect = {}
    
    for i in range(m):
        if h(theta, items[i]) >= 0.5:
	    itemSelect[items[i].name] = h(theta, items[i])
    
    itemSorted = sorted(itemSelect.items(), key = operator.itemgetter(1), reverse = True)
 
 
    ######    >> select at most top ten related artists 
    
    num = 0
    for key, val in itemSorted:
        if num > 10:
	    break
	num += 1
	s = key + "|" + str(val)
	nameSelect.append(s)
	if key in goldList[index]:
	    acc += 1
    
    #######    >> calculate precision, recall, f1score

    myOnes = len(nameSelect)
    if myOnes == 0:
        precision = 0
    else:
        precision = float(acc) / float(myOnes)
    
    recall    = float(acc) / float(g)
    if (precision == 0 and recall == 0):
        f1score = 0
    else:
        f1score   = 2 * precision * recall / (precision + recall)
    fscore = Fscore(indexMap[index], precision, recall, f1score)

    #######    >>   choice = false, return recommendated artists.

    if choice == True:
        return fscore
    else:
        return nameSelect



#############     >> logistic regression  Training


def train(items, lambda0, alpha, start, end):
    
    trainTimes  = 100
    m           = end - start
    thetaBefore = [0.0]*4
    thetaAfter  = [0.0]*4
    thetaBefore = [0.0]*4
    thetaAfter  = [0.0]*4
    
    fscoreTuple = []
    
    ######    >> loop for iteration, gradient descent

    for i in range(trainTimes):
        tmp = 0.0
        for j in range(m):
            tmp += (h(thetaBefore, items[j]) - float(items[j].clas)) * 1.0
	tmp = tmp * alpha / m
	thetaAfter[0] -= tmp
	tmp = 0.0
	for j in range(m):
	    tmp += (h(thetaBefore, items[j]) - float(items[j].clas)) * float(items[j].coScore)
        tmp = alpha * (tmp / m + lambda0 * thetaBefore[1] / m)
	thetaAfter[1] -= tmp
        tmp = 0.0
	for j in range(m):
	    tmp += (h(thetaBefore, items[j]) - float(items[j].clas)) * float(items[j].degree)
	tmp = alpha * (tmp / m + lambda0 * thetaBefore[2] / m)
	thetaAfter[2] -= tmp
	tmp = 0.0
	for j in range(m):
	    tmp += (h(thetaBefore, items[j]) - float(items[j].clas)) * float(items[j].spectral)
	tmp = alpha * (tmp / m + lambda0 * thetaBefore[3] / m)
	thetaAfter[3] -= tmp
        for j in range(4):
	    thetaBefore[j] = thetaAfter[j]
    
    return thetaBefore




############################

###  Read in all the files

fileGold     = sys.argv[1]
fileCoScore  = sys.argv[2]
fileDegree   = sys.argv[3]
fileSpectral = sys.argv[4]
fileNameFile = sys.argv[5]


gold     = ReadIn(fileGold)
CoScore  = ReadIn(fileCoScore)
Degree   = ReadIn(fileDegree)
Spectral = ReadIn(fileSpectral)
nameFile = ReadIn(fileNameFile)


############################

##  namd map,   integer - name

indexMap = {}
for line in nameFile:
    line = line.split('\t')
    indexMap[line[0]] = line[2]


############################


####
##  store standard set


standard = {}
for line in gold:
    line = line.split('\t')
    standard[line[0]] = line[1].split('|')


#####

#####
##  Store three features


## Co-occurrency 


coList  = {}

for i in range(len(CoScore)):
    line = CoScore[i]
    line = line.split('\t')
    coList[line[0]] = line[1].split('|')

####
##  Degree


deList  = {}

for i in range(len(Degree)):
    line = Degree[i].split('\t')
    deList[line[0]] = line[1]


####
##  Spectral Mean Distance


specList = {}

for i in range(len(Spectral)):
    line = Spectral[i].split('\t')
    specList[line[0]] = line[1].split('|')


####
##  End in reading in features



#########################


####
##  Start building training features

####     Item = namedtuple("Item", ['name', 'coScore', 'degree', 'spectral', 'clas'])


nameList = {}


for index in standard:
    
    nameSpec = {}
    for item in specList[index]:
        item = item.split('/')
        nameSpec[item[0]] = item[1]

    nameCo   = {}
    for item in coList[index]:
        item = item.split('/')
        nameCo[item[0]] = item[1]

    items = []
    mainDegreeScore = float(deList[index])
    for item in nameCo:
        itemCoScore      = float(nameCo[item])
        itemSpecScore    = float(nameSpec[item])
	if mainDegreeScore > 0:
            itemDegreeScore  = float(deList[item]) / mainDegreeScore
	else:
	    itemDegreeScore = float(deList[item])
        clas = 0
        if item in standard[index]:
            clas = 1

        items.append(Item(item, itemCoScore, itemDegreeScore, itemSpecScore, clas))

    nameList[index] = items
    
    ####


#######################


####           >>   shuffle the index list, for 10-fold validation


index = []
for key in nameList:
    index.append(key)

random.shuffle(index)


#############################


####     >>   create list and dictionary to store the results


avgFscore     = []
avgFscoreName = {}
table         = []
totalLength   = len(nameList)


############################

####     >> 10-fold


step = int (totalLength / 10);


for iterate in range(0, totalLength, step):
    
    #######     >>   e.g. stepRange = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] index for testing list

    print "total iteration times # 10\t|\titerate #", iterate/step, "..."


    stepRange = []
    iteStart = iterate
    iteEnd   = min(totalLength, iterate + step)
    for j in range(iteStart, iteEnd):
        stepRange.append(j)
    
    #######      >>    creating trainling list and testing list

    trainList = []
    testList  = []
 
    for i in range(len(index)):
	if i in stepRange:
            testList.append(index[i])
	else:
	    trainList.append(index[i])
    
    ##########     >> alpha : learning rate for gradient descent, lambda0 : regularization parameter 

    alpha = 0.1
    lambda0 = 1
    
    ##########     >>  parameters for three features, theta[0] is the offset
    
    theta = [0.0] * 4



    #########    to create a unbalanced training set, the ratio of number of 1 and 0 is 1:1.2 


    items = []
    for i in trainList:
        for item in nameList[i]:
            if item.clas == 1:
                items.append(item)
    trueLength = len(items)

    count = 0
    for i in trainList:
        for item in nameList[i]:
            if item.clas == 0 and count < trueLength * 1.2:
	        items.append(item)
	        count += 1

    random.shuffle(items)

    ####################################


    trainSize = int(len(items))
    
    accuracy = 0.0

    #########          >>   training the model  

    print "begin training ..........."

    thetaTrain = train(items, lambda0, alpha, 0, len(items))
    
    print "finish training .........."    
    print
    print "theta is : "
    
    print "\t\t", thetaTrain
    print

    #########          >>   testing the model

    print "begin testing ............"
    print

    for i in testList:
	avgFscore.append(test(i, nameList, thetaTrain, standard, indexMap, True))
        avgFscoreName[i] = test(i, nameList, thetaTrain, standard, indexMap, False)
	tmp = []
	tmp.append(indexMap[i])
	for key in avgFscoreName[i]:
	    key = key.split('|')
            tmp.append(indexMap[key[0]])
	
	#########      >> table to store the results, related artists' names

	table.append(tmp)


    print "finish testing ..........."
    print


print
print

for key in table:
    for val in key:
        print val, '|',
    print


print
##    print len(avgFscore)


######       >> calculate average f1score 

avgfscore = avg(avgFscore)
avgFscore.append(avgfscore)
table = []
for i in range(len(avgFscore)):
    table.append(avgFscore[i])

print
print


headers = ["names", "precision", "recall", "F1-score"]

print tabulate(table, headers, tablefmt = "rst")



#####  calculate Mrr


#avgMrr = 0.0
#for i in range(len(mainList)):
#    gold = goldList[mainList[i]]
#    candidate = avgFscoreName[mainList[i]]
#    candidateDict = {}
#    for element in candidate:
#        element = element.split('|')
#	candidateDict[element[0]] = float(element[1])
#    sortedCandidate = sorted(candidateDict.items(), key = operator.itemgetter(1), reverse = True)
#    mrr = 0.0
#    num = 0.0
#    #print gold
#    #for k, v in sortedCandidate:
#    #    print k,
#    #print
#    for j in range(len(gold)):
#	caIndex = 0
#        for k, v in sortedCandidate:
#	    caIndex += 1
#	    if int(gold[j]) == int(k):        
#		mrr += float(1/float(j+1)) * float(1/float(caIndex))
#		num += float(1/float(j+1))
#		break
#    if num != 0:
#        mrr /= num
#    avgMrr += mrr
#    #print
#    print mainList[i], mrr
#print "Avg : " + str(avgMrr/float(20))
