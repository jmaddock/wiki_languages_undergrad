import os; import pandas

#Creating empty dataframe
median_data = pandas.DataFrame(index=os.listdir('/Users/Bennett/Desktop/coding/'),columns=['Language','posts','unique_authors','depth','exchanges'], dtype='float')

#Loop through file paths, import csv, calculate median
for path in os.listdir('/Users/Bennett/Desktop/coding'):
    if path!='.DS_Store':
        data=pandas.read_csv(''.join(['/Users/Bennett/Desktop/coding/',path]))
        for col in ['posts','unique_authors','depth','exchanges']:
            median_data[col][path]=pandas.Series.median(data[col])
            print(pandas.Series.median(data[col]))
median_data.to_csv('/Users/Bennett/Desktop/example.csv')


                         
                         
    
    
