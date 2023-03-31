from collections import Counter
import numpy as np
import shutil
import json
import os
import time

time.sleep(5)
x = 'find . | grep "\.json" > json_files.txt'
os.system(x)
f = open('json_files.txt','r')
r = f.read()
r_list = r.split('\n')[:-1]

total_lib_list = []
popular_libs = {}
for i in range(len(r_list)):
    freq = 0
    print(r_list[i])
    f = open(r_list[i],'r')
    e = json.loads(f.read())
    file_name = os.path.basename(r_list[i])
    lib_name = os.path.splitext(file_name)[0]
    print(lib_name)
    if "dependencies" in e:
        total_lib_list.append(e["dependencies"])
        print("\n")
    else:
        shutil. rmtree((os.path.dirname(r_list[i])))
        # print("no dependencies\n")
        # popular_libs[lib_name] = freq
        # shutil. rmtree((os.path.dirname(r_list[i])))

# print(total_lib_list)

all_libs = []
for i in total_lib_list:
    if type(i) is not dict:
        i = dict.fromkeys(i)
    for keys, value in i.items():
        all_libs.append(keys)

# dep_freq = Counter(all_libs)
# keys = list(dep_freq.keys())
# values = list(dep_freq.values())
# sorted_value_index = np.flip(np.argsort(values))
# sorted_libs = {'pod' +' '+ f"'{keys[i]}'": values[i] for i in sorted_value_index}
# all_libs = []
# for i, j in sorted_libs.items():
# #print first key
#     all_libs.append(i)
# with open("pod_libs.txt", "w") as t:
#     t.write('\n'.join(all_libs))


# final_libs_list = json.dumps(sorted_libs,indent=4)
# f = open("pop_libs_list.txt", "w")
# f.write(final_libs_list)
# f.close()
# # print(total_lib_list)

all_libs = []                                      # if version also matters...... 
its_versions = []
for i in total_lib_list:
    if type(i) is not dict:
        i = dict.fromkeys(i)
    for keys, value in i.items():
        all_libs.append(keys + str(value))

dep_freq = Counter(all_libs)
keys = list(dep_freq.keys())
values = list(dep_freq.values())
sorted_value_index = np.flip(np.argsort(values))
sorted_libs = {keys[i]: values[i] for i in sorted_value_index}
# print(sorted_libs)
final_libs_list = list(sorted_libs.keys())
# final_libs_list = json.dumps(final_libs_list, indent=4)
f = open("pop_libs_list.txt", "w")
f.writelines(final_libs_list)
f.close()

























