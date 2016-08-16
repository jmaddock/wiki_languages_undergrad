import mwxml, re, pandas as pd

df=pd.DataFrame(columns=['lang','page_id','page_title','subheading_title','user_text','indentation_depth','subheading_line'])
index=1
     
# All necessary re-patterns
MISC=r'(\s*(\[\[[^\]]*]])*\s*.){0,10}'  #matches either a space, a page element (anything between brackets), or any character, up to 10 times
SUBHEAD=r'==[^=]+==';
COMMENT_REG=r'\[\[User[^|]+\|[^|]+]]'
COMMENT_TALK=COMMENT_REG+MISC+r'\[\[User[^|]+:[^|]+\|[^\]]+]]'   # Talk page has a regular comment, some misc, then a talk comment
COMMENT_ANON=r'\{\{[Nn]ofirmado\|[^}]+}}'
NEW_LINE=r'\n\n|\n'
ALL='|'.join([COMMENT_TALK,COMMENT_ANON,COMMENT_REG])


# Measures indentation by the number of colons at the beginning of a comment, after bullets or numbering symbols
# Creates data frame with all relevant information
def identify_comment_metrics(sub_title,comment,author):
     global index, lang, _id_, page_title, df, comment_num
     indent=0
     while comment.startswith('*') or comment.startswith('#'):
          comment=comment[1:-1]
     while comment.startswith(':'):
          indent+=1
          comment=comment[1:-1]
     df.loc[index]=(lang,_id_,page_title,sub_title,author,indent,comment_num)
     index+=1
     
     
        
# Identify subheading title, find all comments by indentation and author tag, then loop through and
# break them into comments
def split_into_comments (subheading):
     if re.match(SUBHEAD, subheading):
          sub_title=re.match(SUBHEAD, subheading)
          subheading=subheading[sub_title.end():-1]
          sub_title=sub_title.group()
     else:
          sub_title='Top_Subtitle'
     comments_list=list()
     authors_list=list()
     comment_iterator=re.finditer(NEW_LINE, subheading)
     comment_begin=0
     for comment in comment_iterator:
          author=re.search(ALL,subheading[comment_begin:comment.end()])
          if author:
               comments_list.append(subheading[comment_begin:comment.end()])
               authors_list.append(subheading[comment_begin+author.start():comment_begin+author.end()])
               comment_begin=comment.end()
     author=re.search(ALL,subheading[comment_begin:-1])
     if author:
          comments_list.append(subheading[comment_begin:-1])
          authors_list.append(subheading[comment_begin+author.start():comment_begin+author.end()])
     return comments_list, sub_title, authors_list

                               
# Find beginning of page, find all subheadings, then loop thorugh and break into a list
def split_subheadings_into_list (file):
     subheading_list=list()
     sub_iterator=re.finditer(SUBHEAD, file)
     last_sub=0
     for sub in sub_iterator:
          subheading_list.append(file[last_sub:sub.start()])
          last_sub=sub.start()
     subheading_list.append(file[last_sub:-1])
     return subheading_list


# Linearly runs through all the above functions
def parse_page (file):
     global comment_num
     subheading_list=split_subheadings_into_list(file)
     for subheading in subheading_list:
          comments_list,sub_title,authors_list=split_into_comments(subheading)
          comment_num=1
          #Use a dictionary for comments and authors?
          for i in range(len(comments_list)):
               identify_comment_metrics(sub_title,comments_list[i],authors_list[i])
               comment_num+=1
              

# Creates page iterator and feeds it into parse_page, appending the resulting dataframe to the master dataframe
# dump has 400202 elements
# skip empty talk pages
def main():
     global lang, _id_, page_title, index
     dump=mwxml.Dump.from_file(open(u'/Users/Bennett/Desktop/scraping/simplewiki-latest-pages-meta-current.xml','rb'))
     for page in dump:
         lang=dump.site_info.dbname
         if page.namespace==1:
             for revision in page:
                  if revision.text==None:
                       print('Empty: '+ revision.page.title)
                  else:                      
                       _id_=revision.page.id
                       page_title=revision.page.title
                       try:
                            parse_page(revision.text)
                       except TypeError:
                            print('Type Error, expected string or bytes-like object')
                            print(revision)
                            print(revision.text)

     df.to_csv('xml_output.csv',index=False)

main()
