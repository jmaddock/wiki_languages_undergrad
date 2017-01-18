import csv; import pandas

#Defining user name for each edit
data=pandas.read_csv('/Users/Bennett/Desktop/Wiki_Data/raw_data/combined_raw_edits.csv')
del data['Unnamed: 0']
user=data.user_text

#Defining list of bot users
bot_list=pandas.read_csv('/Users/Bennett/Desktop/Wiki_Data/raw_data/bot_list.csv', header=None)
bot_list=bot_list.values.tolist()
bot_list=[i[0] for i in bot_list]

#Create boolean list and append to csv file
bot_bool=pandas.DataFrame(user.isin(bot_list))
bot_bool.columns.values[0]='is_bot'
final_data=pandas.concat([data,bot_bool], axis=1)

#export csv file
final_data.to_csv('/Users/Bennett/Desktop/Wiki_Data/raw_data/bot_test_processed.csv')




        
    
          
