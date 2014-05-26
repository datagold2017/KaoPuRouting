#!/usr/bin/python

import sys
import json
import httplib
from AdRoute import *
from Tool import *
import urllib 
import urllib2

class RoutesMain:

    #Server_Address="route.nlp.nokia.com.cn"
    Server_Address="211.151.53.78"
    Debug=True

    #GEO "latitude","longitude"
    def listRoutes(self, geo1,geo2):
        conn=httplib.HTTPConnection(self.Server_Address)
        headers={'accept':'application/json'}
        alternatives= '2'
        route_mode='fastest;car;traffic:disabled;'
        uri ="/routing/7.2/calculateroute.json?routeattributes=wp,sm,lg&maneuverattributes=ac,po,tt,le,li&linkattributes=sh&legattributes=sh&jsonAttributes=41&verboseMode=5&metricSystem=metric&alternatives="
        uri =uri + alternatives + "&waypoint0=geo!"+geo1[0]+","+geo1[1]+"&waypoint1=geo!"+geo2[0]+","+geo2[1]+"&language=zh_CN&mode="
        uri =uri + route_mode + "&app_id=90oGXsXHT8IRMSt5D79X&token=JY0BReev8ax1gIrHZZoqIg"

        Tool.debugStaticMessage(self.Debug,"/routing/7.2/calculateroute.json?"+uri)
        
        uri ='http://'+self.Server_Address+uri
        req = urllib2.Request(uri)
        req.add_header('accept', 'application/json')
        
        response = urllib2.urlopen(req)
        
        r=response.getcode()
        if r != 200 :
            conn.close()
            Tool.errorLog(str(r))
            Tool.errorLog(" "+uri+"\n")
            raise Exception("Cannot get routes by HTTP RestAPI")
            
        content = json.loads(response.read())
        
        routes_txt=content["response"]["route"]

        ## parse links info
        routes=[]
        for one_route in routes_txt:
            links=[]
            shape=''
            for leg in one_route["leg"]:
            
                shape=leg['shape']
                for maneuver in leg["maneuver"]:

                    link_action=maneuver["action"]
                    if link_action == "arrive":
                        break

                    link_length=str(maneuver["length"])
                    link_id=str(maneuver["toLink"])
                    link_instruction=(maneuver["instruction"]).encode('utf-8')
                    pos=maneuver["position"]
                    links.append((link_id,link_length,link_instruction))
                
                #only one leg
            travel_time=one_route['summary']['travelTime']
            routes.append((shape,links,travel_time))
            
            Tool.debugStaticMessage(self.Debug,"\nShape is:\n "+ str(shape))
                      
        return routes
    
    #arrived_time= yyyyddmmHHMM
    def getRoutes(self,geo0,geo1,arrived_time):
        routeOption=[]
        routes_info=self.listRoutes(geo0,geo1)
        
        for route in routes_info:
            ad_route=AdRoute(route,geo0,geo1,'',arrived_time)
            ad_route.calByArrivalTime()
            routeOption.append(ad_route)
        
            
        return routeOption
    

#########################################################

        
    def testGetRoutes(self):
    
        start_geoX="39.9515592744"
        start_geoY="116.41934259"
        end_geoX="39.9992530"
        end_geoY="116.4744977"
        planned_time="201404090000"
        
        self.getRoutes([start_geoX,start_geoY],[end_geoX,end_geoY],planned_time)
    

    def testListRoutes(self):
    
        start_geoX="39.871990"
        start_geoY="116.433120"
        end_geoX="39.871680"
        end_geoY="116.439420"
        
        start_geoX="39.9515592744"
        start_geoY="116.41934259"
        end_geoX="39.9992530"
        end_geoY="116.4744977"
        
        routes=self.listRoutes([start_geoX,start_geoY],[end_geoX,end_geoY])
        
        Tool.results2Log(str(routes[0]))
        
        
###############################################################
#

def main():

    '''
    args_size=len(sys.argv)
    if args_size != 6:
        usage()
        sys.exit()
        
    start_geoX=sys.argv[1]
    start_geoY=sys.argv[2]
    end_geoX=sys.argv[3]
    end_geoY=sys.argv[4]
    planned_time=sys.argv[5]
    
    req = urllib2.Request(request_string)
    response = urllib2.urlopen(req)
    image_data = response.read()
        
    '''
    my_route=RoutesMain()
    
    #my_route.testGetRoutes()
    
    my_route.testListRoutes()
    #211.151.53.78/routing/7.2/calculateroute.json?/routing/7.2/calculateroute.json?routeattributes=wp,sm,lg&maneuverattributes=ac,po,tt,le,li&linkattributes=sh&legattributes=sh&jsonAttributes=41&verboseMode=5&metricSystem=metric&alternatives=3&waypoint0=geo!39.9515592744,116.41934259&waypoint1=geo!39.9992530,116.4744977&language=zh_CN&mode=fastest;car;traffic:disabled;&app_id=90oGXsXHT8IRMSt5D79X&token=JY0BReev8ax1gIrHZZoqIg


if __name__=='__main__':
    main()
