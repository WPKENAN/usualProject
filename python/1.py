import tensorflow as tf
logPath="tmp/log"

'''2018/09/13'''
cnt=tf.Variable(0,name="cnt");
a=tf.constant(1,name="a");
y=tf.add(cnt,a);
cnt=tf.assign(cnt,y);
init=tf.global_variables_initializer();
with tf.Session() as ss:
    ss.run(init);
    xss=ss.run(cnt);
    print(y)
    print(cnt)
    # xsum=tf.summary.FileWriter(logPath,ss.graph);

print("start")
with tf.Graph().as_default():
    a = tf.Variable(1, name="a")
    # a = tf.assign(a, tf.add(a,1),name="b")
    # a=a+1;
    a=tf.add(a,1)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(a))
        print(sess.run(a))
        print(sess.run(a))
        xsum = tf.summary.FileWriter(logPath, sess.graph);
'''
state=tf.Variable(0,name="a")
one = tf.constant(1)
new_value = tf.add(state,one)
update = tf.assign(state,new_value)
init=tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)#对变量进行初始化，执行（run）init语句
    for i in range(4):
        # print(sess.run(state))
        # print(sess.run(update))
        # print(update.eval())
        # print(state.eval())
        # print(update.eval())
'''

