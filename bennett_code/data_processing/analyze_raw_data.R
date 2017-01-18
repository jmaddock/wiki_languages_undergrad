data_directory = '/Users/Bennett/OneDrive/Northwestern/Research/Wiki_Project/data/raw_data'
file_list=list.files(path=data_directory,pattern='*.csv')

# Initialize Vectors
lang=c()
size=c()
unsigned_sub=c()
mean_depth=c()
median_sub_length=c()

for (file in file_list) {
  print(file)
  #Calculate new values
  file_data = read.csv(paste(data_directory,file,sep='/'))
  new_lang = file
  new_size = nrow(file_data)
  new_unsigned_sub = sum(file_data$user_text=='None' & file_data$subheading_title!='Top_Subtitle')/new_size
  new_mean_depth = mean(file_data$indentation_depth)
  new_median_sub_length = median(file_data$subheading_line)
  
  #Add to vectors
  lang = append(lang,new_lang)
  size = append(size,new_size)
  unsigned_sub = append(unsigned_sub,new_unsigned_sub)
  mean_depth = append(mean_depth,new_mean_depth)
  median_sub_length = append(median_sub_length,new_median_sub_length)
}

raw_data=data.frame(file=lang,size,unsigned_sub,mean_depth,median_sub_length)