# -*- coding: utf-8 -*-
"""Loan_defaulter_prediction_using_keras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_dsodxHx3p9tyRg_ltvTKkInVDi7Gl2a
"""

#mount google drive

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
#import the required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

#read the dataset

df = pd.read_csv('/content/drive/MyDrive/Dataset Files/lending_club_loan_two.csv')
df.head()

"""#Data Overview

----
-----
There are many LendingClub data sets on Kaggle. Here is the information on this particular data set:

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>LoanStatNew</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>loan_amnt</td>
      <td>The listed amount of the loan applied for by the borrower. If at some point in time, the credit department reduces the loan amount, then it will be reflected in this value.</td>
    </tr>
    <tr>
      <th>1</th>
      <td>term</td>
      <td>The number of payments on the loan. Values are in months and can be either 36 or 60.</td>
    </tr>
    <tr>
      <th>2</th>
      <td>int_rate</td>
      <td>Interest Rate on the loan</td>
    </tr>
    <tr>
      <th>3</th>
      <td>installment</td>
      <td>The monthly payment owed by the borrower if the loan originates.</td>
    </tr>
    <tr>
      <th>4</th>
      <td>grade</td>
      <td>LC assigned loan grade</td>
    </tr>
    <tr>
      <th>5</th>
      <td>sub_grade</td>
      <td>LC assigned loan subgrade</td>
    </tr>
    <tr>
      <th>6</th>
      <td>emp_title</td>
      <td>The job title supplied by the Borrower when applying for the loan.*</td>
    </tr>
    <tr>
      <th>7</th>
      <td>emp_length</td>
      <td>Employment length in years. Possible values are between 0 and 10 where 0 means less than one year and 10 means ten or more years.</td>
    </tr>
    <tr>
      <th>8</th>
      <td>home_ownership</td>
      <td>The home ownership status provided by the borrower during registration??or obtained from the credit report.??Our values are: RENT, OWN, MORTGAGE, OTHER</td>
    </tr>
    <tr>
      <th>9</th>
      <td>annual_inc</td>
      <td>The self-reported annual income provided by the borrower during registration.</td>
    </tr>
    <tr>
      <th>10</th>
      <td>verification_status</td>
      <td>Indicates if income was verified by LC, not verified, or if the income source was verified</td>
    </tr>
    <tr>
      <th>11</th>
      <td>issue_d</td>
      <td>The month which the loan was funded</td>
    </tr>
    <tr>
      <th>12</th>
      <td>loan_status</td>
      <td>Current status of the loan</td>
    </tr>
    <tr>
      <th>13</th>
      <td>purpose</td>
      <td>A category provided by the borrower for the loan request.</td>
    </tr>
    <tr>
      <th>14</th>
      <td>title</td>
      <td>The loan title provided by the borrower</td>
    </tr>
    <tr>
      <th>15</th>
      <td>zip_code</td>
      <td>The first 3 numbers of the zip code provided by the borrower in the loan application.</td>
    </tr>
    <tr>
      <th>16</th>
      <td>addr_state</td>
      <td>The state provided by the borrower in the loan application</td>
    </tr>
    <tr>
      <th>17</th>
      <td>dti</td>
      <td>A ratio calculated using the borrower???s total monthly debt payments on the total debt obligations, excluding mortgage and the requested LC loan, divided by the borrower???s self-reported monthly income.</td>
    </tr>
    <tr>
      <th>18</th>
      <td>earliest_cr_line</td>
      <td>The month the borrower's earliest reported credit line was opened</td>
    </tr>
    <tr>
      <th>19</th>
      <td>open_acc</td>
      <td>The number of open credit lines in the borrower's credit file.</td>
    </tr>
    <tr>
      <th>20</th>
      <td>pub_rec</td>
      <td>Number of derogatory public records</td>
    </tr>
    <tr>
      <th>21</th>
      <td>revol_bal</td>
      <td>Total credit revolving balance</td>
    </tr>
    <tr>
      <th>22</th>
      <td>revol_util</td>
      <td>Revolving line utilization rate, or the amount of credit the borrower is using relative to all available revolving credit.</td>
    </tr>
    <tr>
      <th>23</th>
      <td>total_acc</td>
      <td>The total number of credit lines currently in the borrower's credit file</td>
    </tr>
    <tr>
      <th>24</th>
      <td>initial_list_status</td>
      <td>The initial listing status of the loan. Possible values are ??? W, F</td>
    </tr>
    <tr>
      <th>25</th>
      <td>application_type</td>
      <td>Indicates whether the loan is an individual application or a joint application with two co-borrowers</td>
    </tr>
    <tr>
      <th>26</th>
      <td>mort_acc</td>
      <td>Number of mortgage accounts.</td>
    </tr>
    <tr>
      <th>27</th>
      <td>pub_rec_bankruptcies</td>
      <td>Number of public record bankruptcies</td>
    </tr>
  </tbody>
</table>

---
----

The loan_status column is the target column

##Exploratory Data Analysis

Check info of the dataset
"""

