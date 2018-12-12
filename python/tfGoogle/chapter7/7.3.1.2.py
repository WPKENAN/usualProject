import tensorflow as tf
import numpy as np
import threading
import time

def MyLoop(coord,worker_id):
    print("{}{}".format(worker_id,coord.should_stop()))
    while not coord.should_stop():
        if np.random.rand() < 0.2:
            print("Stop from id:{}".format(worker_id));
            coord.request_stop();
        else:
            print("Working on id:{}".format(worker_id));

        time.sleep(2);

coord=tf.train.Coordinator();
threads=[
    threading.Thread(target=MyLoop,args=(coord,i)) for i in range(5)
]

for t in threads:
    t.start();

#等待所有进程退出，再执行这一行之后的程序
# coord.join(threads)

print("stop")