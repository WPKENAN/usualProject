import os
import pandas as pd
import numpy as np
import time
import collections
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

movie_date={'BLACK PANTHER':['2017-11-3','2018-2-12'],
            'BLACKkKLANSMAN':['2018-5-14','2018-8-10'],
            'BOHEMIAN RHAPSODY':['2017-7-17','2018-10-25'],
            'THE FAVOURITE':['2018-7-9','2019-2-12'],
            'GREEN BOOK':['2018-8-14','2019-3-12'],
            'ROMA':['2018-8-30','2018-11-21'],
            'A STAR IS BORN':['2018-8-31','2018-10-5'],
            'VICE':['2018-10-3','2018-12-25']}


movie_director={'BLACK PANTHER':['Ryan Coogler','Chadwick Boseman','Michael B. Jordan'],
            'BLACKkKLANSMAN':['Spike Lee','John David Washington','Adam Driver'],
            'BOHEMIAN RHAPSODY':['Bryan Singer','Rami Malek','Lucy Boynton'],
            'THE FAVOURITE':['Yorgos Lanthimos','Olivia Colman','Emma Stone'],
            'GREEN BOOK':['Peter Farrelly','Viggo Mortensen','Mahershala Ali'],
            'ROMA':['Alfonso Cuarón','Yalitza Aparicio','Marina de Tavira'],
            'A STAR IS BORN':['Bradley Cooper','Andrew Dice Clay','Lady Gaga'],
            'VICE':['Adam McKay','Christian Bale','Amy Adams']}

movie_revenue={'BLACK PANTHER':1346913161,
            'BLACKkKLANSMAN':93304264,
            'BOHEMIAN RHAPSODY':903655259,
            'THE FAVOURITE':95918706,
            'GREEN BOOK':320788183,
            'ROMA':51000000,
            'A STAR IS BORN':434888866,
            'VICE':76073488}
def readCsv(path):
    df = pd.read_csv(path, header=0)
    # print(df)
    data = df.values
    # max_=max(data[:,0])
    # dt=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(max_))
    # timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return data
    # print(dt)
    # print(timeArray)
    # print(type(data[0,1]))
    # data.sort(axis=0)
    # print(data)
    # print(data[data[:,0]<1466638597].shape)
    # return data

def ymd2timestd(y,m,d):
    format_time='{}-{}-{} {}:{}:{}'.format(y,m,d,0,0,0)
    ts = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(ts)
    # print(timestamp)
    return timestamp

def calAllCounts(data):
    for movie in movie_date:
        count = 0;
        print(movie)
        for i in range(data.shape[0]):

            if (movie.lower() in data[i,1] or movie.replace(' ','-').lower() in data[i,1] or movie.replace(' ','').lower() in data[i,1]):
                if movie == 'ROMA' or movie == 'VICE':
                    if 'movie' in data[i,1]:
                        count+=1
                else:
                    count+=1
            elif movie_director[movie][0].lower() in data[i, 1] or movie_director[movie][1].lower() in data[i, 1] or movie_director[movie][2].lower() in data[i, 1]:
                count+=1
        print(count)

def calCounts(data,movie):
    count=0
    for i in range(data.shape[0]):
        if movie.lower() in data[i, 1] or movie.replace(' ', '-').lower() in data[i, 1] or movie.replace(' ','').lower() in data[i, 1]:
            if movie == 'ROMA' or movie == 'VICE':
                if 'movie' in data[i, 1]:
                    count += 1
            else:
                count += 1

        elif movie_director[movie][0].lower() in data[i, 1] or movie_director[movie][1].lower() in data[i, 1] or \
                movie_director[movie][2].lower() in data[i, 1]:
            count += 1
    return count

def calMeanLength(data,movie):
    count = 0
    length=0
    for i in range(data.shape[0]):
        if movie.lower() in data[i, 1] or movie.replace(' ', '-').lower() in data[i, 1] or movie.replace(' ',
                                                                                                         '').lower() in \
                data[i, 1]:
            if movie == 'ROMA' or movie == 'VICE':
                if 'movie' in data[i, 1]:
                    count += 1
                    length+=len(data[i,1].split(' '))
            else:
                count += 1
                length+=len(data[i,1].split(' '))

        elif movie_director[movie][0].lower() in data[i, 1] or movie_director[movie][1].lower() in data[i, 1] or \
                movie_director[movie][2].lower() in data[i, 1]:
            count += 1
            length+=len(data[i,1].split(' '))
    print(count)
    return length/count

