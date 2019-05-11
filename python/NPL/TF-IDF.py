from jieba.analyse import *
import re
with open('data.txt') as f:
    data=f.read()

with open('data.txt') as f:
    lines=f.readlines()
# data=re.sub('(钱夫人).*(])','',data)

out=open('out.txt','w')
# out.write(data)
# out.close()

for line in lines:
    if '----------------------------' in line:
        out.write('--------------------------------------------------------------------\n')
        continue
    line = re.sub('(【).*(】)', '', line)
    line = re.sub('(\[).*(\])', '', line)
    line = re.sub('(钱夫人).*(:)', '', line)
    line = re.sub('().*(:)', '', line)
    line = re.sub('(--).*(--)', '', line)
    line = re.sub('(//).*()', '', line)
    line = re.sub('(809).*()', '', line)
    line = re.sub('(=).*()', '', line)
    line = re.sub('(小仙女).*()', '', line)
    line = line.replace('亲亲.您拍下时候标注的是现货的话.是付款后3-7天左右安排发货噢.', '')
    line = line.replace('亲亲', '')
    line = line.replace(' ', '')
    line = line.replace('\n', '')
    if len(line)==0:
        continue
    out.write(line)
    out.write('\n')





data=re.sub('(【).*(】)','',data)
data=re.sub('(\[).*(\])','',data)
data=re.sub('(钱夫人).*(:)','',data)
data=re.sub('().*(:)','',data)
data=re.sub('(--).*(--)','',data)
data=re.sub('(//).*()','',data)
data=re.sub('(809).*()','',data)
data=re.sub('(=).*()','',data)
data=re.sub('(小仙女).*()','',data)
data=data.replace('亲亲.您拍下时候标注的是现货的话.是付款后3-7天左右安排发货噢.','')
data=data.replace('亲亲','')
data=data.replace(' ','')
data=data.replace('\n\n','')



print(data)
# for keyword,weight in extract_tags(data,withWeight=True):
#     print("{} {}".format(keyword,weight))

for keyword,weight in textrank(data,withWeight=True,topK = 30):
    print("{} {}".format(keyword, weight))