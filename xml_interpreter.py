import re
import pandas as pd
import numpy as np

#df_final=pd.DataFrame(columns=['lang','page_id','page_title','subheading_title','user_text','indentation_depth','line_in_subheading'])
df=pd.DataFrame(columns=['subheading','comment','indentation'])
index=1
     
# All necessary re-patterns
MISC=r'(\s*(\[\[[^\]]*]])*\s*.){0,10}'  #matches either a space, a page element (anything between brackets), or any character, up to 10 times
SUBHEAD=r'==[^=]+==';
COMMENT_REG=r'\[\[Usuario[^|]+\|[^|]+]]'
COMMENT_TALK=COMMENT_REG+MISC+r'\[\[Usuario [^|]+:[^|]+\|[^\]]+]]'   # Talk page has a regular comment, some misc, then a talk comment
COMMENT_ANON=r'\{\{[Nn]ofirmado\|[^}]+}}'
BEGINNING=r'"\*":'
NEW_LINE=r'\\n\\n'

# Measures indentation by the number of colons at the beginning of a comment, after bullets or numbering symbols
def identify_comment_metrics(sub_title,comment_num,comment):
     global index, df
     indent=0
     while comment.startswith('*') or comment.startswith('#'):
          comment=comment[1:-1]
     while comment.startswith(':'):
          indent+=1
          comment=comment[1:-1]
     df.loc[index]=(sub_title,comment_num,indent)
     index+=1        
     
        
# Identify subheading title, find all comments, then loop through and break them into comments
# As an added measure, disregards newline markers from subheadings
def split_into_comments (subheading):
     if re.search(SUBHEAD, subheading):
          sub_title=re.search(SUBHEAD, subheading)
          subheading=subheading[sub_title.end():-1]
          sub_title=sub_title.group()
     else:
          sub_title='Top_Subtitle'
     comments_list=list()
     comment_iterator=re.finditer(NEW_LINE, subheading)
     last_comment=0
     for comment in comment_iterator:
          if len(subheading[last_comment:comment.end()])>10:
               comments_list.append(subheading[last_comment:comment.end()])
               last_comment=comment.end()
          else:
               last_comment=comment.end()               
     comments_list.append(subheading[last_comment:-1])
     return comments_list, sub_title
                                
# Find beginning of page, find all subheadings, then loop thorugh and break into a list
def split_subheadings_into_list (file):
     subheading_list=list()
     file=file[re.search(BEGINNING, file).end():-1]
     sub_iterator=re.finditer(SUBHEAD, file)
     last_sub=0
     for sub in sub_iterator:
          subheading_list.append(file[last_sub:sub.start()])
          last_sub=sub.start()
     subheading_list.append(file[last_sub:-1])
     return subheading_list

def main ():
     file=open('/Users/Bennett/Desktop/scraping/778946.txt').read()
     subheading_list=split_subheadings_into_list(file)
     for subheading in subheading_list:
          comments_list,sub_title=split_into_comments(subheading)
          #print(sub_title,': ',comments_list, '\n')
          comment_num=1
          for comment in comments_list:
               identify_comment_metrics(sub_title,comment_num,comment)
               comment_num+=1
     print(df)
          
          
main()
