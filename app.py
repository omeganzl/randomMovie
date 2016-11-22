import requests
from flask import Flask, render_template, request, url_for
import findMovie
from rq import Queue
from rq.job import Job
from worker import conn

app = Flask(__name__)
q = Queue(connection=conn)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/search')
def search():
    rating = request.args.get('minRating')
    movie = findMovie.findMovie(rating)
    if movie is not None:
        title = movie['Title']
        year = movie['Year']
        plot = movie['Plot']
        if movie['Poster'] != "N/A":
            poster = movie['Poster']
        else:
            poster = url_for('static/img', filename='noPoster.jpg')
        url = 'http://imdb.com/title/' + movie['imdbID']
        return render_template('search.html', title=title, year=year, plot=plot, poster=poster, url=url)
    else:
        return render_template('error.html', error="Unable to access OMDB. Please try again later")


if __name__ == '__main__':
    app.run()
    
