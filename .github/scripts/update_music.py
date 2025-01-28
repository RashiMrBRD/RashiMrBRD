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
    """Update the Now Playing badge in the README."""
    repo_root = get_repo_root()
    readme_path = os.path.join(repo_root, 'README.md')
    print(f"Looking for README.md at: {readme_path}")
    
    try:
        if not os.path.exists(readme_path):
            print(f"Error: README.md not found at {readme_path}")
            print("Current directory contents:")
            print(os.listdir(repo_root))
            raise FileNotFoundError(f"README.md not found at {readme_path}")

        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create new badge URL
        song_text = f"{title}-{artist}".replace(' ', '_')
        new_badge = f'<img src="https://img.shields.io/badge/Now_Playing-{song_text}-FF69B4?style=for-the-badge&logo=youtube-music&logoColor=white" alt="Now Playing"/>'
        
        # Check if badge already exists
        pattern = r'<img src="https://img\.shields\.io/badge/Now_Playing-[^"]*" alt="Now Playing"/>'
        if re.search(pattern, content):
            # Update existing badge
            updated_content = re.sub(pattern, new_badge, content)
        else:
            # Add badge after the first heading
            heading_pattern = r'^#[^#\n]*\n'
            match = re.search(heading_pattern, content)
            if match:
                insert_pos = match.end()
                updated_content = content[:insert_pos] + f"\n{new_badge}\n" + content[insert_pos:]
            else:
                # If no heading found, add at the beginning
                updated_content = f"{new_badge}\n\n{content}"
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Successfully updated README with song: {title} by {artist}")
    except Exception as e:
        print(f"Error updating README: {str(e)}")
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