def calPreLength(data,movie='GREEN BOOK',predate='1999-02-02'):
    predate=predate.split('-')
    # print(predate)
    pretimestamp=ymd2timestd(predate[0],predate[1],predate[2]);
    # print(pretimestamp)
    tmpdata=data[data[:,0]<pretimestamp];
    meanlength=calMeanLength(tmpdata,movie)
    count=calCounts(tmpdata,movie)

    return meanlength,count

def calPrePostLength(data,movie='GREEN BOOK',predate='1999-02-02',postdate='1999-02-02'):
    predate=predate.split('-')
    postdate=postdate.split('-')
    # print(predate)
    pretimestamp=ymd2timestd(predate[0],predate[1],predate[2]);
    posttimestamp=ymd2timestd(postdate[0],postdate[1],postdate[2]);

    # print(pretimestamp)
    tmpdata=data[data[:,0]>=pretimestamp];
    tmpdata=tmpdata[tmpdata[:,0]<posttimestamp]
    meanlength=calMeanLength(tmpdata,movie)
    count=calCounts(tmpdata,movie)

    return meanlength,count

def calPostLength(data,movie='GREEN BOOK',postdate='1999-02-02'):
    postdate=postdate.split('-')
    posttimestamp=ymd2timestd(postdate[0],postdate[1],postdate[2]);

    tmpdata=data[data[:,0]>=posttimestamp]
    meanlength=calMeanLength(tmpdata,movie)
    count=calCounts(tmpdata,movie)

    return meanlength,count

def calAllLength(data,movie='GREEN BOOK'):

    meanlength=calMeanLength(data,movie)
    count=calCounts(data,movie)

    return meanlength,count

def writeCsv(path,x,y):
    out=open(path,'w')
    for i in range(len(x)):
        out.write("{},{}\n".format(x[i,0],y[i]))
    out.close()


