# Medium Article to Markdown Blog converter

In the **medium_to_md.py** (commercial version) file 3 arguments are required:

- The full name of the user on Medium
- The username of the user on Medium
- A link to the article you want to convert to Markdown from Medium

Example usage:

```
python medium_to_md.py -n 'Full Name' -u 'Username' -a 'Full link to article'

python medium_to_md.py -n 'Pier Paolo Ippolito' -u 'pierpaoloippolito28' -a 'https://towardsdatascience.com/answering-causal-questions-in-ai-87c9b53e3a72'
```

In the **pier_medium_to_md.py** file one argument is required: the link to the Medium article, the other 2 parameters are default.

In the Pier version the contacts section is automatically deleted and the featured image is moved at the top before the title and subtitle (like in the website blog).

```
python pier_medium_to_md.py -a 'Full link to article'

python pier_medium_to_md.py -a 'https://towardsdatascience.com/answering-causal-questions-in-ai-87c9b53e3a72'
```

In both versions, figures/GIFs captions are assumed to end with a full stop (.) and that they have just a single full stop in the caption (otherwise the caption and the next paragraph will end up in the same sentence). Medium link embeds are currently not supported for automatic conversion (e.g. they will end up like captions that don't have a full stop). Embeds external from medium will not appear at all as part of the content (they will need to be added as an html embed and not like a link embed like is done on Medium). 

**TODO**:

Download images from Medium (in pier=True version)

Add requirements.txt

Improve argparse version for product version

Publish on Automation scripts GitHub repository

Create API version to sell as a product on the website

Add on an API marketplace + AWS

Tweet/Post blog article/Linkedin post about the end product and the process to create it