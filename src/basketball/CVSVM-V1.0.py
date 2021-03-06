#!/usr/bin/env python
# coding = utf-8
#
# Author: Archer Reilly
# Date: 24/DEC/2014
# File: CVSVM-V1.0.py
# Desc: SVM -- Spport Vector Machine
#
# Produced By CSRGXTU
import cv2
import numpy as np

from Utility import loadMatrixFromFile, loadSeasons, loadTeamIds

svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                    svm_type = cv2.SVM_C_SVC,
                    C=2.67, gamma=5.383 )
                    
# buildTrainingSets
# build training sets from raw data file
#
# @param inputFile
# @return numpy.ndarray
def buildTrainingSets(inputFile):
  res = []
  mat = loadMatrixFromFile(inputFile)
  for row in mat:
    res.append([row[0], float(row[4]), float(row[5]), float(row[9]), float(row[10])])

  return np.array(res).astype(np.float32)

# buildTrainingLabels
# build training labels from raw data file
#
# @param inputFile
# @return numpy.ndarray
def buildTrainingLabels(inputFile):
  res = []
  mat = loadMatrixFromFile(inputFile)
  for row in mat:
    res.append([[row[11]]])

  return np.array(res).astype(np.float32)

# buildTestingSets
# build testing sets from raw data file
#
# @param inputFile
# @return numpy.ndarray
def buildTestingSets(inputFile):
  res = []
  mat = loadMatrixFromFile(inputFile)
  for row in mat:
    res.append([row[0], float(row[4]), float(row[5]), float(row[9]), float(row[10])])

  return np.array(res).astype(np.float32)

# buildTestingLabels
# build testing labels from raw data file
#
# @param inputFile
# @return numpy.ndarray
def buildTestingLabels(inputFile):
  res = []
  mat = loadMatrixFromFile(inputFile)
  for row in mat:
    res.append([[row[11]]])

  return np.array(res).astype(np.float32)

# teamMain
# train and test for team
def teamMain():
  DIR = '/home/archer/Documents/maxent/data/basketball/leaguerank/'
  teamIds = loadTeamIds(DIR + 'teamidshortname.csv')
  teamNames = [x[1] for x in loadMatrixFromFile(DIR + 'teamidshortname.csv')]
  countTotal = 0
  total = 0

  for team in teamIds:
    trainData = buildTrainingSets(DIR + team + '-train.csv.knn')
    trainLabels = buildTrainingLabels(DIR + team + '-train.csv.knn')
    testData = buildTestingSets(DIR + team + '-test.csv.knn')
    testLabels = buildTestingLabels(DIR + team + '-test.csv.knn')
    total = total + len(testLabels)

    svm = cv2.SVM()
    svm.train(trainData, trainLabels, params=svm_params)
    svm.save('svm_data.dat')
    
    # Accuracy
    count = 0
    for i in range(len(testLabels)):
      ret = svm.predict(np.array([testData[i]]))
      if ret == testLabels[i][0]:
        count = count + 1
    countTotal = countTotal + count
    print 'INFO: Accuracy(', team, ')', count/float(len(testLabels))
  print 'INFO: Total Accuracy: ', countTotal/float(total)

# seasonMain
# train and test for seasons
def seasonMain():
  DIR = '/home/archer/Documents/maxent/data/basketball/leaguerank/'
  seasons = loadSeasons(DIR + 'seasons-18-Nov-2014.txt')
  countTotal = 0
  total = 0

  for season in seasons:
    trainData = buildTrainingSets(DIR + season + '-train.csv.knn')
    testData = buildTestingSets(DIR + season + '-test.csv.knn')
    trainLabels = buildTestingLabels(DIR + season + '-train.csv.knn')
    testLabels = buildTestingLabels(DIR + season + '-test.csv.knn')
    total = total + len(testLabels)

    svm = cv2.SVM()
    svm.train(trainData, trainLabels, params=svm_params)
    svm.save('svm_data.dat')

    # Accuracy
    count = 0
    for i in range(len(testLabels)):
      ret = svm.predict(np.array([testData[i]]))
      if ret == testLabels[i][0]:
        count = count + 1

    countTotal = countTotal + count
    print 'INFO: Accuracy(', season, ')', count/float(len(testLabels))

  print 'INFO: Total Accuracy: ', countTotal/float(total)

# main
# train and test for all
def main():
  DIR = '/home/archer/Documents/maxent/data/basketball/leaguerank/'
  seasons = loadSeasons(DIR + 'seasons-18-Nov-2014.txt')
  total = 0
  count = 0
  trainData = []
  trainLabels = []
  testData = []
  testLabels = []

  for season in seasons:
    tmpTrainData = buildTrainingSets(DIR + season + '-train.csv.knn').tolist()
    tmpTrainLabels = buildTestingLabels(DIR + season + '-train.csv').tolist()
    tmpTestData = buildTestingSets(DIR + season + '-test.csv').tolist()
    tmpTestLabels = buildTestingLabels(DIR + season + '-test.csv').tolist()
    
    trainData.extend(tmpTrainData)
    trainLabels.extend(tmpTrainLabels)
    testData.extend(tmpTestData)
    testLabels.extend(tmpTestLabels)

  trainData = np.array(trainData).astype(np.float32)
  trainLabels = np.array(trainLabels).astype(np.float32)
  testData = np.array(testData).astype(np.float32)
  testLabels = np.array(testLabels).astype(np.float32)
  total = len(testLabels)

  svm = cv2.SVM()
  svm.train(trainData, trainLabels, params=svm_params)
  svm.save('svm_data.dat')

  for i in range(len(testLabels)):
    ret = svm.predict(np.array([testData[i]]))
    if results[0][0] == testLabels[i][0]:
      count = count + 1
  
  print 'INFO: Total Accuracy: ', count/float(total)

if __name__ == '__main__':
  #print "+++++++++++++++++Main+++++++++++++++++++++++++"
  #main()
  print "+++++++++++++++teamMain+++++++++++++++++++++++"
  teamMain()
  print "++++++++++++++seasonMain++++++++++++++++++++++"
  seasonMain()
