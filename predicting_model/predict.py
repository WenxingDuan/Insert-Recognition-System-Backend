import argparse
import torch
import os
from . import data_utils as du
from . import model_utils as mu


# Collect the input arguments
# def process_arguments():
#     ''' Collect the input arguments according to the syntax
#         Return a parser with the arguments
#     '''
#     parser = argparse.ArgumentParser(
#         description=
#         'Uses a trained network to predict the input image - flower - name')

#     parser.add_argument('--image',
#                         action='store',
#                         dest='input_image_path',
#                         default='your_dataset/valid/5/image_05209.jpg',
#                         help='File path to the input flower image')

#     parser.add_argument('--checkpoint',
#                         action='store',
#                         dest='checkpoint_file_path',
#                         default='checkpoint.pth',
#                         help='File path to the checkpoint file to use')

#     parser.add_argument('--top_k',
#                         action='store',
#                         dest='topk',
#                         default=2,
#                         type=int,
#                         help='top K most likely classes to return')

#     parser.add_argument('--mapping',
#                         action='store',
#                         dest='cat_name_file',
#                         default='cat_to_name.json',
#                         help='file for mapping of categories to real names')

#     parser.add_argument('--gpu',
#                         action='store_true',
#                         default=False,
#                         help='Use GPU. The default is CPU')

#     return parser.parse_args()


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


def predict(input_image_path, topk, gpu):
    modelPath = os.path.dirname(__file__) + "\\checkpoint_dir"
    # mapping = os.getcwd() + "\\insertID.json"
    default_device = torch.device(
        "cuda" if torch.cuda.is_available() and gpu else "cpu")

    # probs, classes = mu.predict(input_image_path, checkpoint_file_path,
    #                             default_device)
    modelList = os.listdir(modelPath)
    votingDict = {}

    for theModel in modelList:
        currModelPath = modelPath + "\\" + theModel
        # print("Using " + theModel + " to predict " + imagePath)

        probs, classes = mu.predict(input_image_path, currModelPath,
                                    default_device, topk)
        specie = findHighestProb(classes, probs)
        # log.write("    使用 " + theModel + " 预测 " + imagePath + "\n")
        # log.write("        预测结果是: " + specie + "\n")
        if specie in votingDict:
            votingDict[specie] = votingDict[specie] + 1
        else:
            votingDict[specie] = 1

    predictedSpecies = str.lower(findHighestVote(votingDict)).replace("_", " ")

    return predictedSpecies


# Get input arguments and predict a probability for the flower's name
# def main():
#     # Get the input arguments
#     input_arguments = process_arguments()

#     # Set the device to cuda if specified
#     default_device = torch.device(
#         "cuda" if torch.cuda.is_available() and input_arguments.gpu else "cpu")

#     # Predict
#     probs, classes = mu.predict(input_arguments.input_image_path,
#                                 input_arguments.checkpoint_file_path,
#                                 default_device, input_arguments.topk)

#     i = 0
#     for specie in classes:
#         print("your dataset named : " + specie +
#               " predicted with probability: " + str(probs[i]))
#         i += 1

#     pass

# if __name__ == '__main__':
#     main()