df.info()

"""We can observe that there are 27 columns and 396030 rows in the dataset.

The dataset contains mixed data types and we can observe that there are missing values in the data.

check the summary statistics for numerical columns
"""

df.describe()

"""Visualize countplot for the target column (Loan_status)"""

sns.countplot(x=df['loan_status'])
plt.show()

"""We can observe that there is class imbalance for the target column. Most people have fully paid back their loan while others have been charged off"""

#Check the histogram of loan_amt column

sns.histplot(data=df['loan_amnt'])

"""Looking at the distribution of the loan_amnt column, it looks to be fairly normal.

The loan_amnt is ranging from 5000 to 35000 dollars.
"""

#Check the correlation between numerical variables using heatmap

plt.figure(figsize=(15,8))
sns.heatmap(df.corr(), annot=True)
plt.tight_layout()
plt.show()

"""We can observe almost perfect linear relationship between loan amount and installment columns. (0.95)

This makes sense as larger the loan amount, the more the installments would be.
"""

#draw scatter plot between loan amount and installment

sns.scatterplot(x=df['loan_amnt'], y=df['installment'])

#boxplot checking relation between loan status and loan amount

sns.boxplot(x=df['loan_status'], y=df['loan_amnt'])

"""We can observe that the loan amount distribution is almost similar for both the groups"""

df.groupby('loan_status')['loan_amnt'].describe()

#let us have a look at the countplot for grade column with hue as loan_status

sns.countplot(x=df['grade'], hue=df['loan_status'])

"""We can observe that grade B contains more no of people who have fully paid their loan whereas grade C contains more no of people who have been charged off

Countplot of subgrade with hue as loan_status
"""

plt.figure(figsize=(15,4))
subgrade_order = sorted(df['sub_grade'].unique())
sns.countplot(x=df['sub_grade'], hue=df['loan_status'], order=subgrade_order, palette='coolwarm')
plt.tight_layout()

"""It seems F and G sub-grades dont get paid back their loan often.

Feature engineering the loan status column
"""

df['loan_status'].value_counts()

df['loan_status'] =  df['loan_status'].map({"Fully Paid":1, "Charged Off":0})

df['loan_status'].value_counts()

"""Bar plot to show the correlation between new loan status column and other numerical features"""

df.corr()['loan_status'].sort_values().drop('loan_status').plot(kind='bar')

"""We can observe that mort_acc has a high positive correlation with loan status column

# Data PreProcessing

### Missing values
"""

#count the missing values
df.isnull().sum()

#percentage of missing values in each column
df.isnull().sum() / len(df)

"""We can see that some columns have missing values.

Let us have a look at each one of them individually.
"""

#emp_title

df['emp_title'].value_counts()

df['emp_title'].nunique()

