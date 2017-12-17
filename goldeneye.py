import os
import shutil
import sys
import json
import datetime
import time
import urllib2
from HTMLParser import HTMLParser
from random import randint

version = 0.5

filename = 'goldeneye_data.json'
levels = ['Dam', 'Facility', 'Runway', 'Surface 1', 'Bunker 1', 'Silo', 'Frigate', 'Surface 2', 'Bunker 2', 'Statue', 'Archives', 'Streets', 'Depot', 'Train', 'Jungle', 'Control', 'Caverns', 'Cradle', 'Aztec', 'Egypt']
difficulties = ['Agent', 'Secret Agent', '00 Agent']
data = {}
temp = []

def writeOBS(string):
	with open('obs.txt', 'w') as outfile:
		outfile.write(string)

def updatetxt(level, diff, pr, attempts, timespent, completions):
	# This is whats written to obs.txt, feel free to change it. \n indicates a new line
	string = level + " (" + diff + ")\nPR: " + pr + "\nTime Spent: " + timespent + "\nAttempt #" + attempts 
	writeOBS(string)

def isTimeFormat(input): # Used on the HTML data from the-elite to see if what is being read is a time or not
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False

def save(filename, data): # Saves data to the json, filename specified above
	with open(filename, 'w') as outfile:
		json.dump(data, outfile, indent=4, sort_keys=True)
	print '*** Saved! ***'
	writeOBS("goldeneye-ils\nversion:" + str(version) + "\n(Not Active)")

def importFromTheElite(username):
	print 'Getting times from the-elite...'
	url = 'http://rankings.the-elite.net/~' + username + '/goldeneye'
	response = urllib2.urlopen(url)
	html = response.read()
	parser = TagParser()
	parser.feed(html) # Send the HTML data to the TagParser below
	i = 0
	print ''
	for level in levels:
		levelTimes = []
		for difficulty in difficulties:
			print level + ' (' + difficulty + '): ' + temp[i]
			levelTimes.append(temp[i]) 
			# Coincidentally, the-elite and my structure is the same, i.e. levelA levelSA level00A level2A ... makes it easy
			i += 1
		data[level] = {'Agent': {'time': levelTimes[0], 'attempts': 0, 'completions': 0, 'lastplayed': 0, 'timespent': 0}, 
					'Secret Agent': {'time': levelTimes[1], 'attempts': 0, 'completions': 0, 'lastplayed': 0, 'timespent': 0},
					'00 Agent': {'time': levelTimes[2], 'attempts': 0, 'completions': 0, 'lastplayed': 0, 'timespent': 0}}

class TagParser(HTMLParser): # Parses HTML data from the-elite
	def handle_starttag(self, tag, attrs):
		self.tag = tag
	def handle_data(self, data):
		text = str(data[:5])
		if isTimeFormat(text): # If it is a time
			temp.append(text) # Add the time to a temp list
			
def percentage(part, whole):
	try:
  		return str(format(100 * float(part)/float(whole), '.2f')) + "%"
  	except:
  		return "0.00%"

def printDots():
	print "RUNNING",
	i = 0
	while i <= randint(1,50):
		print("."),
		i += 1
		

writeOBS("goldeneye-ils\nversion: " + str(version) + "\n(Not Active)")	

if not os.path.isfile(filename): # Data not found, generate new
	print 'Data not found. Creating new.'

	print 'Import your times from the-elite, or input manually?'
	print ''
	option = raw_input("(import / manual): ")

	if option.lower() == "manual":
		print 'Enter your PRs. Press Enter to skip a time.'
		print ''
		i = 0
		for level in levels:
			levelTimes = []
			for difficulty in difficulties:
				time = raw_input('PR for ' + level + ' (' + difficulty + '): ')
				if not time:
					time = '0:00'
				levelTimes.append(time)
			data[level] = {'Agent': {'time': levelTimes[0], 'attempts': 0, 'completions': 0, 'lastplayed': 0, 'timespent': 0}, 
							'Secret Agent': {'time': levelTimes[1], 'attempts': 0, 'completions': 0, 'lastplayed': 0, 'timespent': 0},
							'00 Agent': {'time': levelTimes[2], 'attempts': 0, 'completions': 0, 'lastplayed': 0, 'timespent': 0}}
			print ''
	elif option.lower() == "import":
		print 'To get your username, look at the URL your times are at, for example: http://rankings.the-elite.net/~DJS/goldeneye'
		print ''
		print "Your username is the part after the ~ and before the /. In the example above, it would be DJS"
		print ''
		username = raw_input("the-elite username: ")
		importFromTheElite(username)
	else:
		print 'Not a valid option'
		sys.exit(1)

	save(filename, data)

