from time import gmtime, strftime
from shutil import copyfile
import getpass
import re
from math import sqrt
from decimal import *

file = open("City_of_Waterloo_trails.kml","r")
trails = {}

cookies = open("/Users/"+getpass.getuser()+"/Library/Cookies/Cookies.binarycookies","r")
print "Username: " + getpass.getuser()
cookie_file = cookies.read()
regex = r"enghack[a-z]+=\d+"
regex_coords = r"enghackposition=-\d+.\d+X\d+.\d+"
matches_coords = re.findall(regex_coords,cookie_file)
matches = re.findall(regex,cookie_file)

enghack = []
for match in matches:
	enghack.append(match.split("="))

for match in matches_coords:
	enghack.append(match.split("="))

print matches
print matches_coords

surfaces = ["No Preference", "Asphalt", "Stonedust", "Mulch", "Concrete", "Bridge", "Varies", "Geotime"]

bus_routes = ["No Preference","Yes","No"]

winter_options = ["No Preference","Yes","No"]
position = []

surface = surfaces[int(enghack[0][1])]
goal = float(enghack[1][1])
bus_route = bus_routes[int(enghack[2][1])]
winter = winter_options[int(enghack[3][1])]
position = enghack[4][1].split("X")

for i in range(19):
	file.readline()

#objectID starts at 2959
#objectID = 2959
for line in file:
	if "OBJECTID" in line:
		s = line.find(">")
		e = line.find("<",s+1)
		objectID = line[s+1:e:]
		#print(objectID)
		info = {}
		for j in range(9):
			nextline = next(file)

			start = nextline.find("\"")
			end = nextline.find("\"",start+1)

			start2 = nextline.find(">")
			end2 = nextline.find("<",start2+1)

			info[nextline[start+1:end:]] = nextline[start2+1:end2:]

			#print nextline[start2+1:end2:]
		next(file)	#get rid of useless line
		nextline2 = next(file)
		if "LineString" in nextline2:
			start = nextline2.find(">",23)
			end = nextline2.find("<",start+1)
			line = nextline2[start+1:end:]	#need to parse this into coords
			list_of_coords = line.split(" ")
			list_of_nums = []
			for each in list_of_coords:
				coords_strings = each.split(",")
				list_of_nums.append(coords_strings)
			#print(list_of_nums)
			info["coordinates"] = list_of_nums
			
		#end for loop
		trails[objectID] = info
		#print info

path = []
def find_closest(cx, cy, surface):
	minimum = 9876543.067
	chosen_path = None
	s_point = [0,0]
	length = 0
	for key in trails:
		if key not in path:
			if surface == trails[key]["SURFACE"] or surface == "":
				list_coord = trails[key]["coordinates"]

				firstx = list_coord[0][0]
				firsty = list_coord[0][1]
				lastx = list_coord[-1][0]
				lasty = list_coord[-1][1]

				#print firstx, firsty, lastx, lasty

				if (Decimal(sqrt(Decimal(Decimal(firstx)-Decimal(cx))**2 + Decimal(Decimal(firsty)-Decimal(cy))**2)) < Decimal(minimum)) and Decimal(firstx) - Decimal(cx) != 0 and Decimal(lastx) - Decimal(cx) != 0:
					minimum = Decimal(sqrt(Decimal(Decimal(firstx)-Decimal(cx))**2 + Decimal(Decimal(firsty)-Decimal(cy))**2))
					chosen_path = key
					s_point = [firstx, firsty]
					length = trails[key]["LENGTH_M"]

				if (Decimal(sqrt(Decimal(Decimal(lastx)-Decimal(cx))**2 + Decimal(Decimal(lasty)-Decimal(cy))**2)) < Decimal(minimum)) and Decimal(firstx) - Decimal(cx) != 0 and Decimal(lastx) -Decimal(cx) != 0:
					minimum = Decimal(sqrt(Decimal(Decimal(lastx)-Decimal(cx))**2 + Decimal(Decimal(lasty)-Decimal(cy))**2))
					chosen_path = key
					s_point = [lastx, lasty]
					length = trails[key]["LENGTH_M"]

	return [chosen_path, s_point, length]

# print (find_closest(-80.5441129, 43.4705486, "Asphalt"))
total_distance = 0.0
pos = position
print pos

while total_distance < goal - 100:
	new_thing = find_closest(Decimal(pos[0]),Decimal(pos[1]),surface)
	path.append(new_thing[0])
	total_distance += float(new_thing[2])
	pos = new_thing[1]

print path

# total_distance = 0.0
# first = find_closest(-80.5441129,43.4705486, total_distance, "Asphalt")
# total_distance += float(first[2])
# print first
# second = find_closest(first[1][0], first[1][1], total_distance, "Asphalt")
# total_distance += float(second[2])
# print second

def change_html(file_name):
	html_file = open("map.html","r+")
	html_file_content = html_file.read()
	html_regex = r'data_\d+_\d+_\d+_\d+_\d+_\d+.kml'

	with open("map.html", "rt") as fin:
	    with open("temp.html", "wt") as fout:
	        for line in fin:
	            fout.write (line.replace((re.findall(html_regex, html_file_content))[0], file_name))

	copyfile("temp.html", "map.html")

	# print html_file_content
	# print "Original file name: " + str(re.findall(html_regex,html_file_content))
	# html_file.write(html_file_content)
	# html_file.close()

