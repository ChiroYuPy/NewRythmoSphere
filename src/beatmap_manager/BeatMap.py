class BeatMap:
    def __init__(self, beatmap_name, difficulty_name, song_path, bg_path, preview_time, creator, artist):

        # [NAME]
        self.beatmap_name: str = beatmap_name
        self.difficulty_name: str = difficulty_name

        # [FILES]
        self.song_path: str = song_path
        self.bg_path: str = bg_path
        self.preview_time: float = preview_time

        # [METADATA]
        self.creator: float = creator
        self.artist: float = artist

