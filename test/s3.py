import os
import sys
import time
import boto3

path = "/home/nitin/script/python/python/test"
now = time.time()

s3 = boto3.client("s3")
for f in os.listdir(path):
  if os.stat(f).st_mtime < now - 7 * 86400:
    if os.path.isfile(f):
      print("older file", f)
      
      s3.upload_file(f, "ais-poc-us-east-1-tothenew-backend", f"prod-env/logs/{f.split('/')[-1]}")
      os.remove(os.path.join(path, f))
