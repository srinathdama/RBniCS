import sys
import importlib
import subprocess
import os

# training data
Ns     = [5, 10, 20, 30, 40, 50, 75, 100, 200, 300, 400]
# Ns     = [5, 10]
N_test = 5000


def run_rbnics_(N, with_test_flag=False, N_test = 1):
    if with_test_flag:
        subprocess.run('python3 tutorial_thermal_block_1.py -N '+ str(N) +
         ' --with_test_flag  --N_test ' + str(N_test), shell=True)
    else:
        subprocess.run('python3 tutorial_thermal_block_1.py -N '+ str(N), shell=True)

for i, N in enumerate(Ns):
    if i == len(Ns)-1:
        run_rbnics_(N, with_test_flag=True, N_test = N_test)
    else:
        run_rbnics_(N)



# def run_rbnics_(N, reload_flag=True, **kwargs):

#     if reload_flag:
#         import tutorial_thermal_block_1
#         importlib.reload(tutorial_thermal_block_1)
#     else:
#         import tutorial_thermal_block_1
#     tutorial_thermal_block_1.run_rbnics(N, **kwargs)
#     # sys.modules['tutorial_thermal_block_1'].__dict__.clear()
#     # del tutorial_thermal_block_1
#     print(N)