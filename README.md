# Extended search for IMDB

This is a python script for extending the IMDB advanced title search by:

  - ordering and filtering by metascore
  - random choice of movies

## General Notes
  - Doesn't require any IMDB/OMDB/TMDB account. The movies get parsed directly from the HTML data.
  - Tested with Python 2.7 and 3.6 under Opensuse 15.

## Usage

There are two options to use this script:

  1. Issue a search on the site <https://www.imdb.com/search/title>. Then copy the url of the resulting page. Alternatively the base url can be extended by the query string directly. Finally insert the url string as optional argument (`--url`).
  2. Create a json file with parameters and insert it as optional argument (`--json`). The parameters get sent to <https://www.imdb.com/search/title> with a get request.

The options `--url` and `--json` are mutually exclusive, i. e. exactly one of them has to be given. Further arguments can be used to filter movies out of the original list. Result is a list of tuples, containing name, metascore and link to IMDB of each movie.

### Examples

  - Get 10 random movies via query string:
```bash
python3 imdb_ext_search.py --url "https://www.imdb.com/search/title?title_type=feature&count=250" --random 10
```

  - Get 10 random movies via JSON parameters:
```bash
python3 imdb_ext_search.py --json "example_params.json" --random 10
```

  - Only show movies with metascore equal or higher than 80 and order the movies descending by metascore:
```bash
python3 imdb_ext_search.py --url "https://www.imdb.com/search/title?title_type=feature&count=250" --metascore 80 100 --sort desc
```

  - Save the movie list as csv file:
```bash
python3 imdb_ext_search.py --url "https://www.imdb.com/search/title?title_type=feature&count=250" --csv my_movies.csv
```