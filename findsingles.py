#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import with_statement, division

import os, bz2
import elementtree.ElementTree as ET
import pylab
import math

filelistdir = "/home/me/.dc++/FileLists"
outputfile = "/home/me/code/dcpputils/unmirrored.html"

def parse_dir(dir, files, seen, username, stats):
	size = 0
	for file in dir.findall("File"):
		tth = file.attrib["TTH"]
		if tth in files:
			if username != files[tth][1]:
				# doesn't count if it's one user with multiple copies of the same file
				del files[tth]
				seen[tth] = True
		elif tth not in seen:
			s = int(file.attrib['Size'])
			size += s
			files[tth] = [file.attrib["Name"], username]
			stats.append(math.log10(s))
	for d in dir.findall("Directory"):
		size += parse_dir(d, files, seen, username, stats)
	return size


files = {}
seen = {}
usernames = {}
stats = []
count = 0
size = 0
# copy them all to uncompressed
for fullname in os.listdir(filelistdir):
	name = os.path.splitext(fullname)[0]
	username = os.path.splitext(os.path.splitext(name)[0])[0]
	try:
		print "Parsing filelist:", username
		bz2file = open(os.path.join(filelistdir, fullname))
		xml = bz2.decompress(bz2file.read())
		if len(xml):
			tree = ET.fromstring(xml)
			size += parse_dir(tree, files, seen, username, stats)
		count += 1
		print "Parsed filelist:", username, "(now parsed", count, "filelists)"
	except Exception:
		print "Uh oh, %s's filelist didn't parse! Eh." % username

pylab.hist(stats, 100)
pylab.savefig('butts.png')
print "total : %s" % size
#page = """<html>
#<head><title>All the files that only one person has</title></head>
#<body><p>Total size: %s</p><table><tr><th>Name</th><th>Owner</th></tr>""" % size

#for tth in files:
#	count += 1
#	if(count / 500 == count // 500):
#		print "AT", count
#	page += '<tr><td><a href="magnet:?xt=urn;tree:tiger:%s&dn=%s">%s</a></td>' % (tth, files[tth][0], files[tth][0])
#	page += '<td>%s</td></tr>\n' % files[tth][1]
#
#with open(outputfile, 'w') as f:
#	f.write(page)

print "DONE"
