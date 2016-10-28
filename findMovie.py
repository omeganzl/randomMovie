import random, json, requests


def findMovie(minRating):

    minRating = float(minRating)
    maxRating = 10.0
    genre = ""
    mid = int((random.random() * 2155529) + 1)  # generate a random movie id
    title = 'tt' + str(mid).zfill(7)  # convert to imdb ID, tt + 7 digits
    try:
        url = 'http://www.omdbapi.com/?i=' + title + '&plot=short&r=json'
        response = requests.get(url)
        response.raise_for_status()

        movieData = json.loads(response.text)
        movieRating = 0
        movieLanguage = movieData['Language'].split(',')
        movieGenre = movieData['Genre'].lower()

        if movieData['Type'].lower() == 'movie':
            if movieLanguage[0] == 'English':
                if 'documentary' not in movieGenre and 'short' not in movieGenre:
                    if int(movieData['Year']) > 1980:
                        if movieData['imdbRating'] != 'N/A' and movieData['Plot'] != 'N/A':
                            movieRating = float(movieData['imdbRating'])
                            if movieRating > minRating:
                                return movieData
                            else:
                                print("Chosen Movie rating is out of range. Trying again\n")
                                return findMovie(minRating)
                        else:
                            print("Movie has no rating or plot! Trying again")
                            return findMovie(minRating)
                    else:
                        print('Chosen movie is too old! Trying again\n')
                        return findMovie(minRating)
                else:
                    print("Didn't find a movie. Trying again")
                    return findMovie(minRating)
            else:
                print('Whoops, that\'s not English! Trying again\n')
                return findMovie(minRating)
        else:
            print("Didn't find a movie. Trying again")
            return findMovie(minRating)

    except KeyError:
        print('Movie didn\'t contain a rating, trying again!')
        return findMovie(minRating)

    except ConnectionError as error:
        print(error)
        print('Unable to acces OMDB! Check your internet connection')
        return None


