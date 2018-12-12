import tensorflow as tf
import os

# print(__file__)
# print(os.getcwd())

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]));

num_shards=2;
instacance_per_shard=2;
for i in range(num_shards):
    filename=os.getcwd()+"/data.tfrecords-%.5d-of-%.5d"%(i,num_shards);
    writer=tf.python_io.TFRecordWriter(filename);
    for j in range(instacance_per_shard):
        example=tf.train.Example(features=tf.train.Features(feature={
            'i': _int64_feature(i),
            'j': _int64_feature(j)
        }))
        writer.write(example.SerializeToString())
    writer.close()

