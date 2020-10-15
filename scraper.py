import lyricsgenius

artists = ['wu tang clan', 'the beatles', 'justin bieber', 'eminem', 'supertramp', 'pink floyd', 'eagles',
           'red hot chili peppers']

for name in artists:
    # scrape lyrics
    genius = lyricsgenius.Genius("YOUR GENIUS API ACCESS TOKEN HERE")
    artist = genius.search_artist(name, max_songs = 500 , sort="title")

    # write to lyrics file
    name = name.split()
    name = '_'.join(name)
    f = open('{}_lyrics.txt'.format(name), 'w+', encoding='utf-8')
    for song in artist.songs:
        try:
            f.write(song.lyrics)
        except:
            print('Song not found')

    print('Writing lyrics by {} done'.format(name))
    f.close()
