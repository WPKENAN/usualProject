from PIL import Image
#
#
#
# path="C:\\Users\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\image\\DogPlainText2048x2048.txt"
# file=open(path).readlines()
# print(len(file)-5)
#
#
# # img1=Image.open("C:\\Users\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\draft\\Debug\\1.ppm")
# # img2=Image.open("C:\\Users\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\draft\\Debug\\2.ppm")
# # img3=Image.open("C:\\Users\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\draft\\Debug\\3.ppm")
# # cpu=Image.open("C:\\Users\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\draft\\Debug\\cpu.ppm")
gpu=Image.open("C:\\Users\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\draft\\Debug\\CUDA5.ppm")
# #
# #
# #
# # img3.show()
print(gpu.size)
print(gpu.load()[0,0])
print(gpu.load()[2,0])
# # print(img3.load()[4000-1,2667-3])
# # print(img2.size)
# gpu.show()
# # cpu=Image.open("C:\\Useimg3.show()rs\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\draft\\Debug\\cpu.ppm")
# # cpu.show()
#
# # # print(img1.format)
# # print(img1.size)
# # img=Image.open("C:\\Users\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\image\Dog2048x2048.ppm").load();
# # imgCpu=Image.open("C:\\Users\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\draft\\Debug\\cpu.ppm").load();
# # imgGpu=Image.open("C:\\Users\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\draft\\Debug\\cuda.ppm").load();
# #
# # print(img[50,50])
# # print(imgCpu[50,50]);
# # print(imgGpu[50,50])
# #
# # print(img[2047,2047])
# # print(imgCpu[2047,2047]);
# # print(imgGpu[2047,2047])
# #
# # imgMoon=Image.open("C:\\Users\\Anzhi\\Documents\\Tencent Files\\3272346474\\FileRecv\\L1062\\xiangmu\\draft\\Debug\\moon.ppm");
# # print(imgMoon.size)
#
#
