import tensorflow as tf
logPath="log"

x=tf.constant(2.0,name="x");
w=tf.Variable(0.8,name="w");
y_model=tf.multiply(w,x,name="output");

y_=tf.constant(0.0,name="correct_value");
loss=tf.pow(y_model-y_,2,name="pow");
train_step=tf.train.GradientDescentOptimizer(0.025).minimize(loss);
for value in [x,w,y_model,y_,loss]:
    tf.summary.scalar(value.op.name,value);
summaries=tf.summary.merge_all();


ss=tf.Session();
init=tf.global_variables_initializer();
xsum=tf.summary.FileWriter(logPath,ss.graph);
ss.run(init);

for i in range(100):
    xdat=ss.run(summaries);
    xsum.add_summary(xdat,i);
    x2=ss.run(train_step);

    x2,y2,w2=ss.run(x),ss.run(y_model),ss.run(w)
    print(w2)
    s2=ss.run(loss)

ss.close();