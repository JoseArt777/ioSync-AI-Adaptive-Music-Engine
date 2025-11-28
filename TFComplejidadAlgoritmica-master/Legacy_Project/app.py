from flask import Flask, render_template, url_for, request, redirect
import DLS
import pandas as pd
import generate_weights
import requests

formData = {}

app = Flask(__name__)

generate_weights.generar_csvs()
df_movies = pd.read_csv('Amdb_5000_movies.csv')
movie_dataset = df_movies['original_title'].astype(str).tolist()
movie_dataset_minusculas = [x.lower() for x in movie_dataset]

#para los posters
df_posters = pd.read_csv('pmdb_5000_movies.csv')

movie_name = df_posters['original_title'].astype(str).tolist()
id_dataset = df_posters['id'].astype(int).tolist()

movie_name_minusculas = [x.lower() for x in movie_name]

posters = dict(zip(movie_name_minusculas, id_dataset))

def get_poster(movie_id_list):
    full_path = []
    for movie_id in movie_id_list:
        try:
            url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
            data = requests.get(url)
            data = data.json()
            poster_path = data['poster_path']
            full_path.append("https://image.tmdb.org/t/p/w500/" + poster_path)
        except:
            print("Error, movie poster not found")
            full_path.append("https://pbs.twimg.com/media/FyOunJ_WYAAXBwX?format=jpg&name=small")
    return full_path

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        formData['movieReference'] = request.form['movieref']
        formData['movieSelectedFilter'] = request.form['check']
        formData['movieRecommendationAmount'] = int(request.form['recamount'])
        return redirect(url_for('output'))
    
    else:
        return render_template('index.html')

@app.route('/output')
def output():
    movie_minus = formData['movieReference']
    movie_minus = movie_minus.lower()
    result = DLS.filter_selector(movie_minus, formData['movieSelectedFilter'], formData['movieRecommendationAmount'], movie_dataset_minusculas)
    movie_id_list = []
    if result[0] != "Error, movie not found in the dataset":
        for movie_name in result:
            movie_id_list.append(posters[movie_name])
        poster = get_poster(movie_id_list)
    else:
        poster = ["https://pbs.twimg.com/media/FyOunJ_WYAAXBwX?format=jpg&name=small"]

    return render_template('output.html', movieRefName = formData['movieReference'], 
                            movieFilter = formData['movieSelectedFilter'],
                            movieRecAmount = formData['movieRecommendationAmount'],
                            recommendation_list = result, poster_list = poster)

@app.route('/algorithm')
def algorithm():
    return render_template('algorithm.html')

if __name__ == '__main__':
    app.run(debug=True)

#flask --app app.py --debug run