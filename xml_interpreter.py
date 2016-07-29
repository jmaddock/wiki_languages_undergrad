
import re
import pandas as pd
import numpy as np

file=open('/Users/Bennett/Desktop/scraping/778946.txt').read();
df_final=pd.DataFrame(columns=['lang','page_id','page_title','subheading_title','user_text','indentation_depth','line_in_subheading'])
df=pd.DataFrame(columns=['subheading','comment'])
index=2;

# All necessary re-patterns
SUBHEAD=r'==[^=]+==';
COMMENT_REG=r'\[\[Usuario[^|]+\|[^|]+]]';
COMMENT_TALK=COMMENT_REG+r'\s*\(*\[\[Usuario [^|]+:[^|]+\|[^\]]+]]';
COMMENT_ANON=r'\{\{nofirmado\|[^|]+}}';
ALL='|'.join([SUBHEAD,COMMENT_TALK,COMMENT_ANON,COMMENT_REG])



# Can I simplify this appending
def comments(position, subheading, comment): 
     global index;
     df.loc[index]=[subheading, comment];
     index=index+1;
     parser(position, subheading);



# Searches for subheadings and comments. Updates subheading variable if subheading and runs comment() if comment.
def parser(position, subheading):
    x=re.search(ALL, file[position:-1])
    if x:
        if re.search(SUBHEAD,x.group()):
            parser(position+x.end(), x.group());
 
        else:
            comments(position+x.end(), subheading, x.group());


def main ():
    parser(0, 'top_level');
    df=pd.DataFrame(index=[],columns=['lang','page_id','page_title','subheading_title','user_text','indentation_depth','line_in_subheading']);


print(parser(0, 'top_level'))
print(df)


# How do I capture this one very long comment that I dont even understand:

#{{Nofirmado|80.102.224.237|<font style=\"font-family:Verdana; font-size:11px; font-variant:small-caps\">'''[[Usuario:Thor8|
#<font color=firebrick>Thor</font><font color=orange>8</font>]]''' [[Image:Banner of the Holy Roman Emperor
#(after 1400).svg|25px]] '''([[Usuario Discusi\u00f3n:Thor8|<font color=firebrick>Di
#</font><font color=orange>scusi</font><font color=firebrick>\u00f3n</font>]])'''</font> 18:54 21 ago 2008 (UTC)}}
