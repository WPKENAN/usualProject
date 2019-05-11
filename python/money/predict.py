# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
import os

norm_size = 128


def predict(infolder,outfolder0,outfolder1):
    labels_list = os.listdir(".\\images");
    labels_list.sort();

    # load the trained convolutional neural network
    print("[INFO] loading network...")
    # model = load_model(args["model"])
    model = load_model("lenet5.model")

    for file in os.listdir(infolder):
        if file[-3:]=='png' or file[-3:]=='jpg' :
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
            # label = str(number)
            # print(number)
            label = "{}: {:.2f}%".format(labels_list[number[0]], proba * 100)
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

    infolder = "C:\\Users\Anzhi\Documents\\Tencent Files\\3272346474\FileRecv\\picture-sheji\\num\\num0"
    outfolder0="C:\\Users\Anzhi\Documents\Tencent Files\\3272346474\FileRecv\\picture-sheji"
    outfolder1="C:\\Users\Anzhi\Documents\Tencent Files\\3272346474\FileRecv\\picture-sheji"
    predict(infolder,outfolder0,outfolder1)


