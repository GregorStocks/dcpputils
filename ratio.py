#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import with_statement, division

import os, re

filedir = "/home/me/.dc++/Logs"
downloadlog = filedir + "/Downloads.log"
uploadlog = filedir + "/Uploads.log"

downloads = 0
with open(downloadlog, 'r') as f:
	for line in f.readlines():
		size = re.search(', \d+ \((\d+)\),', line)
		if size is not None and size.group(1) is not None:
			downloads += int(size.group(1))

uploads = 0
with open(uploadlog, 'r') as f:
	for line in f.readlines():
		size = re.search(', \d+ \((\d+)\),', line)
		if size is not None and size.group(1) is not None:
			uploads += int(size.group(1))
	
print '+me ratio: %.2f (Uploaded: %.2f TiB | Downloaded: %.2f GiB)' % (uploads / downloads, uploads / 1024 ** 4, downloads / 1024 ** 3)
