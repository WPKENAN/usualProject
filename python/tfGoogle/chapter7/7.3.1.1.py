import tensorflow as tf

q=tf.FIFOQueue(6,"int32");
init=q.enqueue_many(([1,100,1000,10000,100000,1000000],));
x=q.dequeue();
z=q.dequeue();
y=x+z;
q_inc=q.enqueue([y]);

with tf.Session() as sess:
    init.run();
    # print(sess.run(x))
    # print(sess.run(x))
    # print(sess.run([q_inc,x]))
    # print(sess.run([z,q_inc,x]))
    # print(sess.run([x, q_inc]))
    # print(sess.run([x, q_inc]))
    print(sess.run(x))
    print(sess.run(x))
    print(sess.run(x))
    print(sess.run(x))
    print(sess.run(x))
    # print(sess.run(x))
    # print(sess.run(x))
