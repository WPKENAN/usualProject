import time
N = 1000
for i in range(N):
    print("进度:{0}%".format((i + 1) * 100 / N), end="\r")
    time.sleep(0.001)