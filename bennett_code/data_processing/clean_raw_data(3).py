import pandas as pd, os, csv, re

class subheading_class:
    def __init__(self,curr_row):
        
        #Public
        self.page_id=curr_row.page_id
        self.sub_index=1
        self.posts=0
        self.max_depth=0
        self.authors=0
        
        # Private
        self.depth_list=[0]
        self.authors_set=set(["None"])

    def update(self,curr_row):
        self.posts+=1
        self.depth_list.append(curr_row.indentation_depth)
        self.authors_set.add(curr_row.user_text)
        
    def output(self):
        page_id=self.page_id
        sub_index=self.sub_index
        posts=self.posts
        max_depth=max(self.depth_list)
        authors=len(self.authors_set)-1
        output_list=[page_id,sub_index,posts,max_depth,authors]
        return output_list
        
def process_subheading(curr_row,file_iter):
    # Initialize variables
    flag=False
    sub_name=curr_row.subheading_title
    # if it doesnt exist skip
    while sub_name!=curr_row.subheading_title:
        curr_row=next(file_iter)
        sub_name=curr_row.subheading_title
    processed_sub=subheading_class(curr_row)
    # Process entire subheading
    while sub_name==curr_row.subheading_title:
        processed_sub.update(curr_row)
        try:
            curr_row=next(file_iter)
        except StopIteration:
            flag=True
            break

    return [processed_sub.output(),curr_row,flag]


def process_file(file_iter,lang):
    #Initialize csvwriter for output
    csvfile=open('cleaned_data/'+lang+'_output.csv','w')
    output_writer=csv.writer(csvfile)
    output_writer.writerow(('page_id','sub_index','posts','max_depth','authors'))
    # Add a new row for every subheading
    curr_row=next(file_iter)
    while True:
        [subheading_output,curr_row,flag] = process_subheading(curr_row,file_iter)
        if flag:
            break;
        output_writer.writerow(subheading_output)
    print("Done: "+lang)
    csvfile.close()
    return


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
    
if __name__=="__main__":
    page=main()
