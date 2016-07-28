
import re, pandas as pd, numpy as np

# open file
file=open('/Users/Bennett/Desktop/scraping/778946.txt').read()

# re patterns
subhead=re.compile(r'==[^=]+==')
sig=re.compile(r'\[\[Usuario[^|]+|[^|]+]]')

# Recognize user talk page links when there are two signatures within a few characters of each other

# create and fill dataframe
df=pd.DataFrame(index=[],columns=['lang','page_id','page_title','subheading_title','user_text','indentation_depth','line_in_subheading'])
                         

## IDEAS

# Easy Way to Code? (Loops through twice)
# Find all subheadings, mark beginning and end points, then find all comments + their indentations and group them under
# subheadings by their beginning/end point.

# Harder Way to Code? (Loops through once)
# Once a subheading is found, mark all comments until another subheading is found.
# Find subheading, loop through a search of comments and subheadings, if a comment is found record the data and iterate,
# if subheading is found start new loop.



