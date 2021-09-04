from markdown2 import Markdown
import requests
import re
import os
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import argparse

# Get images from Medium articles for a large number of posts (or all!)
full_name, user_name = "Pier Paolo Ippolito", "pierpaoloippolito28"

parser = argparse.ArgumentParser(
    prog='single_article_imgs_download.py', description="Downloading locally all the images from a Towards Data Science (TDS) article")
parser.add_argument('-a', metavar='Article Link',
                    help="Link to the TDS article you want to get the images from", required=True, type=str)
args = parser.parse_args()

# Creating a folder to store the md articles and saving them
if not os.path.exists("_images/"):
    os.makedirs("_images/")

post = requests.get(args.a).text
post = md(post)
# Fetching the article publication date to create md file title
pub_date = post[post.find("datePublished")+len("datePublished") +
                3:post.find("datePublished")+len("datePublished")+50].split("T")[0]
filename = pub_date + "-" + "-".join([i.title()
                                      for i in args.a.split("/")[3].split("-")[:-1]])
filename = filename.replace(":", "").replace("?", "")
# Start reading all the file, go through ![Towards Data Science]( and stop after the link at this signal -)
no_header = re.sub(
    '^(.*?)\[\!\[Towards Data Science\]\(?(.*?)\-\)', '', post, flags=re.DOTALL)
# Start reading the file (from where we stopped before), go through [Open in app]( and stop after the link at this signal -)
no_header = re.sub(
    '^(.*?)\[Open in app\]\(?(.*?)\-\)', '', no_header, flags=re.DOTALL)
# Remove everything at the bottom af the file once the article is finished and the post sidebar is referenced
no_bottom = no_header.split('''[{0}
-------------------](https://{1}.medium.com/?source=post_sidebar--------------------------post_sidebar-----------)'''.format(full_name, user_name))[0]

# Remove the contacts section from the article by referencing the contacts title and the last contact on the list (Kaggle)
no_contacts = no_bottom.split('''Contacts
========''')[0] + no_bottom.split('''* [Kaggle](https://www.kaggle.com/pierpaolo28?source=post_page---------------------------)\n''')[1]

# Remove any tiny alt image from the markdown conversion (Image)
no_contacts = re.sub('\!\[\]\(https\:\/\/miro\.medium\.com\/max\/60\/?(.*?)q\=20\)\!\[\]\(\)',
                     '', no_contacts, flags=re.DOTALL)
# and (GIFs)
no_contacts = re.sub('\!\[\]\(https\:\/\/miro\.medium\.com\/freeze\/max\/?(.*?)q\=20\)\!\[\]\(\)',
                     '', no_contacts, flags=re.DOTALL)

# Removing writer, publisher and publication date from the top of the article
no_contacts = re.sub('''\[\!\[{0}\]\(?(.*?)\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\-\-\)\!\[\]'''.format(full_name),
                     '![]', no_contacts, flags=re.DOTALL)

# Creating a folder to store the md articles and saving them
if not os.path.exists("_images/{0}".format(filename)):
    os.makedirs("_images/{0}".format(filename))

markdowner = Markdown()
soup = BeautifulSoup(markdowner.convert(no_contacts), 'html.parser')
images = soup.find_all("img")
for name, i in enumerate(images):
    try:
        img_data = requests.get(i["src"]).content
        if i["src"].split(".")[-1] == "jpeg":
            if not os.path.exists("_images/{0}/{1}.jpeg".format(filename, name)):
                with open('_images/{0}/{1}.jpeg'.format(filename, name), 'wb') as handler:
                    handler.write(img_data)
        elif i["src"].split(".")[-1] == "png":
            if not os.path.exists("_images/{0}/{1}.png".format(filename, name)):
                with open('_images/{0}/{1}.png'.format(filename, name), 'wb') as handler:
                    handler.write(img_data)
        elif i["src"].split(".")[-1] == "gif":
            if not os.path.exists("_images/{0}/{1}.gif".format(filename, name)):
                with open('_images/{0}/{1}.gif'.format(filename, name), 'wb') as handler:
                    handler.write(img_data)
        elif i["src"].split("?")[-1] == "q=20":
            pass
        else:
            if not os.path.exists("_images/{0}/{1}.jpg".format(filename, name)):
                with open('_images/{0}/{1}.jpg'.format(filename, name), 'wb') as handler:
                    handler.write(img_data)
    except:
        print(args.a)
        print(i["src"])
