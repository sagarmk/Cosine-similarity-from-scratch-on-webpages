import re, math
from collections import Counter
import urllib
import urllib.request
import sys
import operator
import csv
from bs4 import BeautifulSoup
from tabulate import tabulate

#  grabbing text from url

def parse_from_url(url):
     html = urllib.request.urlopen(url).read()
     soup = BeautifulSoup(html, "lxml" )
     for script in soup(["script", "style"]):
      script.extract()
     text = soup.get_text()
     return text


##############################################
# calculating cosine simmilarity starts here #
##############################################

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator



def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)



def co_cal(url1, url2):
     text1 = parse_from_url(url1)
     text2 = parse_from_url(url2)


     vector1 = text_to_vector(text1)
     vector2 = text_to_vector(text2)

     cosine11 = get_cosine(vector1, vector2)
     return cosine11


urllist = []

def userWish():
     print("------------------------------------------------------------------")
     print("| Select 1 > To MANUALLY enter  set of urls                       | ")
     print("| Select 2 > To use PRE-DEFINED set of urls of 7*7                | ")
     print("| Select 3 > To process url from INPUT.txt to OUTPUT.txt          | ")
     user_wish = input("| Enter 1 or 2 or 3 => ")
     print("------------------------------------------------------------------")
     user_wish = int(user_wish)

     if user_wish ==1:
          print(("--") * 50)
          print("                 * Please DO NOT include https *                  ")
          print("                  * Enter 'q'  to quit list *                     ")
          def take_inputs():

               val =  input("Enter url ==> ")
               val = "http://"+ val
               if val == 'http://q':
                    return 0
               else:

                    urllist.append(val)
                    take_inputs()
          print(("--") * 50)
          take_inputs()
     elif user_wish ==2:
          urllist.append("https://en.wikipedia.org/wiki/Theodore_Komnenos_Doukas")
          urllist.append("https://en.wikipedia.org/wiki/Empire_of_Thessalonica#Rulers")
          urllist.append("https://en.wikipedia.org/wiki/Second_Bulgarian_Empire")
          urllist.append("https://en.wikipedia.org/wiki/Veliko_Tarnovo")
          urllist.append("https://en.wikipedia.org/wiki/Veliko_Tarnovo_Province")
          urllist.append("https://en.wikipedia.org/wiki/Bulgaria")
          urllist.append("https://en.wikipedia.org/wiki/Ethnic_group")

     elif user_wish ==3:

          with open("input.txt", "r") as filestream:
               for line in filestream:
                    read_list = line.split(",")
               for link in read_list:
                    urllist.append(link)



     else:
          print("*********************************")
          print("          INVALID INPUT          ")
          print("*********************************")
          userWish()

userWish()

# print("URL list = ", urllist)
# print("len = ", len(urllist))

Matrix = [[0 for i  in range(int(len(urllist)))] for j in range(int(len(urllist))) ]
# print(" Initial Matrix = ", Matrix)
type(Matrix)
print(("--")*50)
for row in range(len(urllist)):
     for column in range(len(urllist)):
          percent = ((row+column)/((len(Matrix)-1)*2)*(100))
          # progress = ((("|_|" ) * (row + column)),  str(percent))
          sys.stdout.write("\r>>%s%%" % str(percent))
          sys.stdout.flush()

          if row>= column:
               Matrix[row][column] = " "
          else:
               Matrix[row][column] = co_cal(urllist[row], urllist[column])
print(" ")
print(("=")*100)
print("|  URL list = ")
print("|  ",urllist)
print(("=")*100)
# print("Cosine Matrix = ", Matrix)
print ("Cosine Matrix = ",)
print(("--")*50)
print (tabulate(Matrix, tablefmt='orgtbl'))
max = 0
print(("--")*50)
print(("|")*100)
print((" ")*100)
print("                            For UPPER TRIANGULAR MATRIX                     ")
print((" ")*100)
print(("--")*50)
for i in range(len(Matrix)):



     for j in range(len(Matrix)):

          if str(Matrix[i][j]) > str(max):
             max = Matrix[i][j]
             row_of_max = i
             column_of_max = j
     if str(max) > " ":

          print("There is Max cosine similarity of = ", max, "between = ",urllist[row_of_max], "and = ", urllist[column_of_max])
     max = " "
     print(("--") * 50)

for i in range(len(Matrix)):
     for j in range(len(Matrix)):

          if str(Matrix[i][j]) > str(max):
             max = Matrix[i][j]
             row_of_max = i
             column_of_max = j






print((" ")*100)
print("                            For UPPER TRIANGULAR MATRIX                     ")
print((" ")*100)
print("Maximum cosine similarity among all pages is value = ", max, " And its between =", urllist[row_of_max], "and = ", urllist[column_of_max])
max2 = max
print(("|")*100)
f = open('output.txt', 'w')
f.write(tabulate(Matrix, tablefmt='orgtbl'))
print("                 <++++  Printed OUTPUT in  output.txt file generated     ++++>               ")
f.close()


print(("|")*100)
print((" ")*100)
print("                            For FULL MATRIX                     ")
print((" ")*100)
print(("--")*50)
max = 0
for a in range(len(urllist)):
    max=0
    for b in range(len(urllist)):
        if a == b:
            continue
        else:
            Matrix[a][b] = co_cal(urllist[a], urllist[b])

            if str(Matrix[a][b]) > str(max):
                max = Matrix[a][b]
                row_of_max = a
                column_of_max = b

    print("There is Max cosine similarity of = ", max, "between = ", urllist[row_of_max], "and = ",urllist[column_of_max])
    print(("--") * 50)

# print (tabulate(Matrix, tablefmt='orgtbl'))
print("Maximum cosine similarity among all pages is value = ", max2, " And its between =", urllist[row_of_max], "and = ", urllist[column_of_max])
print(("|")*100)


