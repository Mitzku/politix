import sqlite3
from matplotlib import pyplot as plt
import io
import urllib
import base64

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_vote_data(bundestags_id, abstimmungsverhalten):
    conn = get_db_connection()
    query = f"WITH abs AS (SELECT * FROM df_abstimmungen_selenium WHERE bundestags_id = {bundestags_id}), pol AS (SELECT * FROM df_politiker_selenium WHERE bundestags_id = {bundestags_id}), alldata AS (SELECT * FROM abs LEFT JOIN pol ON abs.bundestags_id = pol.bundestags_id) SELECT DISTINCT * FROM alldata WHERE Abstimmungsverhalten = '{abstimmungsverhalten}'"
    data = conn.execute(query).fetchall()
    conn.close()
    return data

def generate_pie_chart(df):
    df = df.groupby('Abstimmungsverhalten').size().reset_index(name='count')
    colors = ['#ffc107', '#28a745', '#dc3545', '#6c757d']
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
    ax.pie(df['count'], labels=df['Abstimmungsverhalten'], autopct='%1.1f%%', startangle=90, wedgeprops={'linewidth': 3, 'edgecolor': 'k', 'antialiased': True}, textprops={'fontsize': 18}, colors=colors)

    fig.set_facecolor('#ffc107')
    ax.set_title('Abstimmungsverhalten', fontsize=24, fontweight='bold')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode())

    return plot_data

def get_politician_info(bundestags_id):
    conn = get_db_connection()
    query = f"WITH abs AS (SELECT * FROM df_abstimmungen_selenium WHERE bundestags_id = {bundestags_id}), pol AS (SELECT * FROM df_politiker_selenium WHERE bundestags_id = {bundestags_id}) SELECT * FROM abs LEFT JOIN pol ON abs.bundestags_id = pol.bundestags_id"
    data = conn.execute(query).fetchall()
    return data