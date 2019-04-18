# from folium import plugins
import folium.plugins
import webbrowser



guiji=[];
def readCsv(path):
    lines=open(path).readlines();
    for i in range(1,len(lines)):
        lines[i]=lines[i].strip('\n').split(',')
        # print(lines[i])
        for j in range(2):
            lines[i][j]=float(lines[i][j]);

        # print(len(guiji))
        if i==1:
            guiji.append([lines[i][1], lines[i][0]]);
            continue
        if [lines[i][1],lines[i][0]]!=guiji[len(guiji)-1]:
            guiji.append([lines[i][1], lines[i][0]]);




if __name__=="__main__":
    path="1120122.csv";
    readCsv(path)
    m = folium.Map(guiji[0], zoom_start=5)
    folium.Marker(guiji[0], popup='<i>起始点</i>').add_to(m)
    folium.Marker(guiji[-1], popup='<i>终止点</i>').add_to(m)
    route = folium.PolyLine(
        guiji,
        weight=2,
        color='red',
        opacity=1
    ).add_to(m)

    # 警告图例
    attr = {'fill': 'red'}
    # 飞机图例
    aircraft = {'font-weight': 'bold', 'font-size': '10'}


    folium.plugins.PolyLineTextPath(
        route,
        # '\u25BA', # 图例样式
        '\u2708',
        repeat=True,
        offset=0,
        attributes=aircraft
    ).add_to(m)

    m.save("轨迹.html")
    webbrowser.open("轨迹.html")