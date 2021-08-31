import requests
from markdownify import markdownify as md
import re
import os
import argparse

# In this version the contacts section is automatically deleted and the featured image is moved at the top before the title and subtitle
full_name, user_name = "Pier Paolo Ippolito", "pierpaoloippolito28"

parser = argparse.ArgumentParser(
    prog='tds_to_md.py', description="Converting automatically Towards Data Science (TDS) Posts to Markdown")
parser.add_argument('-a', metavar='Article Link',
                    help="Link to the TDS article you want to convert", required=True, type=str)
args = parser.parse_args()

r = requests.get(args.a)
post = md(r.text)

# Fetching the article publication date to create md file title
pub_date = post[post.find("datePublished")+len("datePublished") +
                3:post.find("datePublished")+len("datePublished")+50].split("T")[0]
filename = pub_date + "-" + "-".join([i.title()
                                      for i in args.a.split("/")[3].split("-")[:-1]]) + ".md"

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

# Add a new line after each image and after each caption (captions starting with a P or a whitespace are handled differently to avoid problems with links
# in captions e.g. Unsplash), is assumed that each caption ends with a full stop
no_contacts = re.sub(r'(\!\[\]\(?(.*?)\))([^P ](.*?)\.)',
                     r'\1\n\3\n\n', no_contacts, flags=re.DOTALL)

# Invert the order at the top of the article from Titla, Subtitle, Image to Image, Title, Subtitle
start = no_contacts.find("![](https://")
for i, j in enumerate(no_contacts[start:]):
    if j == '\n':
        end = start + i
        break
intro_image = no_contacts[start:end]
no_contacts = no_contacts.replace(no_contacts[start:end+1], "")
no_contacts = intro_image + "\n" + no_contacts

# Creating a folder to store the md articles and saving them
if not os.path.exists("_posts/"):
    os.makedirs("_posts/")

with open('_posts/'+filename, 'w', encoding='utf-8') as f:
    print(no_contacts, file=f)
