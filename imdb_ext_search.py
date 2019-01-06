"""Module for extening the IMDB advanced title search by:
  - ordering by metascore
  - random choice of movies
"""

import argparse
import csv
import random
import sys

from bs4 import BeautifulSoup
import requests

def parse_args(args):
    """Parse input arguments.

    >>> parse_args(["abc", "--metascore", "0", "100"])
    Namespace(csv=None, metascore=[0, 100], random=None, sort=None, url='abc')
    >>> parse_args([])
    Traceback (most recent call last):
    ...
    SystemExit: 2
    """
    parser = argparse.ArgumentParser(description="IMDB")
    parser.add_argument("url", type=str, help="full url for imdb request")
    # TODO: Allow to add request parameters by passing a dict.
    #       This would be an alternative to provide the full url.
    parser.add_argument(
        "--metascore", type=int, nargs=2, metavar=("min", "max"),
        help="exclude movies with a metascore outside of this range")
    parser.add_argument(
        "--sort", type=str, choices=["asc", "desc"],
        help="sort list of movies ascending or descending")
    parser.add_argument(
        "--random", type=int,
        help="number of movies to be randomly picked out of the list")
    parser.add_argument(
        "--csv", type=str, help="export movie list to the csv file")
    return parser.parse_args(args)

def parse_html(html_code):
    """Parse raw html code and return a list of all movies contained.

    >>> parse_html("<html></html>")
    []
    """
    soup = BeautifulSoup(html_code, "html.parser")
    parsed_movies = soup.find_all("div", class_="lister-item mode-advanced")
    movies = []
    for movie in parsed_movies:
        name = movie.h3.a.text
        link = "https://www.imdb.com" + movie.h3.find("a")["href"]
        try:
            metascore = int(movie.find("span", class_="metascore").text)
        except AttributeError:
            metascore = None
        movies.append((name, metascore, link))
    return movies

def sort_movie_list(movies, reverse=False):
    """Sort movies based on the metascore.

    >>> sort_movie_list([])
    []
    >>> sort_movie_list([(7, 8, 9), (1, 2, 3), (4, None, 6)])
    [(4, None, 6), (1, 2, 3), (7, 8, 9)]
    """
    return sorted(
        movies, key=lambda x: (x[1] is not None, x[1]), reverse=reverse)

def is_in_range(val, min_val, max_val):
    """Check whether a value is assigned and in a range.

    >>> is_in_range(0, 1, 2)
    False
    >>> is_in_range(None, 0, 5)
    False
    >>> is_in_range(1, 0, 1)
    True
    """
    return val is not None and val >= min_val and val <= max_val

def modify_movie_list(movies, metascore, random_cnt, sort):
    """Modify the movie list according to the input arguments.

    >>> modify_movie_list([], None, None, None)
    []
    """
    if metascore:
        movies = [m for m in movies if is_in_range(m[1], *metascore)]

    if random_cnt and movies:
        movies = [random.choice(movies) for _ in range(random_cnt)]

    if sort == "asc":
        movies = sort_movie_list(movies)
    elif sort == "desc":
        movies = sort_movie_list(movies, reverse=True)
    return movies

def export_csv(movies, filename):
    """Write the movie list to a csv file."""
    with open(filename, "w") as outfile:
        wrt = csv.writer(outfile)
        for mov in movies:
            wrt.writerow(mov)

def main():
    """Main control function."""
    args = parse_args(sys.argv[1:])

    url = args.url if args.url else "https://www.imdb.com/search/title"
    req = requests.get(url)
    if req.status_code != 200:
        print("Request not successful (status code: %d)" % req.status_code)
        return

    movies = parse_html(req.text)
    movies = modify_movie_list(movies, args.metascore, args.random, args.sort)
    for mov in movies:
        print(mov)

    if args.csv:
        export_csv(movies, args.csv)

if __name__ == "__main__":
    main()
