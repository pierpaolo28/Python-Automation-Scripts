# Towards Data Science Article to Markdown Blog converter

If you are interested in automatically converting a Towards Data Science article in a Markdown blog format, you can make use of the **tds_to_md.py** file. This file requires just one argument: the link to the Towards Data Science article you want to convert. The output markdown file, will then be stored in the **_posts** folder.

```
python tds_to_md.py -a "Full link to article"

python tds_to_md.py -a "https://towardsdatascience.com/answering-causal-questions-in-ai-87c9b53e3a72"
```

This program has been constructed to work with [my personal website](https://pierpaolo28.github.io/), following a specific format (the contacts section is automatically deleted and the featured image is moved at the top before the title and subtitle). Therefore in order to make it work for your own blog, you will have to make different modifications to the source code, including adding your own Medium account full name and username. A commercial version of this project, designed to be suitable for use for any Medium user with an API call, is available on the [services page on my website](https://pierpaolo28.github.io/services/). 

In this version, figures/GIFs captions are assumed to end with a full stop (.) and having just a single full stop in the caption (otherwise the caption and the next paragraph will end up in the same sentence). Medium link embeds are currently not supported for automatic conversion (e.g. they will end up like captions that don't have a full stop). Embeds external from Medium will not appear at all as part of the content (they will need to be added as an HTML embed and not like a link embed like is done on Medium). 

For additional help on usage, use:

```
python tds_to_md.py -h 
# or 
python tds_to_md.py --help

usage: tds_to_md.py [-h] -a Article Link

Converting automatically Towards Data Science (TDS) Posts to Markdown

optional arguments:
  -h, --help       show this help message and exit
  -a Article Link  Link to the TDS article you want to convert
```

The necessary dependencies needed in order to use the **tds_to_md.py** script, can be simply installed using:

```
pip install -r requirements.txt
```

In order to avoid possible conflicts between different libraries versions, it is suggested to create first a virtual environment where to install the packages listed in the **requirements.txt** file. 