"""There are 173105 unique entries in this column. We will drop this column"""

df.head()

df.drop('emp_title', axis=1, inplace=True)
df.head()

#emp_length

df['emp_length'].value_counts()

df['emp_length'].dtypes

#let us check the relationship of emp_length vs loan_status

emp_co = df[df['loan_status'] == 0].groupby('emp_length').count()['loan_status']
emp_co

emp_fp = df[df['loan_status'] == 1].groupby('emp_length').count()['loan_status']
emp_fp

#calculate percentage of people per employment category who didn't pay back their loan
emp_len = emp_co / emp_fp
emp_len

#plot the bar graph
emp_len.plot(kind='bar')

"""Charge off rates are extremely similar across all employment lengths.
Therefore, we can drop the emp_length column
"""

df.drop('emp_length', axis=1, inplace=True)
df.head()

df.isnull().sum()

#title

df['title'].value_counts()

df['title'].head()

df['purpose'].head()

"""Title and purpose seem to be related. Therefore, we can drop the title column"""

df.drop('title', axis=1, inplace=True)
df.head()

df.isnull().sum()

#revol_util

df['revol_util'].describe()

df['revol_util']

"""We can fill the missing values in this column by the mean value as both mean and median values lie close to each other as per the summary statistics"""

df['revol_util']  = df['revol_util'].fillna(df['revol_util'].median())

df.isnull().sum()

#mort_acc

df['mort_acc'].describe()

df['mort_acc'].value_counts()

print("Correlation with the mort_acc column")
df.corr()['mort_acc'].sort_values()

"""We can observe that total_acc is more closely correlated with mort_acc

We will group the dataframe by the total_acc and calculate the mean value for the mort_acc per total_acc entry.
"""

print("Mean of mort_acc column per total_acc")
df.groupby('total_acc').mean()['mort_acc']

"""Fill in the missing mort_acc values based on their total_acc value. If the mort_acc is missing, then we will fill in that missing value with the mean value corresponding to its total_acc value from the Series we created above. """

total_acc_avg = df.groupby('total_acc').mean()['mort_acc']

def fill_mort_acc(total_acc,mort_acc):
    '''
    Accepts the total_acc and mort_acc values for the row.
    Checks if the mort_acc is NaN , if so, it returns the avg mort_acc value
    for the corresponding total_acc value for that row.
    
    total_acc_avg here should be a Series or dictionary containing the mapping of the
    groupby averages of mort_acc per total_acc values.
    '''
    if np.isnan(mort_acc):
        return total_acc_avg[total_acc]
    else:
        return mort_acc

df['mort_acc'] = df.apply(lambda x: fill_mort_acc(x['total_acc'], x['mort_acc']), axis=1)

#check the missing values
df.isnull().sum()

df['pub_rec_bankruptcies'].value_counts()

"""Fill in the missing values by the most occuring value i.e. 0"""

df['pub_rec_bankruptcies'] = df['pub_rec_bankruptcies'].fillna(0.0)

#check the missing values in the dataset
df.isnull().sum()

"""We have handled all the missing values

#### Handling Categorical variables
"""

df.select_dtypes('object').columns

#term

df['term'].value_counts()

df['term'][0]

"""convert term into 36 and 60 int type using map"""

df['term'] = df['term'].map({' 36 months':36, ' 60 months':60})

#check the size
df['term'].value_counts()

"""####sub-grade

We know that subgrade is a part of grade. So we drop this feature
"""

df.drop('sub_grade', axis=1, inplace=True)
df.head(1)

#grade

#convert the grade into dummy variables

dummies = pd.get_dummies(df['grade'],drop_first=True)

df = pd.concat([df.drop('grade',axis=1),dummies],axis=1)

df.columns

#verification_status, application_type,initial_list_status,purpose

#convert these columns into dummy variables and concatenate with the original dataframe

