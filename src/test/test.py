import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__)) 
PATH += "/" if not PATH.endswith("/") else ""
sys.path.append(PATH + "../")
sys.path.append(PATH + "../engine/")
sys.path.append(PATH + "../backend/")
sys.path.append(PATH + "../gui/")
sys.path.append(PATH + "../gui/interface/")
