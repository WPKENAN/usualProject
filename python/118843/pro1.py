import os
import numpy as np
import pandas as pd
import os
os.environ["PROJ_LIB"] = "D:\\anaconda\pkgs\proj4-5.2.0-ha925a31_1\Library\share";



def main(data,vmax,vmin,title,label=''):



    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap
    from matplotlib.patches import Polygon
    from matplotlib.colors import rgb2hex, Normalize
    import numpy as np
    import pandas as pd
    from matplotlib.colorbar import ColorbarBase
    plt.figure(figsize=(16, 8))
    m = Basemap(
        llcrnrlon=77,
        llcrnrlat=14,
        urcrnrlon=140,
        urcrnrlat=51,
        projection='lcc',
        lat_1=33,
        lat_2=45,
        lon_0=100
    )
    m.drawcountries(linewidth=1.5)
    m.drawcoastlines()

    m.readshapefile('gadm36_CHN_shp/gadm36_CHN_1', 'states', drawbounds=True)



    provinces = m.states_info
    statenames = []
    colors = {}
    cmap = plt.cm.YlOrRd

    norm = Normalize(vmin=vmin, vmax=vmax)

    # print(len(provinces))
    for each_province in provinces:
        # print(each_province)
        province_name = each_province['NAME_1']
        p = province_name.split(' ')
        s=p[0]

        if s=='Nei':
            s='Inner Mongolia'
            statenames.append(s)
            pop = data[s]
        elif s=='Ningxia Hui':
            s="Ningxia"
            statenames.append(s)
            pop = data[s]
        elif s=="Xizang":
            statenames.append(s)
            pop = 0
        else:
            statenames.append(s)
            pop = data[s]
        colors[s] = cmap(np.sqrt((pop - vmin) / (vmax - vmin)))[:3]
    plt.figure(figsize=(100, 50))
    fig, ax = plt.subplots()

    print(np.unique((np.array(statenames))))
    for nshape, seg in enumerate(m.states):
        color = rgb2hex(colors[statenames[nshape]])
        poly = Polygon(seg, facecolor=color, edgecolor=color)
        ax.add_patch(poly)
    ax.set_title(title,fontsize=10)

    # %% ---------  Plot bounding boxes for Alaska and Hawaii insets  --------------
    light_gray = [0.8] * 3  # define light gray color RGB
    x1, y1 = m([-190, -183, -180, -180, -175, -171, -171], [29, 29, 26, 26, 26, 22, 20])
    x2, y2 = m([-180, -180, -177], [26, 23, 20])  # these numbers are fine-tuned manually
    m.plot(x1, y1, color=light_gray, linewidth=0.8)  # do not change them drastically
    m.plot(x2, y2, color=light_gray, linewidth=0.8)

    # %% ---------   Show color bar  ---------------------------------------
    ax_c = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    cb = ColorbarBase(ax_c, cmap=cmap, norm=norm, orientation='vertical',label=label)
    # plt.savefig("{}.jpg".format(title),bbox_inches = 'tight')
    plt.savefig("{}.jpg".format(title))
    # plt.show()
if __name__=="__main__":

    #waste
    df = pd.read_excel("./data/Total waste water releaseAnnualbyProvince- 20 yrs(1).xlsx", header=3)
    waste = df.values[:-3, [0, 2]]
    data={}
    for city,num in waste:
        print(city,num)
        data[city]=num
    main(data,max(waste[:,1]),min(waste[:,1]),title='China city water pollution degree distribution map',label='Waste wate content (ton)')

    #income
    df = pd.read_excel("./data/人均国民收入per capita national income.xlsx", header=3)
    poplulation=df.values[:-1, [0, 2]]
    data = {}
    for city, num in poplulation:
        print(city, num)
        data[city] = num
    main(data, max(poplulation[:, 1]), min(poplulation[:, 1]), title='China per capita national income distribution map',label='yuan')