import mwxml, mwparserfromhell as pfh

# All necessary re-patterns

#Combine ranges of nodes that account for one large signature
def combine_complex_signatures(user_list):
    return

# Create list of users with node indexes
def create_user_list(text):
    user_list=list()
    tags_list=text.filter_wikilinks()
    for tag in tags_list:
        if tag.find('[[User')!=-1:
            user_list.append(tag)
    return user_list


# Open dump file and run through the parsing function chain
def main():
    dump=mwxml.Dump.from_file(open('/Users/Bennett/Desktop/scraping/simplewiki-latest-pages-meta-current.xml','rb'))
    for page in dump:
        lang=dump.site_info.dbname
        if page.namespace==1:
            for revision in page:
                _id_=revision.page.id
                page_title=revision.page.title
                text=pfh.parse(revision.text,skip_style_tags=True)
                subheading_list=text.filter_headings()
                last_sub_end=0
                for subheading in subheading_list:
                    user_list=create_user_list(text[0:-1])
                    print(user_list)
                return

main()
