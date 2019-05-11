# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
import os

norm_size = 32


# def args_parse():
#     # construct the argument parse and parse the arguments
#     ap = argparse.ArgumentParser()
#     ap.add_argument("-m", "--model", required=True,
#                     help="path to trained model model")
#     ap.add_argument("-i", "--image", required=True,
#                     help="path to input image")
#     ap.add_argument("-s", "--show", action="store_true",
#                     help="show predict image", default=False)
#     args = vars(ap.parse_args())
#     return args


def predict(infolder,outfolder0,outfolder1):
    # load the trained convolutional neural network
    print("[INFO] loading network...")
    # model = load_model(args["model"])
    model = load_model("soma.model")

    for file in os.listdir(infolder):
        if file[-3:]=='png':
            print(file)
            # load the image
            # image = cv2.imread(args["image"])
            image=cv2.imread(infolder+"\\"+file)
            orig = image.copy()

            # pre-process the image for classification
            image = cv2.resize(image, (norm_size, norm_size))
            image = image.astype("float") / 255.0
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)

            # classify the input image
            result = model.predict(image)[0]
            # print (result.shape)
            proba = np.max(result)
            number=np.where(result == proba)[0]
            label = str(number)
            label = "{}: {:.2f}%".format(label, proba * 100)
            print(label)

            # if args['show']:
            # draw the label on the image
            output = imutils.resize(orig, width=400)

            cv2.putText(output, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)
            if int(number)==0:
                cv2.imwrite(outfolder0+"\\"+file,output);
            else:
                cv2.imwrite(outfolder1 + "\\" + file, output);
            # # show the output image
            # cv2.imshow("Output", output)
            # cv2.waitKey(0)


# python predict.py --model traffic_sign.model -i ../2.png -s
if __name__ == '__main__':
    # args = args_parse()
    # predict(args)

    infolder = "C:\\Users\Anzhi\Documents\WXWork\\1688850161522981\Cache\File\\2019-04\\2Dpng\\train\\0"
    outfolder0="C:\\Users\Anzhi\Documents\WXWork\\1688850161522981\Cache\File\\2019-04\\2Dpng\predict\\0\\0"
    outfolder1="C:\\Users\Anzhi\Documents\WXWork\\1688850161522981\Cache\File\\2019-04\\2Dpng\predict\\0\\1"
    predict(infolder,outfolder0,outfolder1)


