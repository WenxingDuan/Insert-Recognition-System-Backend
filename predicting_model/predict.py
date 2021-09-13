# -*- coding: utf-8 -*-
import argparse
import torch
import os
import sys
from . import data_utils as du
from . import model_utils as mu


def findHighestProb(classes, probs):
    highest = ""
    tempProb = 0
    for i in range(0, len(probs)):
        if probs[i] > tempProb:
            tempProb = probs[i]
            highest = classes[i]
    return highest


def findHighestVote(votingDict):
    highest = ""
    voteNum = 0
    for i in votingDict:
        if votingDict[i] > voteNum:
            voteNum = votingDict[i]
            highest = i
    return highest


def predict(input_image_path, topk):
    modelPath = os.path.dirname(__file__) + "/MODEL"
    default_device = torch.device("cpu")

    # print('1', file=sys.stderr)

    modelList = os.listdir(modelPath)
    votingDict = {}
    # print('2', file=sys.stderr)

    for theModel in modelList:
        currModelPath = modelPath + "/" + theModel
        # print('3', file=sys.stderr)

        probs, classes = mu.predict(input_image_path, currModelPath,
                                    default_device, topk)
        specie = findHighestProb(classes, probs)
        # print('4', file=sys.stderr)

        if specie in votingDict:
            votingDict[specie] = votingDict[specie] + 1
        else:
            votingDict[specie] = 1

    predictedSpecies = str.lower(findHighestVote(votingDict)).replace("_", " ")
    # print('5', file=sys.stderr)

    return predictedSpecies


def predictPercentage(input_image_path, topk):
    modelPath = os.path.dirname(__file__) + "/MODEL"
    default_device = torch.device("cuda")

    modelList = os.listdir(modelPath)
    votingDict = {}
    classLsit = []
    probsList = []
    for theModel in modelList:
        currModelPath = modelPath + "/" + theModel
        probs, classes = mu.predict(input_image_path, currModelPath,
                                    default_device, topk)
        prob_digit = [prob / sum(probs) for prob in probs]
        classLsit = classLsit + classes
        probsList = probsList + prob_digit

    probDict = concludeProb(classLsit, probsList, len(modelList))

    return probDict


def concludeProb(classLsit, probsList, modelNumber):
    index = 0
    probDict = {}
    for insert in classLsit:
        if insert in probDict.keys():
            probDict[insert] = probDict[insert] + probsList[index]
        else:
            probDict[insert] = probsList[index]
        index += 1
    for insert in probDict.keys():
        probDict[insert] = probDict[insert] / modelNumber

    sorted_prob = sorted(probDict.items(),
                         key=lambda kv: (kv[1], kv[0]),
                         reverse=True)
    returnJson = []
    for i in sorted_prob:
        tempDict = {}
        tempDict["latin_name"] = i[0].replace("_", " ")
        tempDict["percentage"] = round(i[1], 4)
        returnJson.append(tempDict)
    return returnJson
