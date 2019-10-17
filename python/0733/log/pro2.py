#导入包
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
# import seaborn as sns

#读取数据
movies = pd.read_csv('./data/TMDB/tmdb_5000_movies.csv')
credits = pd.read_csv('./data/TMDB/tmdb_5000_credits.csv')
#json转换
def load_tmdb_credits(path):
    df = pd.read_csv(path)
    json_columns = ['cast', 'crew']
    for column in json_columns:
        df[column] = df[column].apply(json.loads)
    return df

def load_tmdb_movies(path):
    df = pd.read_csv(path)
    df['release_date'] = pd.to_datetime(df['release_date']).apply(lambda x: x.date())
    json_columns = ['genres', 'keywords', 'production_countries', 'production_companies', 'spoken_languages']
    for column in json_columns:
        df[column] = df[column].apply(json.loads)
    return df
def pipe_flatten_names(keywords):
    return '|'.join([x['name'] for x in keywords])
credits = load_tmdb_credits('./data/TMDB/tmdb_5000_credits.csv')
movies = load_tmdb_movies('./data/TMDB/tmdb_5000_movies.csv')
#合并两张表，删除公共列title
del credits['title']
df = pd.concat([movies, credits], axis=1)
#提取电影类型并显示
df['genres'] = df['genres'].apply(pipe_flatten_names)
df['genres'].head()