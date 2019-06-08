import os
import random
import shutil





def first():
    train=0.8
    path="./images"
    labels_list=os.listdir(path);
    labels_list.sort();

    if os.path.exists("./train"):
        shutil.rmtree("./train")
    if os.path.exists("./val"):
        shutil.rmtree("./val")
    os.mkdir("./train")
    os.mkdir("./val")


    for label in labels_list:
        if os.path.exists("./train/"+label):
            shutil.rmtree("./train/"+label)
        os.mkdir("./train/"+label)
        if os.path.exists("./val/"+label):
            shutil.rmtree("./val/"+label)
        os.mkdir("./val/"+label)


    for label in labels_list:
        for fig in os.listdir(path+"/"+label):
            if random.random()<=train:
                shutil.copy(path+"/"+label+"/"+fig,"./train/"+label+"/"+fig)
            else:
                shutil.copy(path + "/" + label + "/" + fig, "./val/" + label + "/" + fig)

if __name__=="__main__":
    first()


