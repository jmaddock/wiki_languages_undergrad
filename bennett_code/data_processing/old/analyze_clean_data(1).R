data_directory = '/Users/Bennett/OneDrive/Northwestern/Research/Wiki_Project/data/cleaned_data'
file_list=list.files(path=data_directory,pattern='*.csv')

# Initialize Vectors
lang=c()
num_pages=c()
users_page=c()
subs_page=c()
exchanges_page=c()

for (file in file_list) {
  print(file)
  #Calculate new values
  file_data=read.csv(paste(data_directory,file,sep='/'))
  new_lang=file
  new_num_pages=nrow(file_data)
  new_users_page=mean(file_data$num_sigs)
  new_subs_page=mean(file_data$num_subs)
  new_exchanges_page=mean(file_data$exchanges)
  
  #Add to vectors
  lang=append(lang,new_lang)
  num_pages=append(num_pages,new_num_pages)
  users_page=append(users_page,new_users_page)
  subs_page=append(subs_page,new_subs_page)
  exchanges_page=append(exchanges_page,new_exchanges_page)
}

cleaned_data=data.frame(file=lang,num_pages,users_page,subs_page,exchanges_page)
