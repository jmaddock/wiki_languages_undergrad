import mwxml, re, pandas as pd

df=pd.DataFrame(columns=['lang','page_id','page_title','subheading_title','user_text','indentation_depth','subheading_line'])
index=1

# All necessary re-patterns
NEW_LINE=r'\n\n|\n'
ALL='|'.join([COMMENT_TALK,COMMENT_ANON,COMMENT_REG])
MISC=r'(\s*(\[\[[^\]]*]])*\s*.){0,10}'  #matches either a space, a page element (anything between brackets), or any character, up to 10 times
SUBHEAD=r'(?<!=)==[^=].*?==';

COMMENT_REG=r'\[\[[Uu]ser[^|\]]{1,55}\|[^|]+]]'
COMMENT_TALK=COMMENT_REG+MISC+r'\[\[[Uu]ser[^|\]]+:[^|]+\|[^\]]+]]'   # Talk page has a regular comment, some misc, then a talk comment
COMMENT_ANON=r'\{\{subst:[^|\]]+\|[^}]+}}'

def define_comment_tags (lang_ed):
     global COMMENT_REG, COMMENT_TALK, COMMENT_ANON
     # get tag elements from csv
#     lang_df=pd.read_csv('csvfile.csv')
#     lang_df=lang_df[lang_df[lang==lang_ed]]
#     user=lang_df[1]
#     anonymous=lang_df[2]         
     COMMENT_REG=r'\[\[User[^|\]]{1,55}\|[^|]+]]'
     COMMENT_TALK=COMMENT_REG+MISC+r'\[\[User[^|\]]+:[^|]+\|[^\]]+]]'   # Talk page has a regular comment, some misc, then a talk comment
     COMMENT_ANON=r'\{\{subst:[^|\]]+\|[^}]+}}'
     return    


# Define comment class
class comment:
     lang='Unset'
     page_id='Unset'
     page_title='Unset'
     def __init__ (self,sub_title,comment_text,user_tag):
          self.comment_text=comment_text
          self.subheading_title=self.subtitle_from_subtag(sub_title)
          self.username=self.username_from_usertag(user_tag)
          self.indent=self.comment_indents(comment_text)
          
     # Find indentation by finding the number of starting colons, excluding certain characters
     def comment_indents (self,comment_text):
          indent=0
          while comment_text.startswith('*') or comment_text.startswith('#'):
               comment_text=comment_text[1:]
          while comment_text.startswith(':'):
               indent+=1
               comment_text=comment_text[1:]
          return indent
     
     # Find user name in user tag
     def username_from_usertag (self,usertag):
         if usertag.startswith('[[User:'):
             try:
                  username=re.match(r'[^|]+',usertag[7:]).group()
             except:
                  print('re-match didnt work: '+usertag)
                  username='NO USERNAME'
         elif usertag=='no signed comments':
              username='no signed comments'
         else:
             username='ANONYMOUS'
         return username

     def subtitle_from_subtag (self,subtag):
          if subtag=="Top_Subtitle":
               sub_title="Top_Subtitle"
          else:
               sub_title=subtag[2:-2].lstrip()
          return sub_title

# Identify subheading title, find all comments by indentation and author tag, then loop through and
# break them into comments
def create_comments_list (subheading):
     sub_title=re.match(SUBHEAD, subheading)
     if sub_title:
          subheading=subheading[sub_title.end():]
          sub_title=sub_title.group()
     else:
          sub_title='Top_Subtitle'
     comments_list=list()
     newline_iterator=re.finditer(NEW_LINE, subheading)
     line_begin=0
     #Grab last author from each line
     for line in newline_iterator:
          author=False
          for author in re.finditer(ALL,subheading[line_begin:line.end()]):
               pass
          if author:
               comment_text=subheading[line_begin:]
               user_tag=subheading[line_begin+author.start():line_begin+author.end()]
               comments_list.append(comment(sub_title,comment_text,user_tag))
               line_begin=line.end()
     # Text does not end with newline, so check the end of the text after the loop
     author=re.search(ALL,subheading[line_begin:])
     if author:
          comment_text=subheading[line_begin:]
          user_tag=subheading[line_begin+author.start():line_begin+author.end()]
          comments_list.append(comment(sub_title,comment_text,user_tag))
     if comments_list==list():
          comment_text=''
          user_tag='no signed comments'
          comments_list.append(comment(sub_title,comment_text,user_tag))
     return comments_list
                             
# Find beginning of page, find all subheadings, then loop thorugh and break into a list
def split_subheadings_into_list (file):
     subheading_list=list()
     sub_iterator=re.finditer(SUBHEAD, file)
     last_sub=0
     for sub in sub_iterator:
          subheading_list.append(file[last_sub:sub.start()])
          last_sub=sub.start()
     subheading_list.append(file[last_sub:])
     return subheading_list

# Linearly runs through all the above functions
def parse_page (file):
     subheading_list=split_subheadings_into_list(file)
     for subheading in subheading_list:
          comments_list=create_comments_list(subheading)
          comment_num=1
          for comment in comments_list:
               df.loc[len(df)]=(comment.lang,comment.page_id,comment.page_title,comment.subheading_title,comment.username,comment.indent,comment_num)
               # People dont use append to add to dataframes. Efficiency wise dataframes are supposed to be preallocated, so
               # if speed is a concern a different method for writing data (probably to a csv) should be used
               #df=df.append(pandas.DataFrame(data=[[val1,val2,val3]],columns=['column name1', 'column name2']), ignore_index=True)
               comment_num+=1
              
# Creates page iterator and feeds it into parse_page, appending the resulting dataframe to the master dataframe
# skip empty talk pages
def main():
     dump=mwxml.Dump.from_file(open(u'/Users/Bennett/Desktop/scraping/simplewiki-latest-pages-meta-current.xml','rb'))
     for page in dump:
         comment.lang=dump.site_info.dbname
         if page.namespace==1:
             for revision in page:
                  if revision.text==None:
                       print('Empty: '+ revision.page.title)
                  else:
                       comment.page_id=revision.page.id
                       comment.page_title=revision.page.title
                       parse_page(revision.text)
     df.to_csv('xml_output(current).csv',index=False)

if __name__ =='__main__':
     main()
