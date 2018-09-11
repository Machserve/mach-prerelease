#!/usr/bin/python

import os
from dotenv import load_dotenv
from mach_prerelease.main import main
os.chmod("mach_prerelease/main.py", 0b111101101) # rwxr-xr-x make it executable 
load_dotenv()
main()
