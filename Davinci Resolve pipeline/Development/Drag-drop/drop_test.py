import sys
import shutil
from time import sleep

droppedFile = sys.argv[1]
print (droppedFile)
shutil.copy(droppedFile, f"new {droppedFile}")
sleep(5)
input()