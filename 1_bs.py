from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os

# Author : Pruthvi R. Hingu

search = input("Enter search term : ")
params = {"q":search} 
r = requests.get("https://www.bing.com/search",params=params)

soup = BeautifulSoup(r.text,"html.parser")

results = soup.find("ol",{"id":"b_results"})

links = soup.findAll("li",{"class":"b_algo"})

for item in links:
    item_text = item.find("a").text
    item_href = item.find("a").attrs["href"]

    if item_text and item_href:
        # By parent
        # print("Item parent = ",item.find("a").parent)
        # print("Item summary = ",item.find("a").parent.parent.find("p").text)
        
        print("Item text = "+item_text)
        print("Item href = "+item_href+'\n')

        # children = item.children
        # count = 0
        # for child in children:
        #     print(str(count),"child : ",child)
        #     count+=1

        children = item.contents[0]
        print("Next sibling of the h2: ", children.next_sibling)


print("\n\n\n\n Now see gettinf pictures of pizzas\n")
r_pics = requests.get("https://www.bing.com/images/search",params=params)

dir_name = search.replace(" ","_").lower()
if not os.path.isdir(dir_name):
    os.makedirs(dir_name)

soup_pics = BeautifulSoup(r_pics.text,"html.parser")

links_pics = soup_pics.findAll("a",{"class":"thumb"})

for item in links_pics:
    try:
        img_obj = requests.get(item.attrs["href"])
        print("Getting ",item.attrs["href"])
        title = item.attrs["href"].split("/")[-1]
        try:
            img = Image.open(BytesIO(img_obj.content))
            img.save("./"+ dir_name+"/"+title,img.format)
        except:
            print("could not save img")
    except:
        print("could not request img")