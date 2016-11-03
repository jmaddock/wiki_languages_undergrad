import mwxml, re, pandas as pd, argparse, os
from lang_dict import lang_dict

df=pd.DataFrame(columns=['lang','page_id','page_title','subheading_title','user_text','indentation_depth','subheading_line'])

# All necessary re-patterns
NEW_LINE=r'\n\n|\n'
SUBHEAD=r'(?<!=)==[^=].*?=='
IP_ADD=r'[0-9\.]{9,18}'

anon_count=0

# Create dictionary of regular expressions
def define_comment_tags (lang):
     user=lang_dict['user'][lang]
     anon=lang_dict['anonymous'][lang][0]
     user_rev=''.join(reversed(user))
     anon_rev=''.join(reversed(anon))
     user_list=[]
     rev_user_list=[]
     for user in lang_dict['user'][lang]:
         user_list.append(user)
         rev_user_list.append(''.join(reversed(user)))
     user='|'.join(user_list)
     rev_user='|'.join(rev_user_list)
     anon_list=[]
     rev_anon_list=[]
     for anon in lang_dict['anonymous'][lang]:
         anon_list.append(anon)
         rev_anon_list.append(''.join(reversed(anon)))
     anon='|'.join(anon_list)
     rev_anon='|'.join(rev_anon_list)
     COMMENT_REG=r'\|.{1,55}?:'+user_rev+r'\[\['
     #COMMENT_REG=r'\|.{1,55}?:.{1,55}?\[\['
     COMMENT_ANON=r'}}.{1,55}?\|('+rev_anon+'){{'
     #COMMENT_ANON=r'}}.{1,55}\|.{1,55}{{'
     
     
     ALL='|'.join([COMMENT_REG,COMMENT_ANON])
     return ALL

# Define comment class
class comment(object):
     def __init__ (self,sub_title,comment_text,user_tag,lang):
          self.comment_text=comment_text
          self.subheading_title=self.subtitle_from_subtag(sub_title)
          self.username=self.username_from_usertag(user_tag,lang)
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
     def username_from_usertag (self,usertag,lang):
         global anon_count
         user=lang_dict['user'][lang]
         if usertag==None:
              username=None
         elif re.match(r'\[\['+user+':',usertag,re.IGNORECASE):
             username=re.match(r'[^|]+',usertag[3+len(user):]).group()
         elif re.match(r'{{.{1,55}?\|',usertag):
             username=usertag[re.match(r'{{.{1,55}?\|',usertag).end():-2];
             #print(username);
             #print(usertag);
             #input('pause');
         else:
             username='UNDEFINED'
             #print(usertag);input('pause')
         return username

     def subtitle_from_subtag (self,subtag):
          if subtag=="Top_Subtitle":
               sub_title="Top_Subtitle"
          else:
               sub_title=subtag[2:-2].lstrip()
          return sub_title

# Identify subheading title, find all comments by indentation and author tag, then loop through and
# break them into comments
def create_comments_list (subheading,lang,ALL):
     sub_title=re.match(SUBHEAD, subheading)
     if sub_title:
          subheading=subheading[sub_title.end():]
          sub_title=sub_title.group()  
     else:
          sub_title='Top_Subtitle'
     comments_list=list()
     last_end=0
     newline_iterator=re.finditer(NEW_LINE, subheading)
     #Grab last author from each line
     for line in newline_iterator:
         #print(subheading[last_end:line.start()]);input('pause')
         reversed_text=''.join(reversed(subheading[last_end:line.end()]))
         if re.search(ALL,reversed_text):
               tag_loc=re.search(ALL,reversed_text)
               comment_text=subheading[last_end:line.start()]
               user_tag=''.join(reversed(reversed_text[tag_loc.start():tag_loc.end()]))
               comments_list.append(comment(sub_title,comment_text,user_tag,lang))
         last_end=line.end()
     # Text does not end with newline, so check the end of the text after the loop
     author=re.search(ALL,subheading[last_end:])
     reversed_text=''.join(reversed(subheading[last_end:]))
     if re.search(ALL,reversed_text):
         tag_loc=re.search(ALL,reversed_text)
         comment_text=''.join(reversed_text)
         user_tag=''.join(reversed(reversed_text[tag_loc.start():tag_loc.end()]))
         comments_list.append(comment(sub_title,comment_text,user_tag,lang))
     if comments_list==list():
          comment_text=''
          user_tag=None
          comments_list.append(comment(sub_title,comment_text,user_tag,lang))
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
def parse_page (revision,lang,ALL):
     file=revision.text
     subheading_list=split_subheadings_into_list(file)
     for subheading in subheading_list:
          comments_list=create_comments_list(subheading,lang,ALL)
          comment_num=1
          for comment in comments_list:
               df.loc[len(df)]=(lang,revision.page.id,revision.page.title,comment.subheading_title,comment.username,comment.indent,comment_num)
               # People dont use append to add to dataframes. Efficiency wise dataframes are supposed to be preallocated, so
               # if speed is a concern a different method for writing data (probably to a csv) should be used
               #df=df.append(pandas.DataFrame(data=[[val1,val2,val3]],columns=['column name1', 'column name2']), ignore_index=True)
               comment_num+=1
              
# Creates page iterator and feeds it into parse_page, appending the resulting dataframe to the master dataframe
# skip empty talk pages
def parse_dump(lang):
     
     # Get dump file
     cwd = os.getcwd()
     if os.path.isfile(cwd+'/wiki_dumps/'+lang+'wiki-latest-pages-meta-current.xml'):
          file_path = cwd+u'/wiki_dumps/'+lang+'wiki-latest-pages-meta-current.xml'
     else:
          file_path = cwd+u'/wiki_dumps/'+lang+'wiki-latest-pages-meta-current1.xml'
     dump=mwxml.Dump.from_file(open(file_path,'rb'))
     
     # Parse dump file
     ALL=define_comment_tags(lang)
     for page in dump:
         if page.namespace==1:
             for revision in page:
                  if revision.text==None:
                       print('Empty: '+ revision.page.title)
                  else:
                       parse_page(revision,lang,ALL)
     df.to_csv('xml_output('+lang+').csv',index=False,na_rep='None',encoding="utf-8")


# Construct argument parser for command line usage
def main (input_lang):
     parser=argparse.ArgumentParser()
     parser.add_argument("-l","--lang",help="Define the language of the given wikipedia dump")
     parser.add_argument("-f","--file",help="Give path to Wikidump")
     parser.add_argument("-o","--output",help="Define output file location")
     args=parser.parse_args()

     # Enforce input requirement
     if not (args.lang):
          lang=input_lang
     else:
          lang=args.lang
          
     parse_dump(lang)
     return

if __name__ =='__main__':
     main('es')
