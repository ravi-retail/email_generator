'''
import pandas as pd and create dataframe using dictionary and print the head
'''

import pandas as pd

data = {'Students':['Tom','nick','krish','jack'],
        'Age':[20,21,19,18], 
        'Class': [2,2,3,4], 
        'Subjects': ['English,Hindi', 'Telugu, English', 'Hindi,Telugu', 'English, Spanish']}

'''
as data as pandas dataframe,
'''

df = pd.DataFrame(data)

'''
prepare rows to have ever subject in individual rows, 
subjects are separated by ','
prepare every row with only one subject name

'''




df['Subjects'] = df['Subjects'].str.split(',')

'''
prepare the dataframe with every row with only one subject name
by preparing a new row for every subject name
'''


df = df.explode('Subjects') 

'''
select only students and subjects columns
'''


df = df[['Students','Subjects']]

'''
group student names values into one row , based on the subject name'''

df = df.groupby(['Students','Subjects']).size().reset_index(name='Count')

print(df)