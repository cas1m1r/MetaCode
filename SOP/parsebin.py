from utils import *
import json
import sys
import os


linux_src = '/usr/include/x86_64-linux-gnu'
all_source = crawl_dir(linux_src, {})
