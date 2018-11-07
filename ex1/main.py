import csv
import collections
import sys
import time

INPUT_FILE = 'song_titles.csv'
OUTPUT_FILE = 'output.csv'
'''
Got This function from Google
'''
def iterative_levenshtein(s, t):
    """
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    rows = len(s) + 1
    cols = len(t) + 1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = i
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row - 1][col] + 1,  # deletion
                                 dist[row][col - 1] + 1,  # insertion
                                 dist[row - 1][col - 1] + cost)  # substitution

    return dist[row][col]

if __name__ == "__main__":

    print("Started!")
    song_names = set([])
    with open(INPUT_FILE, 'rb') as f:
        input_reader = csv.DictReader(f)
        song_names = set([line['song_name'] for line in input_reader])

    with open(OUTPUT_FILE, 'wb') as f:
        output_writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(('song_name', 'similar1', 'similar2', 'similar3'))

        distances = collections.defaultdict(int)

        for song in song_names:

            closest_songs = []

            for similar_song in song_names:
                if song == similar_song:
                    continue

                'Avoid calculations'
                key = '|'.join(sorted([song.strip().lower(), similar_song.strip().lower()]))
                if distances[key] == 0:
                    distances[key] = iterative_levenshtein(song, similar_song)

                similar_song_rank = distances[key]

                #in case that we don't have 3 items in the array
                if len(closest_songs) < 3:
                    closest_songs.append( (similar_song, similar_song_rank ) )
                    closest_songs.sort(key=lambda tup: tup[1])
                    continue

                highest_rank = closest_songs[2][1]#array is sorted
                if similar_song_rank < highest_rank:
                    closest_songs[2] = (similar_song, similar_song_rank)
                    closest_songs.sort(key=lambda tup: tup[1])

            output_writer.writerow((song, closest_songs[0][0], closest_songs[1][0], closest_songs[2][0]))

    print("Finished!")
print(iterative_levenshtein("lawn2", "lawn"))
print(iterative_levenshtein("I Didn't Mean To", "Amor De Cabaret" ))