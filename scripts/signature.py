from Crypto.Util.number import *
from hashlib import md5 
import os
import re
import json

p,q = 179489823466965033388736877593438481917 , 181478545186404321965187956638508911883

def method_signer(p,q,class_name, method_class ,number_of_args):    # class name consist of both return value and class name.
    m = (str(class_name)+str(method_class)+str(number_of_args)).encode()
    n = p*q 
    phi = (p-1)*(q-1)
    e = 65537 
    d = inverse(e,phi)
    D = md5(m).digest()
    sign = pow(bytes_to_long(D),d,n)
    return sign
def class_signer(p,q,class_signs,instance_signs):
    cc_signs = "".join(str(i) for i in class_signs)
    ic_signs = "".join(str(i) for i in instance_signs)
    m = (cc_signs+ic_signs).encode()    
    n = p*q 
    phi = (p-1)*(q-1)
    e = 65537 
    d = inverse(e,phi)
    D = md5(m).digest()
    sign = hex(pow(bytes_to_long(D),d,n))[2:]
    return sign

def oss(function_name):
    e = function_name
    cd_each_class = "dsdump -o -vvv -a arm64 -f" + " " + e + " " + filename + " > fil.txt" #
    os.system(cd_each_class)
    x1 = "ggrep '+' fil.txt | ggrep '[[:space:]]0x000000' | ggrep -o -P '(?<=\+).*(?=)' > class_method.txt" 
    x2 = "ggrep '-' fil.txt | ggrep '[[:space:]]0x000000' | ggrep -o -P '(?<=\-).*(?=)' > instance_method.txt"
    os.system(x1)
    os.system(x2)
    x3 = "while read i; do echo $i |ggrep -o 'arg'| wc -l;  done < class_method.txt > class_method_arguments.txt"
    x4 = "while read i; do echo $i |ggrep -o 'arg'| wc -l;  done < instance_method.txt > instance_method_arguments.txt"
    os.system(x3)
    os.system(x4)
    class_methods = open("class_method.txt",'r').read().split('\n')[:-1]
    instance_methods = open("instance_method.txt",'r').read().split('\n')[:-1]
    class_arguments = open("class_method_arguments.txt",'r').read().split('\n')[:-1]
    instance_arguments = open("instance_method_arguments.txt", 'r').read().split('\n')[:-1]
    return class_methods, instance_methods, class_arguments,instance_arguments

#print("Enter filename: ")
#filename = str(input())

filename = sys.argv[1]
version = sys.argv[2]
os.chdir(sys.argv[3])


x = "dsdump -o -a arm64 " + filename + " > total_bin_metadata.txt" #

#fir = "ggrep 'AF' total_bin_metadata.txt| grep -v '[[:space:]]0x000000'  | ggrep -o -P '(?<=\ ).*(?= :)' | grep '^AF\|_AF\|^_AF' | grep -v '0x000000'> function_namess.txt"
#prefix_name = "FIR" #"AF"

print("Enter prefix name:")
prefix_name = str(input())
fir = "ggrep" + " " + prefix_name + " " + "total_bin_metadata.txt| grep -v '[[:space:]]0x000000'  | ggrep -o -P '(?<=\ ).*(?= :)' | grep" + " " + "'^" + prefix_name + "\|_" + prefix_name + "\|^_" + prefix_name + "' | grep -v '0x000000'> function_namess.txt"

#print(fir)
os.system(x)
os.system(fir)
function_namess = open("function_namess.txt",'r').read().split('\n')[:-1]
class_signs = {}

for u in function_namess:
    class_methods, instance_methods, class_arguments,instance_arguments = oss(u)
    funcname = u
    class_method_signs = []
    instance_method_signs = []
    for i,j in zip(class_methods,class_arguments):
        class_method_signs.append(method_signer(p,q,funcname,i,j))
    for k,l in zip(instance_methods,instance_arguments):
        instance_method_signs.append(method_signer(p,q,funcname,k,l))
    class_signs[u] = class_signer(p,q,class_method_signs,instance_method_signs)

result = json.dumps(class_signs, indent=4)
result = result.replace(" ", "")
result = result.replace("\n", "")
result = result[1:-1]
result = result.replace('"', '')
result = result.split(",")

with open(str(filename) + '-' + str(version) + '-' + 'signatures', 'w') as file:
    for i in result:
        file.write(i)
        file.write('\n')

# Removing intermediate file
os.remove('class_method.txt')
os.remove('class_method_arguments.txt')
os.remove('fil.txt')
os.remove('function_namess.txt')
os.remove('instance_method.txt')
os.remove('instance_method_arguments.txt')
os.remove('total_bin_metadata.txt')
