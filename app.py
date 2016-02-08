from flask import Flask, jsonify, request, render_template
import os
import networkx
#os.chdir("C:\\Users\\Wenxin\\Documents\\School\\University\\Utek\\pyshp-1.2.3")
os.chdir(r"C:\Users\Wenxin\Documents\School\University\Utek\pyshp-1.2.3")

import shapefile

ap_sf = shapefile.Reader(r"C:\Users\Wenxin\Documents\School\University\Utek\address_points\ADDRESS_POINT_WGS84.dbf")

ap_shapes = ap_sf.shapes()

cl_sf = shapefile.Reader(r"C:\Users\Wenxin\Documents\School\University\Utek\centreline\CENTRELINE_WGS84.dbf")

cl_shapes = cl_sf.shapes()

clint_sf = shapefile.Reader(r"C:\Users\Wenxin\Documents\School\University\Utek\centreline_intersection\CENTRELINE_INTERSECTION_WGS84.dbf")

clint_shapes = clint_sf.shapes()

# print(ap_sf.fields , "\n")
# 
# print(ap_sf.record(1000) , "\n")
# 
# print(ap_sf.shape(1000).points , "\n")
# 
# print(cl_sf.fields , "\n")
# 
# print(cl_sf.record(1000), "\n")
# print(cl_sf.record(1001), "\n")

# list = [10093,10231,10973, 10974, 11032, 11374, 12791, 40944, 41019, 41020, 42114, 50865, 51066, 53742]
# 
# 
# for i in range(14):
#     print(cl_sf.record(list[i]), "\n")
# 
# print(clint_sf.record(32151))


# for i in range(len(cl_shapes)):
#     if cl_sf.record(i)[2] == "St George St":
#         print("Index", i)

ap_records = ap_sf.records()
cl_records = cl_sf.records()
clint_records = clint_sf.records()


# for i in range (len(clint_records)):
#     #if clint_sf.record(i)[2] == "Bloor St W / St George St" or clint_sf.record(i)[2] == "St George St / Bloor St W":
#     if clint_records[i][0] == 13463981:
#         print(clint_records[i])
#     if clint_records[i][0] == 13463893:
#         print(clint_records[i])

# for i in range(len(ap_shapes)):
#     rec = ap_sf.record(i)
#     if rec[4] == "St George St" and rec[5] == 135:
#         print(i)

# print(ap_sf.record(57721))
# print(ap_sf.record(57721)[17:19])

# print(ap_sf.record(132490))
# print(ap_sf.record(132490)[17:19])
        
# print(len(ap_shapes))
# print(len(cl_shapes))
# print(len(clint_shapes))
# 
# print(clint_sf.fields , "\n")
# 
# print(clint_sf.record(1000) , "\n")
# 
# 
# print(clint_sf.shape(1000).points , "\n")

G = networkx.Graph()

# for i in range(len(clint_shapes)):
    
for i in range(len(clint_records)):

    G.add_node(clint_records[i][0], lon = clint_records[i][15], lat = clint_records[i][16]) #LONGITUDE THEN LATITUDE
    
print(G.node[13468164])

from math import sin, asin, cos, sqrt, atan2, radians
def haversine_d(lat1,lat2,lon1,lon2):

    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
        
    dlon = lon2-lon1
    dlat = lat2-lat1
    a = (sin(dlat/2))**2 + cos(lat1)*cos(lat2)*(sin(dlon)/2)**2
    b = 2 * asin(sqrt(a))
    d = 6371 * b
    #d = 2*(6371)*asin(sqrt((sin(dlat/2))**2)+ cos(lat1)*cos(lat2)*(sin((dlon)/2)))
    return (d)

print(haversine_d( 43.659726,43.666035, -79.397320,-79.398792))

l = [201200, 201201, 201300, 201301, 201400, 201401, 201500, 201600, 201601, 201700, 201800]

for i in range(len(cl_records)):
    
    info = cl_records[i]
    
    if info[13] in l:
        streetID = info[0]
        fromID = info[11]
        toID = info[12]
        
        dist = haversine_d(G.node[fromID]["lat"], G.node[toID]["lat"], G.node[fromID]["lon"], G.node[toID]["lon"])
    
        G.add_edge(fromID, toID, d = dist)

def shortestDistance(start, end):

    distances = {}
    previous = {}
    
    unvisited = []

    for i in range(len(clint_records)):
        
        distances[clint_records[i][0]] = 10000000000000000
    
        previous[clint_records[i][0]] = -1
        
        unvisited.append(clint_records[i][0])
    
    distances[start] = 0
    
    while len(unvisited) > 0:
        
        lowest = distances[unvisited[0]]
        current_lowest = unvisited[0]
        ind = 0
        for i in range(1,len(unvisited)):
            if distances[unvisited[i]] < lowest:
                 lowest = distances[unvisited[i]]
                 current_lowest = unvisited[i]
                 ind = i
        
        if current_lowest == end:
            u = end
            d = 0
            while True:
                try:
                    g = G.node[u]
                    d += haversine_d(G.node[u]["lat"], G.node[previous[u]]["lat"], G.node[u]["lon"], G.node[previous[u]]["lon"])
                    u = previous[u]
                except KeyError:
                    return d
            break;
        del unvisited[ind]
        
        for e in G.neighbors(current_lowest):
            testlength = distances[current_lowest] + haversine_d(G.node[current_lowest]["lat"], G.node[e]["lat"], G.node[current_lowest]["lon"], G.node[e]["lon"])
            
            if testlength < distances[e]:
                distances[e] = testlength
                previous[e] = current_lowest
                
    return distance, previous
        
