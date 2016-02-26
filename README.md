# WebApp
Shortest Path Finder for Downtown Toronto

Written in Python, utilizes Flask framework.
Packages used: Networkx, pyshp

###Requires City of Toronto Database Files

* Address Points: [Municipal Address Points (WGS84 - Latitude / Longitude) under "Data Download"](http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=91415f9cd70bb210VgnVCM1000003dd60f89RCRD)
* Centreline: [Toronto Centreline (WGS84 - Latitude / Longitude) under "Data Download"](http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=9acb5f9cd70bb210VgnVCM1000003dd60f89RCRD)
* Centreline Intersections: [Intersection File (WGS84) under "Data Download"](http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=e659522373c20410VgnVCM10000071d60f89RCRD)

`Extract Directly into Repo Directory. E.g. the Address Point .dbf should be located at ~/WebApp/address_points/ADDRESS_POINT_WGS84.dbf`
