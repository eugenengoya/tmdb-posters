import requests
import urllib.request
import os
import re

# Replace with your TMDb API key
TMDB_API_KEY = ''

def search_movies(query):
    url = f'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'query': query
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['results'][:10] if 'results' in data else []

def get_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    params = {
        'api_key': TMDB_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def download_image(url, save_path):
    if not os.path.exists(save_path):
        try:
            urllib.request.urlretrieve(url, save_path)
            print(f"Downloaded: {save_path}")
        except Exception as e:
            print(f"Failed to download {url}. Error: {e}")
    else:
        print(f"File already exists: {save_path}")

def select_movie(movies):
    print("Search Results:")
    for index, movie in enumerate(movies, start=1):
        print(f"{index}. {movie['title']} ({movie['release_date'][:4]})")

    while True:
        try:
            choice = int(input(f"Enter the number of the movie you want to download (1-{len(movies)}, or 0 to exit): "))
            if 0 <= choice <= len(movies):
                break
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(movies)} or 0 to exit.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    return movies[choice - 1] if choice > 0 else None

def format_title(title):
    # Clean up the title to lowercase with underscores
    cleaned_title = re.sub(r'\W+', '_', title.lower())
    return cleaned_title

def main():
    movie_title = input("Enter the title of the movie: ")
    movies = search_movies(movie_title)

    if movies:
        selected_movie = select_movie(movies)

        if selected_movie:
            formatted_title = format_title(selected_movie['title'])
            release_year = selected_movie['release_date'][:4]
            media_folder = 'media'

            # Create media folder if it doesn't exist
            if not os.path.exists(media_folder):
                os.makedirs(media_folder)

            poster_url = f"https://image.tmdb.org/t/p/original{selected_movie['poster_path']}"
            banner_url = f"https://image.tmdb.org/t/p/original{selected_movie['backdrop_path']}"

            # Download poster
            if selected_movie['poster_path']:
                poster_path = os.path.join(media_folder, f"{formatted_title}_({release_year})_poster.jpg")
                print(f"Downloading poster for {selected_movie['title']} ({release_year})...")
                download_image(poster_url, poster_path)

            # Download banner
            if selected_movie['backdrop_path']:
                banner_path = os.path.join(media_folder, f"{formatted_title}_({release_year})_banner.jpg")
                print(f"Downloading banner for {selected_movie['title']} ({release_year})...")
                download_image(banner_url, banner_path)

            print("Download complete.")
        else:
            print("No movie selected. Exiting.")
    else:
        print(f"No movies found with the title '{movie_title}'.")

if __name__ == "__main__":
    main()