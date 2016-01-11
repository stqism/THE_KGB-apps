#the number is the value of %base% converted to %unit%
#naturally the base itself will always equal 1, larger values will be less than 0

#IMPORTANT, EACH SUB ARRAY MUST BE ORDERED LONGEST TO SHORTEST
#Failure to do so may result in mi (miles) being interpreted as m (meters)
#this is because of use of startswith for matchBoth
units = [

#lengths | use meter as base
[
#common names
["centimeter",100, "centimeters"],
["millimeter",1000, "milimeters"],
["nanometer",1e+9, "nanometers"],
["kilo",0.0001, "kilometers"],
["yard",1.09361, "yards"],
["foot",3.28084, "feet"],
["feet",3.28084, "feet"],

["km",0.0001, "kilometers"],
["cm",100, "centimeters"],
["mm",1000, "milimeters"],
["nm",1e+9, "nanometers"],
["mi",0.000621371, "miles"],
["yr",1.09361, "yards"],
["ft",3.28084, "feet"],
["in",39.3701, "inches"],
["na",0.000539957, "naughts"],
["m",1,"meters"]

],

#data | use byte as base
[
#common names
["byte",1,"bytes"],
["kilobyte",0.001,"kilobytes"],
["megabyte",1e-6,"Megabytes"],
["mb",1e-6,"Megabytes"],
["gb",1e-9,"Gigabytes"],
["tb",1e-12,"Terabytes"],
["pb",1e-15,"Petabytes"],
["kb",0.001,"kilobytes"],


["kib",0.0078125,"kibibits"],
["Mib",7.6294e-6,"Mebibits"],
["Gib",7.4506e-9,"Gibibits"],
["Tib",7.276e-12,"Tebibits"],
["Pib",7.1054e-15,"Pebibits"],
["kiB",0.000976563,"kibibytes"],
["MiB",9.5367e-7,"Mebibytes"],
["GiB",9.3131e-10,"Gibibytes"],
["TiB",9.0949e-13,"Tebibytes"],
["PiB",8.8818e-16,"Pebibytes"],
["kb",0.008,"kilobits"],
["Mb",8e-6,"Megabits"],
["Gb",8e-9,"Gigabits"],
["Tb",8e-12,"Terabits"],
["Pb",8e-15,"Petabits"],
["kB",0.001,"kilobytes"],
["MB",1e-6,"Megabytes"],
["GB",1e-9,"Gigabytes"],
["TB",1e-12,"Terabytes"],
["PB",1e-15,"Petabytes"],
["b",8,"bits"],
["B",1,"bytes"]
],

#mass | use kg as base
[
#common names
["millegram",1e+6,"milligrams"],
["kilo",1,"kilograms"],
["pound",2.20462,"pounds"],
["ou",35.274,"ounces"],

["kg",1,"kilograms"],
["to",0.001,"tonnes"],
["st",0.157473,"stone"],
["lb",2.20462,"pounds"],
["oz",35.274,"ounces"],
["g",1000,"grams"]
]

]


def declare():
	val = {"convert":"privmsg"}
	for i in range (len(units)):
		for j in range (len(units[i])):
			val[ units[i][j][0] ] = "privmsg"
	return val

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
	#	^convert 5 in to cm
	#	^kg 5 to lb
	#msg is  value to unit
	values = msg.split(' ')

	if channel.startswith('#'):
		if values[1] == "help":

			self.msg(channel, "^convert [value] [unit1] to [unit2]'. Use ^convert units to be messaged the units accepted.")
			return

		elif values[1] == "units":
			s = ""
			for i in range (len(units)):
				for j in range (len(units[i])):
					s = s + " " + units[i][j][2] + " (" + units[i][j][0] + "),"
			self.msg(user.split('!')[0], 'You can use the following: ' + s.strip(','))
			return

		#deal with getting the value
		try:
			value = float(values[1])
		except ValueError:
			self.msg(channel, 'First parameter must be a number')
			return;

		#deal with unit1
		unit1 = command.strip('^')

		if unit1 == "convert":	#must be using ^convert
			unit1 = values[2]

		#deal with unit2
		unit2 = values[len(values)-1]	#last index must be the second unit

		condex = matchBoth(unit1, unit2)

		if condex != "":	#must be supported units
			value = float(value)

			converted = convert(condex,value)

			converted = round(converted, 3)
			self.msg(channel, "%s %s is %s in %s." % (value, condex[0][2], converted, condex[1][2]))
		else:
			self.msg(channel, 'Conversion format must match "^convert [value] [unit1] in [unit2]. ^convert help for information on available values')
			return

def matchBoth(u1, u2):
	for i in range (len(units)):
		found1 = ""
		found2 = ""

		for j in range (len(units[i])):
			if u1.startswith(units[i][j][0]):
				found1 = units[i][j]
			if u2.startswith(units[i][j][0]):
				found2 = units[i][j]

			if (found1 != "")&(found2 != ""):
				return [found1,found2]

	return ""

def convert(condex, v):
	return (v / condex[0][1]) * condex[1][1]
