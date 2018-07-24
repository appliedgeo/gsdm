import subprocess
import os
import time


r_script_path = "F:\\2018\CIAT\dev\gsdm\\toolbox\scripts\\"

r_cmd = "Rscript " + r_script_path + "example_modified.R > log.txt"

#subprocess.call(r_cmd, shell=False)

os.system(r_cmd)

