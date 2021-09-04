from markdown2 import Markdown
import requests
import json
from datetime import datetime
import pandas as pd
import re
import os
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Get images from Medium articles for a large number of posts (or all!)
full_name = "Pier Paolo Ippolito"
user_name = "pierpaoloippolito28"
limit, rss_number_of_pages = 60, 3
posts_info = 0


url = "https://medium.com/@{0}/latest".format(user_name)
headers = {'Accept': 'application/json'}
response = requests.get(
    url, params={"limit": limit, "next": rss_number_of_pages}, headers=headers)
data = response.text
data_no_xml = data[data.find("{"):]
resp_dict = json.loads(data_no_xml)
posts_info = resp_dict['payload']["references"]["Post"].keys()
print("Number of articles fetched: ", len(posts_info))
links, file_names = [], []
for i in posts_info:
    links.append("https://medium.com/@pierpaoloippolito28/" +
                 resp_dict['payload']["references"]["Post"][i]['id'])
    title = resp_dict['payload']["references"]["Post"][i]['title']
    title = '-'.join(title.split(' ')).replace(":", "").replace("?", "")
    date = float(resp_dict['payload']["references"]
                 ["Post"][i]["firstPublishedAt"]) / 1000
    date = datetime.fromtimestamp(date)
    date = date.strftime("%Y-%m-%d")
    file_names.append("{0}-{1}".format(date, title))

articles_df = pd.DataFrame({'Name': file_names, 'Link': links})
articles_df.to_csv('_images/articles_list.csv', index=False)

# Creating a folder to store the md articles and saving them
if not os.path.exists("_images/"):
    os.makedirs("_images/")

for link, filename in zip(links, file_names):
    post = requests.get(link)
    redirected_link = post.url.split("?")[0]
    post = requests.get(redirected_link).text
    post = md(post)

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
            print(redirected_link)
            print(i["src"])
