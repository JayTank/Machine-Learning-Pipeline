import pandas as pd
import psycopg2 as pg
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB

dbname = "postgres"
nisdb = "nis_database"
user = "postgres"
host = "localhost"
password = "Qwerty@94"

connection = pg.connect(dbname=nisdb, user=user, host=host, password=password)

dataframe_2013_pos = pd.read_sql_query('SELECT age, female, race, dx1, dx2, dx3, dx4, dx5, dx6, dx7, dx8, '
                                       'dx9, dx10, dx11, dx12, dx13, dx14, dx15, dx16, dx17, dx18, dx19, dx20, '
                                       'dx21, dx22, dx23, dx24, dx25, status FROM nis_2013_core WHERE status = 1', connection)
dataframe_2013_neg = pd.read_sql_query('SELECT age, female, race, dx1, dx2, dx3, dx4, dx5, dx6, dx7, dx8, '
                                       'dx9, dx10, dx11, dx12, dx13, dx14, dx15, dx16, dx17, dx18, dx19, dx20, '
                                       'dx21, dx22, dx23, dx24, dx25, status FROM nis_2013_core WHERE status = 0 LIMIT 50000', connection)

for index, row in dataframe_2013_pos.iterrows():
    for i in range(1, 26):
        d = 'dx' + str(i)
        if row[d].startswith('174'):
            dataframe_2013_pos.at[index, d] = '0'

vertical_stack = pd.concat([dataframe_2013_pos, dataframe_2013_neg])

for index, row in vertical_stack.iterrows():
    for i in range(1, 26):
        d = 'dx' + str(i)
        if row[d] == '':
            vertical_stack.at[index, d] = '0'
        if row[d].startswith('V'):
            vertical_stack.at[index, d] = row[d].replace('V', '')
        if row[d] == 'invl':
            vertical_stack.at[index, d] = '0'
        if row[d] == 'incn':
            vertical_stack.at[index, d] = '0'


vertical_stack = vertical_stack.sample(frac=1)
#vertical_stack.to_csv('file_name.csv')
X = vertical_stack.drop(columns='status')

Y = vertical_stack['status']

print(X.shape)
print(Y.shape)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

gnb = GaussianNB()
gnb = gnb.fit(X_train, Y_train)
y_pred = gnb.predict(X_test)
score = accuracy_score(Y_test, y_pred)
print("Accuracy:", score*100, "%")
cm = confusion_matrix(Y_test, y_pred)
print(cm)

