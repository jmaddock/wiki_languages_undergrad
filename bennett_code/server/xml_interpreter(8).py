import mwxml, re, pandas as pd, argparse, os, datetime
# lang_dict is a python dictionary used to make different user tags for each language edition
from lang_dict import lang_dict

cwd = os.getcwd()
#Location of Wikipedia dumps
DUMP_DIRECTORY='/srv/wiki_language_data/dumps/complete_dump/'

df=pd.DataFrame(columns=['lang','page_id','page_title','subheading_title','user_text','indentation_depth','subheading_line'])

# All necessary re-patterns
NEW_LINE=r'\n\n|\n'
SUBHEAD=r'(?<!=)==[^=].*?=='

# Test output utility
# Used to get a csv output when the script is not allowed to run to completion
def output_csv(name,lang):
     df.to_csv('data/raw_data/'+name+'_xml_output_'+lang+'.csv',index=False,na_rep='None',encoding='utf-8')
     return

# Makes the text in the output csv the same as the text given by the wikipedia talk page json found online
# (e.g. /u123456)
def encode_text(text):
          try:
               text=text.encode('raw_unicode_escape').decode('utf-8')
               return text
          except:
               return text

# Creates a single regular expression for a given language that catches any usertag defined in "lang_dict"
# Different user tags are ordered in a relatively efficient way (most common tags are first)
def define_comment_tags (lang):
     user_list=lang_dict['user'][lang]+lang_dict['user']['en']
     anon_list=lang_dict['anonymous'][lang]+lang_dict['anonymous']['en']
     user='|'.join(user_list)
     rev_user=''.join(reversed('|'.join(reversed(user_list))))
     anon='|'.join(anon_list)
     rev_anon=''.join(reversed('|'.join(reversed(anon_list))))
     COMMENT_REG=r'\|.{1,55}?:('+rev_user+r')\[\['
     COMMENT_ANON=r'}}.{1,55}?\|('+rev_anon+'){{'
     # Uncomment this code to make a match with any tag-like text
     #COMMENT_REG=r'\|.{1,55}?:.{1,55}?\[\['
     #COMMENT_ANON=r'}}.{1,55}\|.{1,55}{{'
     
     ALL='|'.join([COMMENT_REG,COMMENT_ANON])
     return ALL

# Define comment class
# The comment class takes the entire text of a comment (distinguished by a newline character) and uses methods to
# extract the number of indents, username from usertag, and subheading from subtag
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
     
     # Extract username from user tag.
     # Can also be used to find new tags for input into "lang_dict". If the commented code in "define_comment_tags()" is 
     # uncommented, all tag-like text is put through this method to try to find usertext. The bottom of this method can
     # uncommented to print a message anytime a tag is found that is not accounted for in lang_dict. That tag text can
     # then be added to lang_dict and the script will run again without triggering on that tag. This is done until
     # all the tags that come up are distincly not usertags.
    
     def username_from_usertag (self,usertag,lang):
         user_list=lang_dict['user'][lang]+lang_dict['user']['en']
         anon_list=lang_dict['anonymous'][lang]+lang_dict['anonymous']['en']
         user='|'.join(user_list)
         anon='|'.join(anon_list)
         if usertag==None:
              username=None
         elif re.match(r'\[\[('+user+'):',usertag,re.I):
             colon_pos=re.search(':',usertag).end()
             try:
                  username=re.match(r'[^|]+',usertag[colon_pos:]).group()
                  #print('correct user: '+username)
             except:
                  username=None
                  print('re.match failed for user-case: '+usertag)
         elif re.match(r'\{\{('+anon+')\|',usertag,re.I):
              line_pos=re.search('\|',usertag).end()
              username=usertag[line_pos:-2]
              # Uncomment for languages with encoded text 
              #print('Encoded: '+usertag.encode('raw_unicode_escape').decode('utf-8'))
              # Uncomment for languages with decoded text
              #print('Decoded: '+usertag)
              #print('Subtitle: '+self.subheading_title)
         # Use to catch unknown tags
         else:
             username='UNDEFINED'
             try:
                  print('Encoded: '+usertag.encode('raw_unicode_escape').decode('utf-8'))
             except:
                  pass
             print('Decoded: '+usertag)
             print('Subtitle: '+self.subheading_title)
             input('')
         return encode_text(username)

     # Extract subheading title from subtag
     def subtitle_from_subtag (self,subtag):
          if subtag=="Top_Subtitle":
               sub_title="Top_Subtitle"
          else:
               sub_title=subtag[2:-2].lstrip()
          return encode_text(sub_title)

