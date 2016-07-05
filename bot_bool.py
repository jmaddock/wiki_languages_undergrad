import csv; import pandas

#Defining user name for each edit
data=pandas.read_csv('/Users/Bennett/Desktop/Wiki_Data/bot_test_data.csv')
del data['Unnamed: 0']
user=data.user_text

#Defining list of bot users
bot_list=pandas.read_csv('/Users/Bennett/Desktop/Wiki_Data/bot_test_list.csv', header=None)
## JIM: you don't actually have to convert this to a list, so you can eliminate these lines
bot_list=bot_list.values.tolist()
## JIM: iterating through the whole list like this is slow
bot_list=[i[0] for i in bot_list]

#Create boolean list and append to csv file
## JIM: instead use bot_list[bot_list.columns[0]] to just the reference the series, that way you
## can skip the loop you made above
bot_bool=pandas.DataFrame(user.isin(bot_list))
bot_bool.columns.values[0]='is_bot'
final_data=pandas.concat([data,bot_bool], axis=1)

#export csv file
final_data.to_csv('/Users/Bennett/Desktop/Wiki_Data/bot_test_processed.csv')

## JIM: here's a shorter way if you're curious:
def flag_bots():
    df=pandas.read_csv('/Users/Bennett/Desktop/Wiki_Data/bot_test_data.csv')
    bot_list = pandas.read_csv('/Users/Bennett/Desktop/Wiki_Data/bot_test_list.csv')
    df['is_bot'] = df['user_text'].isin(bot_list[bot_list.columns[0]])
    return df





        
    
          
