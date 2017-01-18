import pandas as pd, os, csv, statistics as stats, re

# Min/max # of users for a page to be considered relevant
MIN_USERS=0
MAX_USERS=100000

def process_page(first_row,file_iter):
    curr_row=first_row
    page_id=first_row.page_id
    flag=False
    # Initialize variables
    num_sigs=0
    max_depth=0
    subs_page=1
    sig_list=[]
    # Create indent list with each item being a list of the indents for a subheading
    page_indents=[]
    sub_indents=[]
    last_sub=curr_row.subheading_title
    while page_id==curr_row.page_id:
        curr_sub=curr_row.subheading_title
        if curr_sub!=last_sub:
            subs_page+=1
            last_sub=curr_row.subheading_title
            page_indents.append(sub_indents)
            sub_indents=[]
        user_sig=curr_row.user_text
        if user_sig!='None':
            sub_indents.append(curr_row.indentation_depth)
            if not user_sig in sig_list:
                sig_list.append(user_sig)
                num_sigs+=1
                depth+=1
        # Go to next row
        try:
            curr_row=next(file_iter)
        except StopIteration:
            flag="end"
            break
    page_indents.append(sub_indents)
    # Manipulate page_indents
    flat_indents=[val for sublist in page_indents for val in sublist]
    max_indent=0
    median_indent=0
    mean_indent=0
    if flat_indents:
        max_indent=max(flat_indents)
        median_indent=stats.median(flat_indents)
        mean_indent=stats.mean(flat_indents)
    page_output=[page_id,subs_page,posts_sub,max_indent,users_sub]
    # Check number of user signatures
    if (num_sigs < MIN_USERS or num_sigs > MAX_USERS) and flag==False:
        flag="irrelevant_page"
    return [page_output,curr_row,flag]


def process_file(file_iter,lang):
    pages_total=0
    pages_passed=0
    # Initialize csvwriter for output
    column_names=['page_id','subs_page','posts_sub','max_depth','users_sub']
    csvfile=open('cleaned_data/'+lang+'_output.csv','w')
    output_writer=csv.writer(csvfile)
    output_writer.writerow(column_names)
    # Add a new row for every processed page
    curr_row=next(file_iter)
    while True:
        flag=False
        pages_total+=1
        [page_output,curr_row,flag]=process_page(curr_row,file_iter)
        if not flag:
            output_writer.writerow(page_output)
        elif flag=="end":
            break
        elif flag=="irrelevant_page":
            pages_passed+=1
    csvfile.close()
    print("Done: "+lang)
    print("Percentage pages outside user threshold: " + str(pages_passed/pages_total))
    return

# Can create another function that loops over all files
def main():
    # Get data file
    os.chdir(".."); os.chdir("data/")
    file_list=os.listdir("raw_data")
    for file in file_list:
        if file.endswith('.csv'):
            lang=re.search(r'_[^_]*\.',file).group()[1:-1]
            file_iter = pd.read_csv("raw_data/"+file).itertuples()
            process_file(file_iter,lang)
    return
    

if __name__ == "__main__":
    main()
