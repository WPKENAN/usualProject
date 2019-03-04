import tensorflow as tf
import sys

# print(sys._getframe().f_lineno)

word_labels=tf.constant([2,0]);
predict_logits=tf.constant([[2.0,-1.0,3.0],[1.0,0.0,-0.5]]);
loss=tf.nn.sparse_softmax_cross_entropy_with_logits(labels=word_labels,logits=predict_logits)

# sys._getframe()
# print(sys._getframe().f_code.co_name)  # 当前函数名
# print(sys._getframe().f_lineno)  # 当前行号
with tf.Session() as sess:
    print("line: ",sys._getframe().f_lineno)
    print(sess.run(loss))


word_prob_distribution=tf.constant([[0,0,1],[1,0,0]]);
loss=tf.nn.softmax_cross_entropy_with_logits(labels=word_prob_distribution,logits=predict_logits);

with tf.Session() as sess:
    print("line: ",sys._getframe().f_lineno);
    print(sess.run(loss))



word_prob_smooth=tf.constant([[0.01,0.01,0.98],[0.98,0.01,0.01]]);
loss=tf.nn.softmax_cross_entropy_with_logits(labels=word_prob_smooth,logits=predict_logits);
with tf.Session() as sess:
    # print(sys._getframe(0).f_code.co_name)
    print("line: ",sys._getframe().f_lineno)
    print(sess.run(loss))