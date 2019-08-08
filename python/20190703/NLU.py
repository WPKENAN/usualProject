from aip import AipNlp
""" 你的 APPID AK SK """
APP_ID = '16707980'
API_KEY = 'v9iWBNX8usLfy2MuDWQGSX2Q'
SECRET_KEY = 'xBOEUHxuFh6SmwCEjmag147fzsGgTVfF'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
text = "百度是一家高科技公司"
result=client.lexer(text)  # 分词,词性标注,专名识别
print(result)

text = "张飞"
client.depParser(text)  # 词语的句法结构信息（如“主谓”、“动宾”、“定中”等结构关系），并用树状结构来表示整句的结构（如“主谓宾”、“定状补”等）

word = "张飞"
client.wordEmbedding(word)  # 中文词向量

text = "床前明月光"
client.dnnlm(text)   # 输出切词结果并给出每个词在句子中的概率值,判断一句话是否符合语言表达习惯。


word1 = "北京";word2 = "上海"
client.wordSimEmbedding(word1, word2)  # 得到两个词的相似度

text1 = "强大";text2 = "富强"
client.simnet(text1, text2)


text = "三星电脑电池不给力"
options = {}
options["type"] = 13
result=client.commentTag(text, options)  # 对包含主观观点信息的文本进行情感极性类别（积极、消极、中性）的判断，并给出相应的置信度
print(result)


text = "苹果是一家伟大的公司"
result=client.sentimentClassify(text)  # 情感分析
print(result)

# title = "iphone手机出现“白苹果”原因及解决办法，用苹果手机的可以看下"
# content = "如果下面的方法还是没有解决你的问题建议来我们门店看下成都市锦江区红星路三段99号银石广场24层01室。"
# result=client.keyword(title, content)  # 输出多个内容标签以及对应的置信度，用于个性化推荐、相似文章聚合、文本内容分析等场景
# print(result)


title = "1"
content = "欧洲冠军联赛是欧洲足球协会联盟主办的年度足球比赛，代表欧洲俱乐部足球最高荣誉和水平，被认为是全世界最高素质、最具影响力以及最高水平的俱乐部赛事，亦是世界上奖金最高的足球赛事和体育赛事之一。"
result=client.topic(title, content)  # 对文章按照内容类型进行自动分类，首批支持娱乐、体育、科技等26个主流内容类型
print(result)



