# Set directory path
setwd(getSrcDirectory(function(x) {x}))
setwd("..")

data_directory = paste(getwd(),"data/cleaned_data",sep="/")
graphics_directory = paste(getwd(),"data/graphics",sep="/")
file_list=list.files(path=data_directory,pattern='*.csv')
file_data=read.csv(paste(data_directory,file_list[1],sep='/'))
var_list=colnames(file_data)[2:length(colnames(file_data))]
par(mar=c(1,1,1,1))
old.par <- par(mfrow=c(4,6))

for (var in var_list) {
  print(var)
  for (file in file_list) {
    lang=substr(file,1,nchar(file)-11)
    file_data=read.csv(paste(data_directory,file,sep='/'))
    hist(file_data[,var],main=NULL,xlab=lang)
  }
  dev.print(pdf,paste(graphics_directory,"/",var,".pdf",sep=""))
  
}
par(old.par)
