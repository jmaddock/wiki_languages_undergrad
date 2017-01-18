import pandas as pd, os, csv, numpy as np, re

class page_class:
    def __init__(self,page_id):
        
        #Public
        self.page_id=page_id
        self.num_subs=1
        self.posts_sub=0
        self.max_depth=0
        self.users_sub=0
        
        # Private
        self.posts_sub_list=[]
        self.max_depth_list=[]
        self.users_sub_list=[]

    def sub_count(self):
        self.num_subs+=1
        
    def append_sub_data(self,user_list,depth_list):
        while "None" in user_list: user_list.remove("None")
        self.posts_sub_list.append(len(user_list))
        self.users_sub_list.append(len(set(user_list)))
        try:
            self.max_depth_list.append(max(depth_list))
        except ValueError:
            self.max_depth_list.append(0)
    
    def output(self):
        page_id=self.page_id
        num_subs=self.num_subs
        posts_sub=list_stats(self.posts_sub_list)
        max_depth=list_stats(self.max_depth_list)
        users_sub=list_stats(self.users_sub_list)
        nested_output=[page_id,num_subs,posts_sub,max_depth,users_sub]
        output_list=[]
        for element in nested_output:
            if type(element)==list:
                output_list.extend(element)
            else:
                output_list.append(element)
        return output_list
        
# Page helper function
def list_stats(listIn):
        if listIn:
            list_mean=np.mean(listIn)
            list_median=np.median(listIn)
            list_min=min(listIn)
            list_max=max(listIn)
            return [list_mean,list_median,list_min,list_max]
        else:
            return [0,0,0,0]
        

def process_page(page):
    pageInfo=page_class(page[0])
    page_iter=page[1].itertuples()
    # Initialize variables
    user_list=[]
    depth_list=[]
    last_sub="Top_Subtitle"
    # Find subheading indices
    while True:
        try:
            page_row=next(page_iter)
            if last_sub!=page_row.subheading_title:
                pageInfo.sub_count()
                last_sub=page_row.subheading_title
                # Give subheading data to class object
                pageInfo.append_sub_data(user_list,depth_list)
                # Reset variables
                user_list=[]
                depth_list=[]
            user_list.append(page_row.user_text)
            depth_list.append(page_row.indentation_depth)
        except StopIteration:
            # Give last subheading data to class object
            pageInfo.append_sub_data(user_list,depth_list)
            break;
    return pageInfo.output()

   

def process_file(page_groupby,lang):
    global column_names
    #Initialize csvwriter for output
    csvfile=open('cleaned_data/'+lang+'_output.csv','w')
    output_writer=csv.writer(csvfile)
    output_writer.writerow(column_names(1,1))
    # Add a new row for every processed page
    for page in page_groupby:
        page_output = process_page(page)
        output_writer.writerow(page_output)
    csvfile.close()
    print("Done: "+lang)
    return page

# Defines column names for variables constant for a page or calculated
# statistically for a page
def column_names(fix_list,var_list):
    fix_list=['page_id','num_subs']
    var_list=['posts_sub','max_depth','users_sub']
    col_names=fix_list
    for name in var_list:
        col_names.extend([name+"_mn",name+"_md",name+"_min",name+"_max"])
    return col_names

def main():
    # Get data file
    os.chdir(".."); os.chdir("data/")
    file_list=os.listdir("raw_data")
    for file in file_list:
        if file.endswith('.csv'):
            lang=re.search(r'_[^_]*\.',file).group()[1:-1]
            page_groupby = pd.read_csv("raw_data/"+file).groupby("page_id")
            process_file(page_groupby,lang)
    return 
    
if __name__=="__main__":
    page=main()
