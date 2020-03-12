import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__)) 
PATH += "/" if not PATH.endswith("/") else ""

print(PATH)
sys.path.append(PATH + "../")
