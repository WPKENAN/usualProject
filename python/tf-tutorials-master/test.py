import tensorflow as tf
a = tf.constant([[3, 4, -1, 6],[2,3,4,5]])
a_new=tf.reshape(a, [8])
size_a = tf.size(a)
b = tf.gather(a_new, tf.nn.top_k(-a_new, k=8).indices)

sess = tf.Session()
idx_min= sess.run([b])
print(idx_min)
