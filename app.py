from flask import Flask, render_template, request, redirect, url_for
from src.database import get_db_connection, create_table, fetch_latest_clicks, insert_click_data
from src.thompson_sampling import ThompsonSampling

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

# Veritabanı ve Thompson Sampling yapılandırması
create_table()
thompson_sampling = ThompsonSampling(n_ads=10)

@app.route('/')
def index():
    ad = thompson_sampling.select_ad()
    return render_template('index.html', ad=ad)

@app.route('/click', methods=['POST'])
def click():
    ad_id = int(request.form['ad_id'])
    clicked = request.form['clicked'] == '1'
    user_id = 1  # Varsayılan kullanıcı kimliği

    with get_db_connection() as conn:
        insert_click_data(conn, ad_id, user_id, clicked)
        latest_clicks = fetch_latest_clicks(conn)
        for click in latest_clicks:
            thompson_sampling.update(click[0], click[1])

    return redirect(url_for('index'))

@app.route('/results')
def results():
    ads_selected = []
    with get_db_connection() as conn:
        latest_clicks = fetch_latest_clicks(conn, limit=1000)  # Görselleştirme için son 1000 tıklamayı alıyoruz

    for click in latest_clicks:
        ad_id = click[0]
        ads_selected.append(ad_id)

    plt.hist(ads_selected, bins=range(11), edgecolor='black')
    plt.title('Histogram of Ad Selections')
    plt.xlabel('Ad ID')
    plt.ylabel('Number of times each ad was selected')
    plt.savefig('static/histogram.png')  # Görseli static klasörüne kaydediyoruz
    plt.close()

    return '<img src="/static/histogram.png" alt="Histogram of Ad Selections">'

if __name__ == '__main__':
    app.run(debug=True)
