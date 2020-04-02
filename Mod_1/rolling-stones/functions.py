import csv

with open('data.csv') as f:
    albums = []
    for row in csv.DictReader(f):
        albums.append(row)
albums


# Open Top 500 Songs Text File
text_file = open('top-500-songs.txt', 'r')
lines = text_file.readlines()
song_list = []
for line in lines:
    line_list = line.split('\t')
    song_list.append(line_list)


#Create a dict with Top 500 Songs Text File

songs = []
for s in song_list:
    song = {'rank': s[0],
            'name': s[1],
            'artist': s[2],
            'year': s[3][:-1],
            }
    songs.append(song)
    
    
    
import json

file = open('track_data.json', 'r')
albums_json = json.load(file)


# Pass album name, returns dict of album info.
def find_by_name(name, data_set):
    for album in data_set:
        if album['album'].lower() == name.lower():
            return album
        else:
            return None


# Pass album rank, returns album name, rank.
def find_by_rank(rank, our_data):
    for album in our_data:
        if int(album['number']) == rank:
            return album
    return None


# Pass year, returns list of album names in that year. 
def find_by_year(year, data_set):
    result = []
    for album in data_set:
        if int(album['year']) == year:
            result.append(album['album'])
    return result


# Pass start and end years, returns list of album names in range (inclusive).
def find_by_years(start_yr, end_yr, data_set):
    result = []
    for album in data_set:
        if int(album['year']) in range(start_yr, end_yr + 1):
            result.append(album['album'])
    return result


# Pass start and end ranks, returns list of album names in range (inclusive).
def find_by_ranks(start_rk, end_rk, data_set):
    result = []
    for album in data_set:
        if int(album['number']) in range(start_rk, end_rk + 1):
            result.append(album['album'])
    return result


#All titles - Returns a list of album titles for each album.
def all_albums(data_set):
    result = []
    for album in data_set:
        result.append(album['album'])
    return result


#All artists - Returns a list of artist names for each album.
def all_artists(data_set):
    result = []
    for album in data_set:
        result.append(album['artist'])
    return result


# Returns list of all songs.
def all_songs(data_set):
    result = []
    for album in data_set:
        result.append(album['name'])
    return result


top_500 = all_songs(songs)


#following functions require collections
import collections

#Artists with the most albums - Returns the artist with the highest amount of albums on the list of top albums
def artist_w_most_albums(data_set):
    sample = all_artists(data_set)
    c = collections.Counter(sample)
    return c.most_common(5)

   
    
#Most popular word - Returns the word used most in amongst all album titles    
def most_popular_word(data_set):
    result = []
    for title in all_titles(data_set):
        word_list = title.split()
        for word in word_list:
            result.append(word)
    c = collections.Counter(result)
    return c.most_common(1)


#Following Histograms require matplotlib
import matplotlib.pyplot as plt

#Histogram of albums by decade - Returns a histogram with each decade pointing to the number of albums released during that decade.
def year_hist(data_set):
    result = []
    for album in data_set:
        result.append(int(album['year']))
    
    num_bins = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
    plt.hist(result, num_bins, facecolor='blue', alpha=1)
    plt.title('Album Histogram')
    plt.xlabel('Number of Albums')
    plt.ylabel('Years')
    return plt.show()
                       

#Histogram by genre - Returns a histogram with each genre pointing to the number of albums that are categorized as being in that genre.                     
def genre_hist(data_set):
    result = []
    for album in data_set:
        result.append(album['genre']) 
        
    c = collections.Counter(result)
    plt.bar(range(len(c)), c.values(), alpha=1)
    plt.title('Genre')
    plt.xlabel('Genres')
    plt.ylabel('Counter')
    return plt.show()



# Returns the album with the most Top 500 songs.
def album_w_most_songs():
    sample = {}
    most_songs = 0
    top_album = []
    for album in albums_json:
        i = 0
        track_list = []
        for song in album['tracks']:
            track_list.append(song)
            for track in track_list:
                if track in top_500:
                    i += 1
                    sample[album['album']] = [album['artist'], i]
                    if i > most_songs:
                        most_songs = i
                        top_album = [album['artist'], album['album']]
    return top_album



# Returns list of albums with a Top 500 song.
def albums_w_top_songs():
    result = []
    for album in albums_json:
        track_list = []
        for song in album['tracks']:
            track_list.append(song)
            for track in track_list:
                if track in top_500:
                    result.append(album['album'])
    return list(set(result))
albums_w_top_songs()



# Returns list of songs in the Top Albums.
def songs_in_top_albums():
    result = []
    for album in albums_json:
        if album['album'] in all_albums(albums):
            for song in album['tracks']:
                result.append(song)
    return result
songs_in_top_albums()


# Returns hist of Top 10 Albums.
def album_top_10():
    sample = []
    for album in albums_json:
        track_list = []
        for song in album['tracks']:
            track_list.append(song)
            for track in track_list:
                if track in all_songs(songs):
                    sample.append(album['album'])
    counter = collections.Counter(sample)
    c = counter.most_common(10)
    numbers = []
    titles = []
    for item in counter.most_common(10):
        titles.append(item[0])
        numbers.append(item[1])
    plt.bar(range(len(titles), numbers, alpha=1)
    plt.title('Top 10 Album')
    plt.xlabel('Albums')
    plt.ylabel('Apperances')
    return plt.show()


# Returns top overall artist.
def top_overall_artist():
    sample = {}
    i = 0
    for artist in all_artists(albums):
        sample[artist] = i
    for album in albums_json:
        if album['album'] in all_albums(albums):
            sample[album['artist']] += 1
    for song in songs:
        if song['artist'] not in sample.keys():
            sample[song['artist']] = i + 1
        sample[song['artist']] += 1
    top = max(sample.values())
    for artist in sample:
        if sample[artist] == top:
            return artist, top
top_overall_artist()