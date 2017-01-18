data_directory = '/Users/Bennett/OneDrive/Northwestern/Research/Wiki_Project/data/cleaned_data'
file_list=list.files(path=data_directory,pattern='*.csv')

# Initialize Vectors
lang=c()
subheadings=c()
posts=c()
max_depth=c()
authors=c()

for (file in file_list) {
  print(file)
  #Calculate new values
  file_data=read.csv(paste(data_directory,file,sep='/'))
  new_lang=file
  new_subheadings=nrow(file_data)
  new_posts=mean(file_data$posts)
  new_max_depth=mean(file_data$max_depth)
  new_authors=mean(file_data$authors)
  
  #Add to vectors
  lang=append(lang,new_lang)
  subheadings=append(subheadings,new_subheadings)
  posts=append(posts,new_posts)
  max_depth=append(max_depth,new_max_depth)
  authors=append(authors,new_authors)
}

cleaned_data=data.frame(file=lang,subheadings,posts,max_depth,authors)