print ''
print 'goldeneye-ils - version ' + str(version) + ''
print ''
print 'Okay, lets play some Goldeneye!'
print ''

data = {}
with open(filename) as data_file: 
	data = json.load(data_file) # Read in data, even if we just saved it, re-read it from file to ensure consistency

levelSet = False
diffSet = False

while True:
	writeOBS("goldeneye-ils\nversion: " + str(version) + "\n(Not Active)")	
	while levelSet == False:
		level = raw_input("Level: ").title()
		if level in data:
			levelSet = True
		elif level.lower() == "q":
			sys.exit(1)
		else:
			print 'Level doesnt exist'
	while diffSet == False:
		diff = raw_input("Difficulty (A, SA, 00A): ").upper()
		if diff == "A":
			diff = "Agent"
			diffSet = True
		elif diff == "SA":
			diff = "Secret Agent"
			diffSet = True
		elif diff == "00A":
			diff = "00 Agent"
			diffSet = True
		elif level == "q":
			sys.exit(1)
		else:
			print 'That difficulty does not exist'

	print ''
	command = ''

	while command == '':
		#print(chr(27) + "[2J") # clears screen, doesnt work well on windows
		timeStart = datetime.datetime.now()
		niceTime = datetime.timedelta(seconds=data[level][diff]["timespent"])
		if data[level][diff]["attempts"] > 0:
			completionRate = percentage(data[level][diff]["completions"], data[level][diff]["attempts"]) # completion percentage
		else:
			completionRate = "0.000%"

		updatetxt(level, diff, data[level][diff]["time"], str(data[level][diff]["attempts"]), str(niceTime), str(data[level][diff]["completions"]))
		print level + ' (' + diff + ')'
		print 'PR: ' + data[level][diff]["time"]
		print 'Attempt #' + str(data[level][diff]["attempts"])
		print 'Time Spent: ' + str(niceTime)
		#print 'Completions: ' + str(data[level][diff]["completions"])
		print ''
		print '-- Commands --'
		print ' | ENTER = +1 attempts | PR = set new pr | L = change level/diff |'
		print ' | R = reset stats for current level/diff | Q = save & quit |'
		printDots()
		command = raw_input('Command: ').lower()

		if command == "q":
			save(filename, data)
			writeOBS("goldeneye-ils\nversion: " + str(version) + "\n(Not Active)")	
			sys.exit(1)
		elif command == "r":
			data[level][diff]["timespent"] = 0
			data[level][diff]["attempts"] = 0
			data[level][diff]["completions"] = 0
			print ''
			print '*** Time spent and attempts reset ***'
		elif command == "pr":
			pr = raw_input("What is your new PR?: ")
			data[level][diff]["time"] = pr
			save(filename, data)
		elif command == "c":
			data[level][diff]["completions"] += 1
			i = datetime.datetime.now()
			timeDiff = i - timeStart
			data[level][diff]["timespent"] += timeDiff.seconds
			data[level][diff]["attempts"] += 1
			data[level][diff]["lastplayed"] = ("%s" % i)
		elif command == "l":
			# change level
			save(filename, data)
			levelSet = False
			diffSet = False
			timeNow = 0
		else:
			# increment attempts and calc new time
			i = datetime.datetime.now()
			timeDiff = i - timeStart
			if timeDiff.seconds < 1:
				print "\n *** double tap prevented *** \n"
			else:
				data[level][diff]["timespent"] += timeDiff.seconds
				data[level][diff]["attempts"] += 1
				data[level][diff]["lastplayed"] = ("%s" % i)