# Find the subheading title, then iterate over the text in sections seperated by newline characters. If a section has a 
# usertag, use it to create a comment object, then append it to a comment list.
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
     # There is only one author between two newlines, so iterate through sections of text
     # and look for a single author
     for line in newline_iterator:
         #print(subheading[last_end:line.start()]);input('pause')
          # Search the text from back to front, because the usertag is always one of the last elements. This is done
          # by reversing the text and re expressions
         reversed_text=''.join(reversed(subheading[last_end:line.end()]))
         if re.search(ALL,reversed_text,re.I):
               tag_loc=re.search(ALL,reversed_text,re.I)
               comment_text=subheading[last_end:line.start()]
               user_tag=''.join(reversed(reversed_text[tag_loc.start():tag_loc.end()]))
               comments_list.append(comment(sub_title,comment_text,user_tag,lang))
         last_end=line.end()
     # Talk pages do not end with a newline. This means that the text between the last newline and the end of the file
     # still needs to be checked. This is the same idea show above but outside of the loop.
     reversed_text=''.join(reversed(subheading[last_end:]))
     if re.search(ALL,reversed_text,re.I):
         tag_loc=re.search(ALL,reversed_text,re.I)
         comment_text=''.join(reversed_text)
         user_tag=''.join(reversed(reversed_text[tag_loc.start():tag_loc.end()]))
         comments_list.append(comment(sub_title,comment_text,user_tag,lang))
     if comments_list==list():
          comment_text=''
          user_tag=None
          comments_list.append(comment(sub_title,comment_text,user_tag,lang))
     return comments_list
                             
# Create an iterator for subheading positions, then break-up subheading texts into a list to use later as input
# to "create_comments_list()"
def split_subheadings_into_list (file):
     subheading_list=list()
     sub_iterator=re.finditer(SUBHEAD, file)
     last_sub=0
     for sub in sub_iterator:
          subheading_list.append(file[last_sub:sub.start()])
          last_sub=sub.start()
     subheading_list.append(file[last_sub:])
     return subheading_list

# Takes a talk page, breaks it up by subheadings using "split_subheadings_into_list()", then creates a list of comments 
# from each subheading using "create_comments_list()". The list of comments is appended to a dataframe that is eventually
# output as a csv for the lang.
def parse_page (revision,lang,ALL):
     file=revision.text
     subheading_list=split_subheadings_into_list(file)
     for subheading in subheading_list:
          comments_list=create_comments_list(subheading,lang,ALL)
          comment_num=1
          for comment in comments_list:
               df.loc[len(df)]=(lang,revision.page.id,encode_text(revision.page.title),comment.subheading_title,comment.username,comment.indent,comment_num)
               # People dont use append to add to dataframes. Efficiency wise dataframes are supposed to be preallocated, so
               # if speed is a concern a different method for writing data (probably to a csv) should be used
               #df=df.append(pandas.DataFrame(data=[[val1,val2,val3]],columns=['column name1', 'column name2']), ignore_index=True)
               comment_num+=1
              
# Finds the dump file for a language given the DUMP_DIRECTORY and naming convention. Iterates over the dump file and
# runs "parse_page()" on each non-empty talk page (page.namespace==1). Once the dump file is completed, the dataframe 
# full of data is output to a csv named with the language and current date.
def parse_dump(lang,output_dir):
     print("Parsing language: "+lang)
     # Get dump file
     if os.path.isfile(DUMP_DIRECTORY+lang+'wiki-latest-pages-meta-current.xml'):
          file_path = DUMP_DIRECTORY+lang+'wiki-latest-pages-meta-current.xml'
     else:
          file_path = DUMP_DIRECTORY+lang+'wiki-latest-pages-meta-current1.xml'
     dump=mwxml.Dump.from_file(open(file_path,'rb'))
     
     # Iterate over the dump file, running "parse_page()" on the talk pages
     ALL=define_comment_tags(lang)
     for page in dump:
         if page.namespace==1:
             for revision in page:
                  if revision.text==None:
                       print('Empty: '+ revision.page.title)
                  else:
                       parse_page(revision,lang,ALL)
     # Export csv file
     now=datetime.datetime.now()
     date='-'.join([str(now.day),str(now.month),str(now.year)[2:]])
     df.to_csv(output_dir+date+'_xml_output_'+lang+'.csv',index=False,na_rep='None',encoding="utf-8")

# Takes any command line arguments and runs "parse_dump" with them. If there are no command line arguments, it sets
# default values.
def main (input_lang):
     parser=argparse.ArgumentParser()
     parser.add_argument("-l","--lang",help="Define the language of the given wikipedia dump")
     #parser.add_argument("-f","--file",help="Give path to Wikidump")
     parser.add_argument("-o","--output",help="Define output file location")
     args=parser.parse_args()

     # Enforce input requirement
     if not (args.lang):
          lang=input_lang
     else:
          lang=args.lang

     if not (args.output):
          output_dir='data/parsed_dumps/'
     else:
          output_dir=args.output+'/'
          
     parse_dump(lang,output_dir)
     return

# If the python file is run without command line, execute it on a specified language. Used for debugging simplicity.
if __name__ =='__main__':
     main('ca')


