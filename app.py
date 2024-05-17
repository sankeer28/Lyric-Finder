from flask import Flask, request, jsonify
from lyricsgenius import Genius
import re
import config
app = Flask(__name__)
genius = Genius(config.GENIUS_ACCESS_TOKEN)
@app.route('/')
def index():
    return app.send_static_file('index.html')
@app.route('/lyrics', methods=['GET'])
def get_lyrics():
    song_name = request.args.get('song_name')
    artist_name = request.args.get('artist_name')

    print(f"Searching for song: {song_name} by {artist_name}")

    if not song_name:
        return jsonify({'error': 'Please provide a song name'})

    search_query = f"{song_name} {artist_name}" if artist_name else song_name

    song = genius.search_song(search_query)
    if song:
        lyrics = re.sub(r'\[.*\]', '', song.lyrics)
        lyrics = re.sub(r'\d+ Contributors', '', lyrics)
        lines = lyrics.split('\n')
        if len(lines) > 1:
            lyrics = '\n'.join(lines[1:])
        lyrics = lyrics.strip()
        return jsonify({'lyrics': lyrics})
    else:
        return jsonify({'error': 'Song not found'})

if __name__ == '__main__':
    app.run(debug=True)