def drawLength(data):
    # pre
    meanlengths=[]
    counts=[]
    revenue=[]
    for movie in movie_date:
        meanlength,count=calPreLength(data,movie,movie_date[movie][0])
        meanlengths.append(meanlength)
        counts.append(count)
        revenue.append(movie_revenue[movie])
    meanlengths=np.array(meanlengths)
    counts=np.array(counts)
    revenue=np.array(revenue)

    plt.figure(figsize=(40, 20))
    plt.subplot(3,3,1)
    lr = LinearRegression()
    meanlengths = np.reshape(meanlengths, (len(meanlengths), 1))
    lr.fit(meanlengths, revenue)
    xi=np.linspace(np.min(meanlengths),np.max(meanlengths),20)
    xi = np.reshape(xi, (len(xi), 1))
    y_pred = lr.predict(xi)
    plt.scatter(meanlengths, revenue)
    plt.plot(xi,y_pred,color='r')
    plt.grid()
    plt.title("Revenue vs. pre mean tweet length")
    plt.xlabel("pre mean tweet length")
    plt.ylabel('Revenue')
    writeCsv("Revenue vs. pre mean tweet length"+".csv",meanlengths,revenue)


    plt.subplot(3, 3, 4)
    lr = LinearRegression()
    counts = np.reshape(counts, (len(counts), 1))
    lr.fit(counts, revenue)
    xi = np.linspace(np.min(counts), np.max(counts), 20)
    xi = np.reshape(xi, (len(xi), 1))
    y_pred = lr.predict(xi)
    plt.scatter(counts, revenue)
    plt.plot(xi, y_pred,color='r')
    plt.grid()
    plt.title("Revenue vs. pre tweet count")
    plt.xlabel("pre tweet count")
    plt.ylabel('Revenue')
    writeCsv("Revenue vs. pre tweet count" + ".csv", counts, revenue)



    #pre-post
    meanlengths = []
    counts = []
    revenue = []
    for movie in movie_date:
        meanlength, count = calPrePostLength(data, movie, movie_date[movie][0],movie_date[movie][1])
        meanlengths.append(meanlength)
        counts.append(count)
        revenue.append(movie_revenue[movie])
    meanlengths = np.array(meanlengths)
    counts = np.array(counts)
    revenue = np.array(revenue)

    plt.subplot(3, 3, 2)
    meanlengths = np.reshape(meanlengths, (len(meanlengths), 1))
    lr = LinearRegression()
    lr.fit(meanlengths, revenue)
    xi = np.linspace(np.min(meanlengths), np.max(meanlengths), 20)
    xi = np.reshape(xi, (len(xi), 1))
    y_pred = lr.predict(xi)
    plt.scatter(meanlengths, revenue)
    plt.plot(xi, y_pred,color='r')
    plt.grid()
    plt.title("Revenue vs. post pre mean tweet length")
    plt.xlabel('post pre mean tweet length')
    plt.ylabel('Revenue')
    writeCsv("Revenue vs. post pre mean tweet length" + ".csv", meanlengths, revenue)


    plt.subplot(3, 3, 5)
    lr = LinearRegression()
    counts = np.reshape(counts, (len(counts), 1))
    lr.fit(counts, revenue)
    xi = np.linspace(np.min(counts), np.max(counts), 20)
    xi = np.reshape(xi, (len(xi), 1))
    y_pred = lr.predict(xi)
    plt.scatter(counts, revenue)
    plt.plot(xi, y_pred,color='r')
    plt.grid()
    plt.title("Revenue vs. post pre tweet count")
    plt.xlabel('post pre tweet count')
    plt.ylabel('Revenue')
    writeCsv("Revenue vs. post pre tweet count" + ".csv", counts, revenue)

    # plt.show()

    # post
    meanlengths = []
    counts = []
    revenue = []
    for movie in movie_date:
        meanlength, count = calPostLength(data, movie,movie_date[movie][1])
        meanlengths.append(meanlength)
        counts.append(count)
        revenue.append(movie_revenue[movie])
    meanlengths = np.array(meanlengths)
    counts = np.array(counts)
    revenue = np.array(revenue)

    plt.subplot(3, 3, 3)
    lr = LinearRegression()
    meanlengths = np.reshape(meanlengths, (len(meanlengths), 1))
    lr.fit(meanlengths, revenue)
    xi = np.linspace(np.min(meanlengths), np.max(meanlengths), 20)
    xi = np.reshape(xi, (len(xi), 1))
    y_pred = lr.predict(xi)
    plt.scatter(meanlengths, revenue)
    plt.plot(xi, y_pred,color='r')
    plt.grid()
    plt.title("Revenue vs. post mean tweet length")
    plt.xlabel('post mean tweet length')
    plt.ylabel('Revenue')
    writeCsv("Revenue vs. post mean tweet length" + ".csv", meanlengths, revenue)


    plt.subplot(3, 3, 6)
    lr = LinearRegression()
    counts = np.reshape(counts, (len(counts), 1))
    lr.fit(counts, revenue)
    xi = np.linspace(np.min(counts), np.max(counts), 20)
    xi = np.reshape(xi, (len(xi), 1))
    y_pred = lr.predict(xi)
    plt.scatter(counts, revenue)
    plt.plot(xi, y_pred,color='r')
    plt.grid()
    plt.title("Revenue vs. post tweet count")
    plt.xlabel('post tweet count')
    plt.ylabel('Revenue')
    writeCsv("Revenue vs. post tweet count" + ".csv", counts, revenue)


    # total
    meanlengths = []
    counts = []
    revenue = []
    for movie in movie_date:
        meanlength, count = calAllLength(data, movie)
        meanlengths.append(meanlength)
        counts.append(count)
        revenue.append(movie_revenue[movie])
    meanlengths = np.array(meanlengths)
    counts = np.array(counts)
    revenue = np.array(revenue)

    plt.subplot(3, 3, 7)
    lr = LinearRegression()
    meanlengths = np.reshape(meanlengths, (len(meanlengths), 1))
    lr.fit(meanlengths, revenue)
    xi = np.linspace(np.min(meanlengths), np.max(meanlengths), 20)
    xi = np.reshape(xi, (len(xi), 1))
    y_pred = lr.predict(xi)
    plt.scatter(meanlengths, revenue)
    plt.plot(xi, y_pred, color='r')
    plt.grid()
    plt.title("Revenue vs. total tweet length")
    plt.xlabel("total tweet length")
    plt.ylabel('Revenue')
    writeCsv("Revenue vs. total tweet length" + ".csv", meanlengths, revenue)


    plt.subplot(3, 3, 8)
    lr = LinearRegression()
    counts = np.reshape(counts, (len(counts), 1))
    lr.fit(counts, revenue)
    xi = np.linspace(np.min(counts), np.max(counts), 20)
    xi = np.reshape(xi, (len(xi), 1))
    y_pred = lr.predict(xi)
    plt.scatter(counts, revenue)
    plt.plot(xi, y_pred, color='r')
    plt.grid()
    plt.title("Revenue vs. total tweet count")
    plt.xlabel("total tweet count")
    plt.ylabel('Revenue')
    writeCsv("Revenue vs. total tweet count" + ".csv", counts, revenue)

    plt.savefig('pro1.jpg', bbox_inches='tight')
    plt.show()





if __name__=="__main__":
    path="data.csv"
    data=readCsv(path)
    print(data.shape)
    # print(data.shape)
    print(data[data[:,0]<1466638597].shape)
    # print(movie_date['BLACK PANTHER'])

    # calPre(data,'GREEN BOOK')
    # calPreLength(data,'GREEN BOOK',predate='2017-11-3')

    drawLength(data)


