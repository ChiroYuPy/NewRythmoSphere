import json
import os

from src.beatmap_manager.BeatMap import BeatMap


class BeatmapLoader:
    def __init__(self, database_path="database.json"):
        self.database_path = database_path
        self.database = self.load_database()

    def load_database(self):
        """Load the beatmap database from a JSON file."""
        with open(self.database_path, 'r') as db_file:
            return json.load(db_file)

    def check_and_add_missing_beatmaps(self, parent_folder):
        """
        Check for each folder and .txt file in the parent_folder if it exists in the database.
        If not, read the metadata from the .txt files and add the missing beatmap or difficulty
        to the database.
        """
        folders = sorted([item for item in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, item))])

        for folder in folders:
            # Extract the beatmap ID and name
            beatmap_id, beatmap_name = folder.split(' - ', 1)
            beatmap_id = beatmap_id.strip()  # Clean ID

            # Check if the beatmap already exists in the database
            if beatmap_id not in self.database:
                print(f"Adding new beatmap '{beatmap_id} - {beatmap_name}' to database.")
                self.database[beatmap_id] = {
                    "beatmap_name": beatmap_name,
                    "difficulties": {}
                }

            # Check for .txt files corresponding to difficulties
            difficulty_files = [f for f in os.listdir(os.path.join(parent_folder, folder)) if f.endswith('.txt')]
            for difficulty_file in difficulty_files:
                difficulty_name = difficulty_file[:-4]  # Remove '.txt' extension

                # Check if the difficulty exists in the database
                if difficulty_name not in self.database[beatmap_id]["difficulties"]:
                    # Read metadata from the .txt file
                    metadata = self.read_metadata_from_txt(os.path.join(parent_folder, folder, difficulty_file))

                    # Add missing difficulty with the extracted metadata
                    print(f"Adding missing difficulty '{difficulty_name}' for beatmap '{beatmap_id}' to database.")
                    self.database[beatmap_id]["difficulties"][difficulty_name] = {
                        "bg_name": metadata.get("BG_NAME", "background"),
                        "bg_ext": metadata.get("BG_EXTENSION", "jpg"),
                        "preview_time": metadata.get("PREVIEW_TIME", "0.000"),
                        "creator": metadata.get("CREATOR", "Unknown Creator")
                    }

                    # Also update song info if it hasn't been set yet
                    if "song_name" not in self.database[beatmap_id]:
                        self.database[beatmap_id]["song_name"] = metadata.get("SONG_NAME", "unknown")
                        self.database[beatmap_id]["song_ext"] = metadata.get("SONG_EXTENSION", "mp3")
                        self.database[beatmap_id]["preview_time"] = metadata.get("PREVIEW_TIME", "0.000")
                        self.database[beatmap_id]["artist"] = metadata.get("ARTIST", "Unknown Artist")

        # Save the updated database back to the JSON file
        self.save_database()

    def read_metadata_from_txt(self, txt_file_path):
        """
        Read metadata from the .txt file under the [METADATA] section.
        Returns a dictionary containing the relevant metadata.
        """
        metadata = {}
        in_metadata_section = False

        try:
            with open(txt_file_path, 'r') as txt_file:
                for line in txt_file:
                    line = line.strip()

                    if line == "[METADATA]":
                        in_metadata_section = True
                    elif line == "[OBJECTS]":
                        break  # End of metadata section
                    elif in_metadata_section:
                        # Split the key-value pair by ":"
                        if ":" in line:
                            key, value = line.split(":", 1)
                            metadata[key.strip()] = value.strip()

        except Exception as e:
            print(f"Error reading metadata from '{txt_file_path}': {e}")

        return metadata

    def load_beatmaps(self, parent_folder):
        """
        Load beatmaps from the database for each difficulty.
        Returns a list of BeatMap instances.
        """
        # First, ensure all missing beatmaps and difficulties are added to the database
        self.check_and_add_missing_beatmaps(parent_folder)

        all_beatmaps = []
        for beatmap_key, beatmap_info in self.database.items():
            beatmaps = self.create_beatmap_instances(parent_folder, beatmap_key, beatmap_info)
            all_beatmaps.extend(beatmaps)

        return all_beatmaps

    def create_beatmap_instances(self, parent_folder, beatmap_key, beatmap_info):
        """
        Create BeatMap instances from the database info for a specific beatmap key.
        """
        beatmaps = []
        song_name = beatmap_info.get("song_name", "unknown")
        song_ext = beatmap_info.get("song_ext", "mp3")
        beatmap_name = beatmap_info.get("beatmap_name", "unknown")

        for difficulty, details in beatmap_info.get("difficulties", {}).items():
            song_path = os.path.join(parent_folder, beatmap_key + " - " + beatmap_name, f"{song_name}.{song_ext}")
            bg_name = details.get("bg_name", "background")
            bg_ext = details.get("bg_ext", "jpg")
            bg_path = os.path.join(parent_folder, beatmap_key, f"{bg_name}.{bg_ext}")
            creator = details.get("creator", "Unknown Creator")
            artist = beatmap_info.get("artist", "Unknown Artist")
            beatmap_name = beatmap_info.get("beatmap_name", "Unknown Beatmap")
            preview_time = float(beatmap_info.get("preview_time", "0.000"))

            # Create a BeatMap instance for each difficulty
            beatmap = BeatMap(beatmap_name, difficulty, song_path, bg_path, preview_time, creator, artist)
            print(f"Loaded beatmap '{beatmap_name} - {difficulty}' from database.")

            beatmaps.append(beatmap)

        return beatmaps

    def save_database(self):
        """Save the updated database back to the JSON file."""
        with open(self.database_path, 'w') as db_file:
            json.dump(self.database, db_file, indent=4)
