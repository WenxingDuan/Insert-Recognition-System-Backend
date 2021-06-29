import argparse
import torch
from . import data_utils as du
from . import model_utils as mu
import os
import json


# Collect the input arguments
def process_arguments():
    ''' Collect the input arguments according to the syntax
        Return a parser with the arguments
    '''
    parser = argparse.ArgumentParser(
        description=
        'Uses a trained network to predict the input image - flower - name')

    parser.add_argument(
        '--image',
        action='store',
        dest='input_image_path',
        default=
        'C:\\Users\\Owner\\Desktop\Pytest\\A-classifier-with-PyTorch-master\\test_dataset',
        help='Folder path to the input image Folder')
    '''
    -path
    |--C15331005010
    |   |--image1.jpg
    |   |--image2.jpg
    |   |--image3.jpg
    |--C15408105005
    |   |--image1.jpg
    |   |--image2.jpg
    |   |--image3.jpg
    '''
    parser.add_argument(
        '--checkpoint',
        action='store',
        dest='checkpoint_file_path',
        default=
        'C:\\Users\\Owner\\Desktop\\Pytest\\A-classifier-with-PyTorch-master\\checkpoint_dir',
        help='Folder path to the checkpoint folder to use')
    '''
    -path
    |--vgg16.pth
    |--resnet50.pth
    '''
    parser.add_argument('--top_k',
                        action='store',
                        dest='topk',
                        default=2,
                        type=int,
                        help='top K most likely classes to return')

    parser.add_argument('--mapping',
                        action='store',
                        dest='insert_name_file',
                        default='insertID.json',
                        help='file for mapping of categories to real names')

    parser.add_argument('--gpu',
                        action='store_true',
                        default=True,
                        help='Use GPU. The default is CPU')

    return parser.parse_args()


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


def writeStatistics(path, statistics, errorPaths):
    with open(path, "w", encoding='utf-8') as f:
        f.write("=======================================\n")
        f.write("=======================================\n")
        f.write("=======================================\n")
        for i in statistics:
            f.write("物种名：{insect}, 正确数 {correct}, 错误数 {incorrect}\n".format(
                insect=i[0], correct=i[1], incorrect=i[2]))

        f.write("=======================================\n")
        f.write("=======================================\n")
        f.write("=======================================\n")

        for i in errorPaths:
            f.write("错误物种编号：{insect}, 路径 {path}\n".format(insect=i[0],
                                                          path=i[1]))


# Get input arguments and predict a probability for the flower's name
def main():
    # Get the input arguments
    input_arguments = process_arguments()

    # Set the device to cuda if specified
    default_device = torch.device(
        "cuda" if torch.cuda.is_available() and input_arguments.gpu else "cpu")

    imagePathList = os.listdir(input_arguments.input_image_path)
    modelPath = input_arguments.checkpoint_file_path
    modelList = os.listdir(modelPath)

    insertIDDict = json.load(open(input_arguments.insert_name_file))

    # Predict

    # probs, classes = mu.predict(input_arguments.input_image_path,
    #                             input_arguments.checkpoint_file_path,
    #                             default_device, input_arguments.topk)

    # i = 0
    # for specie in classes:
    #     print("your dataset named : " + specie +
    #           " predicted with probability: " + str(probs[i]))
    #     i += 1
    # pass
    statistics = []
    errorPaths = []
    log = open("log.txt", "w", encoding='utf-8')
    for insertClass in imagePathList:
        currPath = input_arguments.input_image_path + "\\" + insertClass
        imageList = os.listdir(currPath)
        insertName = str.lower(insertIDDict[insertClass])

        currectNum = 0
        incurrectNum = 0
        log.write("开始预测类别: " + insertClass + "\n")
        for theImage in imageList:
            imagePath = currPath + "\\" + theImage
            votingDict = {}
            # start voting
            
            for theModel in modelList:
                currModelPath = modelPath + "\\" + theModel
                print("Using " + theModel + " to predict " + imagePath)

                probs, classes = mu.predict(imagePath, currModelPath,
                                            default_device,
                                            input_arguments.topk)
                specie = findHighestProb(classes, probs)
                log.write("    使用 " + theModel + " 预测 " + imagePath +
                          "\n")
                log.write("        预测结果是: " + specie + "\n")
                if specie in votingDict:
                    votingDict[specie] = votingDict[specie] + 1
                else:
                    votingDict[specie] = 1

            predictedSpecies = str.lower(findHighestVote(votingDict)).replace(
                "_", " ")
            log.write("            投票结果是: " + specie + "\n")
            if predictedSpecies == insertName:
                currectNum = currectNum + 1
                log.write("            正确: 结果是 " + specie + "\n\n")

            else:
                incurrectNum = incurrectNum + 1
                print("ERROR: Predict: " + predictedSpecies + " Actual: " +
                      insertName)
                log.write("            错误: 预测为: " + predictedSpecies +
                          " 实际为: " + insertName + "\n\n")
                errorPaths.append([insertClass, imagePath])
        log.write("种类: " + insertClass + " 正确数: "+str(currectNum)+" 错误数: "+str(incurrectNum)+"\n\n")
        statistics.append([insertClass, currectNum, incurrectNum])

    writeStatistics(
        "C:\\Users\\Owner\\Desktop\\Pytest\\A-classifier-with-PyTorch-master\\statistics.txt",
        statistics, errorPaths)


if __name__ == '__main__':
    main()
