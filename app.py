import streamlit as st

# Assuming there's a Song class defined somewhere above
class Song:
    def __init__(self, name, duration, genre, popularity):
        self.name = name
        self.duration = duration
        self.genre = genre
        self.popularity = popularity

# Initialize the session state for songs if it doesn't exist
if 'songs' not in st.session_state:
    st.session_state.songs = [
        Song("ZBlack", 4, "Haryanavi", 7),
        Song("Jaat Warrior's 2", 3, "Haryanavi", 6),
        Song("Bad Boy", 3, "Hip-Hop", 7),
        Song("Sequência da Dz7", 2, "Phonk", 7),
        Song("Rude Boy", 2, "Phonk", 6)
    ]

# Function to add a song (you might have a different implementation)
def add_song(name, genre, duration, popularity):
    st.session_state.songs.append(Song(name, duration, genre, popularity))

def main():
    st.set_page_config(page_title="Ultimate Playlist Generator", page_icon=":musical_note:")
    st.title("Playlist Manager")
    options = ["Add a song", "Delete a song" , "View your playlist" , "Generate your playlist"]
    action = st.sidebar.selectbox("Choose an option", options)
    
    if action == "Add a song":
        st.subheader("Add Your Own Song")
        with st.form("Add Song"):
            new_song_name = st.text_input("Song Name")
            new_song_duration = st.number_input("Duration (minutes)", min_value=0)
            new_song_genre = st.text_input("Genre")
            new_song_popularity = st.number_input("Popularity", min_value=1, max_value=10)
            submit_button = st.form_submit_button("Add Song")

            if submit_button:
                # Create a new Song object and append it to the session state songs list
                add_song(new_song_name, new_song_genre, new_song_duration, new_song_popularity)
                st.success("Song added successfully!")
    
    elif action == "Delete a song":
        delete_song_indices = []
        for index, song in enumerate(st.session_state.songs):
            # Display each song with a checkbox
            if st.checkbox(f"{song.name} - {song.genre} - {song.duration} mins - Popularity: {song.popularity}", key=index):
                delete_song_indices.append(index)
    
        # Button to delete selected songs
        if st.button("Delete Selected Songs"):
            # Delete songs from the end to avoid index shifting issues
            for index in sorted(delete_song_indices, reverse=True):
                del st.session_state.songs[index]
            st.success("Selected songs deleted successfully!")
            # Refresh the page or re-display the playlist here if needed

    elif action == "View your playlist":
        st.subheader("Your current Playlist with all your songs")
        for song in st.session_state.songs:
            st.write(f"{song.name} - {song.genre} - {song.duration} mins - Popularity: {song.popularity}")

    elif action == "Generate your playlist":
        st.subheader("Generate Your Playlist")
        st.write("Here are the songs in your playlist:")

        # Dynamically extract unique genres from the session state songs list
        unique_genres = list(set(song.genre for song in st.session_state.songs))
        unique_genres.sort()  # Optional: Sort the genres alphabetically
        genre_options = ["All"] + unique_genres  # Add "All" option to the list

        genre_preference = st.selectbox("Choose your preferred genre", genre_options)
        duration_preference = st.slider("Select maximum song duration (minutes)", min_value=1, max_value=10, value=5)
        popularity_preference = st.slider("Select minimum popularity", min_value=1, max_value=10, value=5)

        # Filter songs based on user preferences
        filtered_songs = [song for song in st.session_state.songs if (song.genre == genre_preference or genre_preference == "All") and song.duration <= duration_preference and song.popularity >= popularity_preference]

        # Display the custom playlist
        if filtered_songs:
            st.subheader("Your Custom Playlist")
            for song in filtered_songs:
                st.write(f"{song.name} - {song.genre} - {song.duration} mins - Popularity: {song.popularity}")
        else:
            st.write("No songs match your criteria.")

# Run the app
if __name__ == "__main__":
    main()