def write_kml(keys):
	new_file_name = "data_"+strftime("%Y_%m_%d_%H_%M_%S", gmtime())+".kml"
	write_file = open(new_file_name,"w")
	#read_file = open("City_of_Waterloo_Trails.kml","r")
	global trails
	actual_begin = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
	actual_begin += "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n"
	actual_begin += "<Document id=\"root_doc\">\n"
	actual_begin += "<Schema name=\"OGRGeoJSON\" id=\"OGRGeoJSON\">\n"
	actual_begin += "<SimpleField name=\"OBJECTID\" type=\"int\"></SimpleField>\n"
	actual_begin += "<SimpleField name=\"ASSET_ID\" type=\"int\"></SimpleField>\n"
	actual_begin += "<SimpleField name=\"OWNER\" type=\"string\"></SimpleField>\n"
	actual_begin += "<SimpleField name=\"STATUS\" type=\"string\"></SimpleField>\n"
	actual_begin += "<SimpleField name=\"PATH_TYPE\" type=\"string\"></SimpleField>\n"
	actual_begin += "<SimpleField name=\"SURFACE\" type=\"string\"></SimpleField>\n"
	actual_begin += "<SimpleField name=\"BLVD_TYPE\" type=\"string\"></SimpleField>\n"
	actual_begin += "<SimpleField name=\"BUS_ROUTE\" type=\"string\"></SimpleField>\n"
	actual_begin += "<SimpleField name=\"CLEARED_BY\" type=\"string\"></SimpleField>\n"
	actual_begin += "<SimpleField name=\"LENGTH_M\" type=\"float\"></SimpleField>\n"
	actual_begin += "</Schema>\n"
	actual_begin += "<Folder><name>OGRGeoJSON</name>\n"

	actual_end = "</Folder>\n</Document></kml>"

	begin = "<Placemark>\n<Style><LineStyle><color>ff0000ff</color></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style>\n<ExtendedData><SchemaData schemaUrl=\"#OGRGeoJSON\">"
	before_coords = "</SchemaData></ExtendedData>\n<LineString><coordinates>"
	end = "</Placemark>"
	
	to_be_written = ""
	to_be_written += actual_begin
	for key in keys:
		to_be_written += begin
		to_be_written += "<SimpleData name=\"OBJECTID\">" + key + "</SimpleData>\n"
		to_be_written += "<SimpleData name=\"ASSET_ID\">" + trails[key]["ASSET_ID"] + "</SimpleData>\n"
		to_be_written += "<SimpleData name=\"OWNER\">" + trails[key]["OWNER"] + "</SimpleData>\n"
		to_be_written += "<SimpleData name=\"STATUS\">" + trails[key]["STATUS"] + "</SimpleData>\n"
		to_be_written += "<SimpleData name=\"PATH_TYPE\">" + trails[key]["PATH_TYPE"] + "</SimpleData>\n"
		to_be_written += "<SimpleData name=\"SURFACE\">" + trails[key]["SURFACE"] + "</SimpleData>\n"
		to_be_written += "<SimpleData name=\"BLVD_TYPE\">" + trails[key]["BLVD_TYPE"] + "</SimpleData>\n"
		to_be_written += "<SimpleData name=\"BUS_ROUTE\">" + trails[key]["BUS_ROUTE"] + "</SimpleData>\n"
		to_be_written += "<SimpleData name=\"CLEARED_BY\">" + trails[key]["CLEARED_BY"] + "</SimpleData>\n"
		to_be_written += "<SimpleData name=\"LENGTH_M\">" + trails[key]["LENGTH_M"] + "</SimpleData>\n"
		to_be_written += before_coords
		for coord in trails[key]["coordinates"]:
			# print coord
			if coord == trails[key]["coordinates"][-1]:
				to_be_written += coord[0] + "," + coord[1]
			else:
				to_be_written += coord[0] + "," + coord[1] + " "
		to_be_written += "</coordinates></LineString>\n" + end

	to_be_written += actual_end
	write_file.write(to_be_written)
	write_file.close()
		#print to_be_written
	print "New file saved at: " + new_file_name
	change_html(new_file_name)

write_kml(path)


#READING C OOKIES
'''
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
#Create a CookieJar object to hold the cookies
cj = cookielib.CookieJar()
#Create an opener to open pages using the http protocol and to process  cookies.
opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())

#create a request object to be used to get the page.
req = Request("http://www.eng.uwaterloo.ca/")
f = opener.open(req)

#see the first few lines of the page
html = f.read()
print html[:50]

#Check out the cookies
print "the cookies are: "
for cookie in cj:
    print cookie

import os

# Hello world python program
print "Content-Type: text/html;charset=utf-8";


handler = {}
if 'HTTP_COOKIE' in os.environ:
    cookies = os.environ['HTTP_COOKIE']
    cookies = cookies.split('; ')

    for cookie in cookies:
        cookie = cookie.split('=')
        handler[cookie[0]] = cookie[1]

for k in handler:
    print k + " = " + handler[k] + "<br>"
'''