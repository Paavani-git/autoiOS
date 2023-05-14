# Script to download ipa files from ipaspot using command line
# ipaspot URL: https://ipaspot.app/

#!/bin/bash
URL1 = https://ipaspot.app/categories/tweakedapps.html
URL2 = https://ipaspot.app/categories/cydiaapps.html
URL3 = https://ipaspot.app/categories/jailbreaks.html

curl URL1 | grep -Eio '(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]' | grep ".ipa$" > ipafiles1.txt
curl URL2 | grep -Eio '(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]' | grep ".ipa$" > ipafiles2.txt
curl URL3 | grep -Eio '(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]' | grep ".ipa$" > ipafiles3.txt

wget -i ipafiles1.txt
wget -i ipafiles2.txt
wget -i ipafiles3.txt