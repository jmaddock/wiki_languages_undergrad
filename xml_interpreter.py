
import re
import pandas as pd
import numpy as np

file=open('/Users/Bennett/Desktop/scraping/778946.txt').read();
#df_final=pd.DataFrame(columns=['lang','page_id','page_title','subheading_title','user_text','indentation_depth','line_in_subheading'])
df=pd.DataFrame(columns=['subheading','comment'])
index=2;

# All necessary re-patterns
MISC=r'(\s*(\[\[[^\]]*]])*\s*.){0,10}'  #matches either a space, a page element (anything between brackets), or any character up to 10 times
SUBHEAD=r'==[^=]+==';
COMMENT_REG=r'\[\[Usuario[^|]+\|[^|]+]]';
COMMENT_TALK=COMMENT_REG+MISC+r'\[\[Usuario [^|]+:[^|]+\|[^\]]+]]';   # Talk page has a regular comment, some misc, then a talk comment
COMMENT_ANON=r'\{\{[Nn]ofirmado\|[^}]+}}';
ALL='|'.join([SUBHEAD,COMMENT_TALK,COMMENT_ANON,COMMENT_REG])



# Can I simplify this appending method
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

# Give individual pages to parser()
def main ():
    parser(0, 'top_level');

    df=pd.DataFrame(index=[],columns=['lang','page_id','page_title','subheading_title','user_text','indentation_depth','line_in_subheading']);

parser(0, 'top_level')
print(df)
