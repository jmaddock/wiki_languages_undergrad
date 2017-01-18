
process_subheading<-function(file_data,index,data_vectors) {
  return (data_vectors)
}

# Process each lang
process_page<-function(file_data,index,data_vectors) {
  page_id = file_data$page_id[index]
  sub_title = file_data$subheading_title[index]
  max_depth = 0
  while (file_data$page_id[index]==page_id & index<nrow(file_data)) {
    if (file_data$indentation_depth[index]>max_depth) {
      max_depth = file_data$indentation_depth[index]
    }
    index=index+1
  }
  
  append(data_vectors[page_id],page_id)
  append(data_vectors[max_depth],max_depth)
  output = c(index,data_vectors)
  
  return (output)
}

# Start program
main<-function() {
  data_directory = '/Users/Bennett/OneDrive/Northwestern/Research/Wiki_Project/parsed_dumps'
  file_list=list.files(path=data_directory,pattern='*.csv')
  for (file in file_list[5]) {
    print(file)
    file_data <- read.csv(paste(data_directory,file,sep="/"))
    index = 1
    page_id = 0
    # Define data to gather
    data_vectors <- c(page_id = c(), max_depth = c(), num_users = c(), num_sub = c())
    while (index<nrow(file_data)) {
      if (file_data$page_id[index]==page_id) {
      process_page_output =  process_page(file_data,index,data_vectors)
      index = process_page_output[1]
      data_vectors = process_page_output[2]
      }
      else {
        page_id = file_data$page_id[index]
      }
   }
  }
  return(data_vectors)
}

df_out = main()