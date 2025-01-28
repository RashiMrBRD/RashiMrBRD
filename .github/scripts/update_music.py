import json
import random
import re
import os
from datetime import datetime
from pathlib import Path

def get_repo_root():
    """Get the repository root directory."""
    if 'GITHUB_WORKSPACE' in os.environ:
        return os.environ['GITHUB_WORKSPACE']
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_songs():
    """Load songs from the songs.json file."""
    repo_root = get_repo_root()
    songs_path = os.path.join(repo_root, 'songs.json')
    print(f"Looking for songs.json at: {songs_path}")
    
    try:
        with open(songs_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: songs.json not found at {songs_path}")
        raise
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {songs_path}")
        raise

def get_random_song(songs):
    """Get a random song based on the current hour."""
    hour = datetime.now().hour
    
    if hour >= 0 and hour < 8:  # Midnight to 8AM: Lo-fi/Anime
        genre = 'anime'
    elif hour >= 8 and hour < 16:  # 8AM to 4PM: K-pop
        genre = 'kpop'
    else:  # 4PM to Midnight: OPM
        genre = 'opm'
    
    song = random.choice(songs[genre])
    return song['title'], song['artist'], genre

def update_badge(title, artist):
    """Update the Now Playing badge in the profile."""
    repo_root = get_repo_root()
    profile_path = os.path.join(repo_root, 'profile.md')
    print(f"Looking for profile.md at: {profile_path}")
    
    try:
        if not os.path.exists(profile_path):
            print(f"Error: profile.md not found at {profile_path}")
            print("Current directory contents:")
            print(os.listdir(repo_root))
            raise FileNotFoundError(f"profile.md not found at {profile_path}")

        with open(profile_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create new badge URL
        song_text = f"{title}-{artist}".replace(' ', '_')
        new_badge = f'<img src="https://img.shields.io/badge/Now_Playing-{song_text}-FF69B4?style=for-the-badge&logo=youtube-music&logoColor=white" alt="Now Playing"/>'
        
        # Update the badge in the profile
        pattern = r'<img src="https://img\.shields\.io/badge/Now_Playing-[^"]*" alt="Now Playing"/>'
        updated_content = re.sub(pattern, new_badge, content)
        
        # Update the "Now Playing" section in the ASCII art
        now_playing_pattern = r'(Now Playing:</span> 🎧 ")[^"]*(")'
        updated_content = re.sub(now_playing_pattern, f'\\1{title} ({artist})\\2', updated_content)
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Successfully updated profile with song: {title} by {artist}")
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        raise

def main():
    try:
        print("Loading songs...")
        songs = load_songs()
        print("Getting random song...")
        title, artist, genre = get_random_song(songs)
        print(f"Selected {title} by {artist} from {genre}")
        print("Updating badge...")
        update_badge(title, artist)
        print("Update complete!")
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

if __name__ == '__main__':
    main()
