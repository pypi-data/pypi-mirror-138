# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 21:43:08 2022

@author: parse
"""

import sys
import requests
f = open(sys.argv[1])
url = 'https://ssd.jpl.nasa.gov/api/horizons_file.api'
r = requests.post(url, data={'format':'text'}, files={'input': f})
print(r.text)
f.close()