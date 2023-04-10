from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

check = len(sys.argv)
if (check <= 1):
    print("-> Usage:")
    print("     $ python3 program.py URL \n     URL - [URL of the Library's GitHub versions list page]")
    sys.exit("Exiting due to no command-line arguments")

url = sys.argv[1]
for i in range(10):                     # The program is not working properly sometimes, looping is somehow fixing the error
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

soup_text = soup.get_text()
soup_text = soup_text.replace('\n', '')
soup_text = soup_text.replace('  ', ' ')
footer_index = soup_text.find('Footer')
new_soup = soup_text[:footer_index]
new_soup = new_soup.split(' ')
result = new_soup[len(new_soup) - 1]
result = result.split()

print(result)
print("Number of versions: {}".format(len(result)))