dummies = pd.get_dummies(df[['verification_status', 'application_type','initial_list_status','purpose' ]],drop_first=True)
df = df.drop(['verification_status', 'application_type','initial_list_status','purpose'],axis=1)
df = pd.concat([df,dummies],axis=1)

#home ownership

#check the size
df['home_ownership'].value_counts()

"""We will replace any and None with Other and convert this column to dummy variables as we have done before"""

df['home_ownership']=df['home_ownership'].replace(['NONE', 'ANY'], 'OTHER')

home_dummies = pd.get_dummies(df['home_ownership'],drop_first=True)
df = df.drop('home_ownership',axis=1)
df = pd.concat([df,home_dummies],axis=1)

#address

df.head(1)

"""Let's feature engineer a zip code column from the address in the data set by creating a new column 'zip_code'"""

df['zip_code'] = df['address'].apply(lambda address:address[-5:])

"""convert the newly created zip_code column into dummy variables"""

zip_dummies = pd.get_dummies(df['zip_code'],drop_first=True)
df = df.drop(['zip_code','address'],axis=1)
df = pd.concat([df,zip_dummies],axis=1)

df.head(1)

#issue_d

"""This would be data leakage, we wouldn't know beforehand whether or not a loan would be issued when using our model, so in theory we wouldn't have an issue_date, so we drop this feature."""

df = df.drop('issue_d',axis=1)

#earliest_cr_line
df['earliest_cr_line']

"""We can extract the year from this column to get the borrower's earliest credit line year and create a new column called **earliest_cr_line_yr**"""

df['earliest_cr_year'] = df['earliest_cr_line'].apply(lambda date:int(date[-4:]))
df = df.drop('earliest_cr_line',axis=1)

df['loan_status'].dtypes

df.head()

"""We have handled all the categorical variables now.

### Train Test Split
"""

#import train test split
from sklearn.model_selection import train_test_split

X = df.drop('loan_status', axis=1).values
y = df['loan_status'].values

"""Perform a train test split with test size as 0.2"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=101)

X_train.shape, X_test.shape

y_train.shape, y_test.shape

"""### Scaling the input data"""

#using standard scaler

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

#scale the input training data
X_train = scaler.fit_transform(X_train)

#scale the input testing data
X_test = scaler.transform(X_test)

#In order to prevent data leakage, we only transform the input test data

"""## Creating the model"""

#import the necessary keras functions
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.constraints import max_norm

#instantiate the model

model = Sequential()

#input layer
model.add(Dense(50, activation='relu'))
model.add(Dropout(0.2))

# hidden layer
model.add(Dense(30, activation='relu'))
model.add(Dropout(0.2))

# hidden layer
model.add(Dense(15, activation='relu'))
model.add(Dropout(0.2))

#output layer
model.add(Dense(units=1, activation='sigmoid'))


#compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics='accuracy')  
#since binary classification so binary_crossentropy

#fit the model

model.fit(x=X_train, 
          y=y_train, 
          epochs=25,
          batch_size=256,
          validation_data=(X_test, y_test)
          )

"""## Evaluating Model Performance"""

#plot the validation loss vs training loss

losses = pd.DataFrame(model.history.history)
losses[['loss','val_loss']].plot()

"""Predict on the test set"""

from sklearn.metrics import classification_report,confusion_matrix

predictions = model.predict(X_test)
predictions = np.round(predictions).astype(int)

print(classification_report(y_test, predictions))

confusion_matrix(y_test,predictions)

"""Given the customer below, would we offer this person a loan?"""

import random
random.seed(101)
random_ind = random.randint(0,len(df))

new_customer = df.drop('loan_status',axis=1).iloc[random_ind]
new_customer

new_customer = scaler.transform(new_customer.values.reshape(1,50))
new_customer

model.predict(new_customer)

#validate with original column
df.iloc[random_ind]['loan_status']

#save the model

from tensorflow.keras.models import load_model
model.save('loan_model.h5')



