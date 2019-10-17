#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD



def get_year(x):
    try:
        y = int(x.strip()[-5:-1])
    except:
        y = 0

    return y

# 获取电影详细信息函数
def get_movie(df_movie, moive_list):
    # 根据电影ID获取电影详细信息
    df_movieId = pd.DataFrame(movie_list, index=np.arange(len(movie_list)), columns=['movieId'])
    corr_movies = pd.merge(df_movieId, movie_total, on='movieId')
    return corr_movies

def person_method(df_movie, pivot, movie, num):
    # 获取目标电影属性
    bones_ratings = pivot[movie]
    # 计算出电影跟该电影的皮尔森相关性
    similar_to_bones = pivot.corrwith(bones_ratings)
    corr_bones = pd.DataFrame(similar_to_bones, columns=['pearson'])
    # 弃去缺失值
    corr_bones.dropna(inplace=True)
    # 相关性与评论数合并
    corr_summary = corr_bones.join(df_movie[['movieId','ratingCount']].set_index('movieId'))
    # 刷选出对应数量的高关联性电影
    movie_list = corr_summary[corr_summary['ratingCount'] >= 100].sort_values('pearson', ascending=False).index[:num].tolist()
    return movie_list


def knn_method(movie_pivot, movie, num):
    # 压缩稀疏矩阵
    movie_pivot_matrix = csr_matrix(movie_pivot.values)
    # 我们用来计算最近邻居的算法是“brute”，我们指定“metric =cosine”，以便算法计算评级向量之间的余弦相似度。
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    # 训练模型
    model_knn.fit(movie_pivot_matrix)
    # 根据模型找到与所选电影最近6个（包含其本身）电影
    distances, indices = model_knn.kneighbors(movie_pivot.loc[[movie], :].values.reshape(1, -1), n_neighbors=num)
    # 获取电影ID列表
    movie_list = movie_pivot.iloc[indices[0], :].index
    return movie_list




if __name__=='__main__':
    # 导入电影链接文件
    links = pd.read_csv('F:\\datacollect\\links.csv')
    links.head()
    # 导入电影信息文件
    movies = pd.read_csv('F:\\datacollect\\movies.csv')
    movies.head()
    # 导入评分文件
    ratings = pd.read_csv('F:\\datacollect\\ratings.csv')
    ratings.head()
    movies_add_links = pd.merge(movies, links, on='movieId')
    # 获取电影年份
    movies_add_links['movie_year'] = movies_add_links['title'].apply(get_year)

    # 计算每个电影的被评论次数
    rating_counts = pd.DataFrame(ratings.groupby('movieId').count()['rating'])
    rating_counts.rename(columns={'rating': 'ratingCount'}, inplace=True)
    # 合并到一起
    movie_add_rating = pd.merge(movies_add_links, rating_counts, on='movieId')

    # 获取每个电影的平均评分并合并
    rating_means = pd.DataFrame(ratings.groupby('movieId').mean()['rating'])
    rating_means.columns = ['rating_mean']
    movie_total = pd.merge(movie_add_rating, rating_means, on='movieId')
    movie_total.head()

    combine_movie = pd.merge(ratings, rating_counts, on='movieId')
    combine_movie = combine_movie.dropna()
    combine_movie.head()

    combine_movie.ratingCount.quantile(np.arange(.5, 1, .05))
    popularity_threshold = 69
    # 根据位置进行筛选
    rating_popular_movie = combine_movie.query('ratingCount >= @popularity_threshold')
    rating_popular_movie.head()
    # 讲表格转化为2D矩阵
    movie_pivot = rating_popular_movie.pivot(index='movieId', columns='userId', values='rating').fillna(0)
    #knn_method(movie_pivot,5)
    movie_1 = ratings.groupby('movieId').count().sort_values('rating', ascending=False).index[0]
    print(movie_1)
    movie_total[movie_total.movieId == movie_1]
    movie_list = knn_method(movie_pivot, movie_1, 6)
    corr_movies = get_movie(movie_total, movie_list)
    print(corr_movies)
    #movie_pivot, movie, num

    # 看看用户多少，电影多少
    print(movie_pivot.shape)
    ratings.rating.value_counts(sort=True).plot('bar')
    plt.title('Rating Distribution\n')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.savefig('rating.png', bbox_inches='tight')
    plt.show()
    ### 可视化每年电影数量和每年电影被评论数量 ###
    # 设置画幅
    plt.figure(figsize=(16, 16))
    # 分层
    plt.subplot(2, 1, 1)
    # 每年电影数
    movie_total.groupby('movie_year')['ratingCount'].count().plot('bar')
    plt.title('Movies counts by years\n')
    plt.xlabel('years')
    plt.ylabel('counts')
    # 每年电影评论数
    plt.subplot(2, 1, 2)
    movie_total.groupby('movie_year')['ratingCount'].sum().plot('bar')
    plt.title('Movies ratings by years\n')
    plt.xlabel('years')
    plt.ylabel('ratings')
    plt.savefig('mix.png', bbox_inches='tight')
    plt.show()
    # 构建要使用与筛选的电影信息
    combine_movie = pd.merge(ratings, rating_counts, on='movieId')
    combine_movie = combine_movie.dropna()
    combine_movie.head()
    # 计算70%评论数为多少用以筛选
    combine_movie.ratingCount.quantile(np.arange(.5, 1, .05))
    # 选出评分数最多的电影id
    #备注，这里可以改成你自己喜欢的电影id，然后昨晚这个变量继续进行推荐

    # 获取电影ID列表
    movie_list = person_method(movie_total, movie_pivot, movie_1, 6)
    # 获取电影详细数据
    corr_movies = get_movie(movie_total, movie_list)
    print(corr_movies)


    #根据推荐的结果手动进行打分，以2分为满分，总共推荐了5部电影，
    target = [2, 2, 2, 2, 2]
    prediction = [0.5, 1.5, 1, 0.1, 1.2]#皮尔森准确率判断
    prediction_1= [0.5, 0.8, 1.2, 0.8, 1.8]
    error = []
    for i in range(len(target)):
        error.append(target[i] - prediction[i])
    squaredError = []
    absError = []
    for val in error:
        squaredError.append(val * val)  # target-prediction之差平方
        absError.append(abs(val))  # 误差绝对值
    print("皮尔森计算出来的RMSE的结果为:")
    print(sqrt(sum(squaredError) / len(squaredError)))
    # knn 算法的RMSE结果
    for i in range(len(target)):
        error.append(target[i] - prediction_1[i])
    squaredError = []
    absError = []
    for val in error:
        squaredError.append(val * val)  # target-prediction之差平方
        absError.append(abs(val))  # 误差绝对值
    print("knn 计算出来的RMSE的结果为:")
    print(sqrt(sum(squaredError) / len(squaredError)))  #