def StrPath(start, dest):
    
    start = start.lower()
    dest = dest.lower()
    
    begin = start.split(" ")
    end = dest.split(" ")
    
    num = int(begin[0])
    endnum = int(end[0])
    
    srdname = ""
    erdname = ""
    
    for i in range(1, len(begin)-1):
        srdname += begin[i].capitalize() + " "
    
    srdname += begin[len(begin)-1].capitalize()
    
    for i in range(1, len(end)-1):
        erdname += end[i].capitalize() + " "
    
    erdname += end[len(end)-1].capitalize()
    
    startfound = False
    endfound = False
    
    for i in range(len(ap_records)):
        rec = ap_records[i]
        if (rec[4] == srdname and rec[5] == num):
            startcl = rec[1]
            startlon = rec[17]
            startlat = rec[18]
            startfound = True
        elif (rec[4] == erdname and rec[5] == endnum):
            endcl = rec[1]
            endlon = rec[17]
            endlat = rec[18]
            endfound = True
            
        if startfound and endfound:
            break;
    
    if startfound == False:
        return "Start Address Could Not Be Found"
    
    if endfound == False:
        return "End Address Could Not Be Found"
        
    startfound = False
    endfound = False
        
    for i in range(len(cl_records)):
        rec = cl_records[i]
        if rec[0] == startcl:
            startnode1 = rec[11]
            startnode2 = rec[12]
            startfound = True
        elif rec[0] == endcl:
            endnode1 = rec[11]
            endnode2 = rec[12]
            endfound = True
        if startfound and endfound:
            break;
            
    found1 = False
    found2 = False
    found3 = False
    found4 = False
    
    for i in range(len(clint_records)):
        rec = clint_records[i]
        if rec[0] == startnode1:
            startnode1cords = (rec[15], rec[16]) #lon, lat
            found1 = True
        elif rec[0] == startnode2:
            startnode2cords = (rec[15], rec[16])
            found2 = True
        elif rec[0] == endnode1:
            endnode1cords = (rec[15], rec[16])
            found3 = True
        elif rec[0] == endnode2:
            endnode2cords = (rec[15], rec[16])
            found4 = True
            
        if found1 and found2 and found3 and found4:
            break;
        
    #check shortest distance between nodes, 4 checks
    
    l = [(startnode1cords,endnode1cords), (startnode1cords,endnode2cords) , (startnode2cords,endnode1cords) , (startnode2cords, endnode2cords)]
    
    start = startnode1
    end = endnode1
    cur_distance = haversine_d(l[0][0][1], l[0][1][1], l[0][0][0], l[0][1][0])
    
    for i in range(1,4):
        a,b = l[i]
        d = haversine_d(l[i][0][1],l[i][1][1], l[i][0][0], l[i][1][0])
        if d < cur_distance:
            num = i
            cur_distance = d
        
    if i == 2:
        start = startnode1
        end = endnode2
        
    elif i == 3:
        start = startnode2
        end = endnode1
    
    elif i == 4:
        start = startnode2
        end = endnode2
        
    startlat = G.node[start]["lat"]
    startlon = G.node[start]["lon"]
    endlat = G.node[end]["lat"]
    endlon = G.node[end]["lon"]
    
    totald = (startlat - endlat)**2 + (startlon - endlon)**2
    
    distances = {}
    previous = {}
    
    unvisited = []

    for i in range(len(clint_records)):
        
        distances[clint_records[i][0]] = 10000000000000000
    
        previous[clint_records[i][0]] = -1
        
        unvisited.append(clint_records[i][0])
    
    distances[start] = 0
    
    cur_perc = 100
    
    while len(unvisited) > 0:
        
        lowest = distances[unvisited[0]]
        current_lowest = unvisited[0]
        ind = 0
        for i in range(1,len(unvisited)):
            if distances[unvisited[i]] < lowest:
                 lowest = distances[unvisited[i]]
                 current_lowest = unvisited[i]
                 ind = i
                         
        if current_lowest == end:
            u = end
            d = 0
            while True:
                try:
                    g = G.node[u]
                    d += haversine_d(g["lat"], G.node[previous[u]]["lat"], g["lon"], G.node[previous[u]]["lon"])
                    u = previous[u]
                except KeyError:
                    return d
            break;
        del unvisited[ind]
        
        for e in G.neighbors(current_lowest):
            testlength = distances[current_lowest] + haversine_d(G.node[current_lowest]["lat"], G.node[e]["lat"], G.node[current_lowest]["lon"], G.node[e]["lon"])
            
            if testlength < distances[e]:
                distances[e] = testlength
                previous[e] = current_lowest
            
            dis = int(( ((G.node[current_lowest]["lat"]-endlat)**2 + (G.node[current_lowest]["lon"] - endlon)**2)/totald)*100)
        
            if dis < cur_perc:
                cur_perc = dis
                print(100-cur_perc, "% done")
                
    return distance, previous
        
app = Flask("ShortestDistanceFinder")
#app = Flask(static_folder=r"C:\Users\Wenxin\Documents\School\University\Utek\FrontEnd\flaskr",import_name="ShortestDistanceFinder" )

@app.route('/')
#def main():
    
    #return render_template("index.html")
def root():
    #return open(r"index.html").read()
    return open(r"C:\Users\Wenxin\Documents\School\University\Utek\FrontEnd\FlaskApp\index.html").read()
    
@app.route('/add')
def add():
    print("getting args")
    n1 = str(request.args.get('a1')) # GET request variables
    print(n1)
    n2 = str(request.args.get('a2'))
    print(n2)
    d = StrPath(n1, n2)
    print(d)
    return jsonify({'shortestdistance':d, 'start':n1, 'end':n2})
    
if __name__ == '__main__':
     app.run(host="127.0.0.1", port=5001)

