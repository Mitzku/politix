import sqlite3
import pandas as pd

conn = sqlite3.connect('database.db')

df_politiker_selenium = pd.read_csv('df_politiker_selenium_2023-03-02_13-01-20.csv')
df_politiker_selenium.to_sql('df_politiker_selenium', conn, if_exists='replace', index=False)

df_abstimmungen_selenium = pd.read_csv('df_abstimmungen_selenium_2023-03-02_13-01-13.csv')
df_abstimmungen_selenium.to_sql('df_abstimmungen_selenium', conn, if_exists='replace', index=False)

conn.commit()
conn.close()