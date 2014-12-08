#!/usr/bin/env python

import sys
import urllib2
import re
import json
import os
import time
import shutil
import fnmatch

# Be sure to call this file with a Google Spreadsheet key as the first argument
key = sys.argv[1]

# first, back up the old files
old_files = fnmatch.filter(os.listdir('.'), key +'*')

if (len(old_files)):
    try:
        old_file_dirname = 'bak_'+ key +'_'+ time.strftime("%Y%m%d_%H%M%S")
        os.mkdir(old_file_dirname)
        
        # move the files to process into a temp processing dir
        for filename in old_files:
            shutil.copyfile(filename, old_file_dirname +'/'+ filename)
    except IOError as e:
        sys.stderr.write(e)

# for legacy support
if '--old' in sys.argv:
    sq = "&sq="
else:
    sq = ""

base_json_url = "https://spreadsheets.google.com/feeds/worksheets/"+key+"/public/basic?alt=json-in-script&callback=Tabletop.singleton.loadSheets"

base_json_content = urllib2.urlopen(base_json_url).read()

sheet_ids = set(re.findall(r"/public/basic/(\w*)",base_json_content, flags=0))

for sheet_id in sheet_ids:
  sheet_url = "https://spreadsheets.google.com/feeds/list/"+key+"/"+sheet_id+"/public/values?alt=json-in-script" + sq + "&callback=Tabletop.singleton.loadSheet"
  content = urllib2.urlopen(sheet_url).read()
  with open(key+"-"+sheet_id, "w") as f:
		f.write(content)

with open(key, "w") as f:
	f.write(base_json_content)
