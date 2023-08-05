"""
All the domain models for pdcst live here.
"""


class Feed:
    """
    To be able to fetch a feed with feedparser, we need it's url.
    """

    def __init__(self, *args, url, updated):
        self.url = url
        self.updated = updated

    @classmethod
    def from_dict(cls, feed):
        return cls(**feed)

    def dict(self):
        return {
            "url": self.url,
            "updated": self.updated,
        }

    def __eq__(self, other):
        return self.url == other.url


class Podcast:
    """
    Podcasts have a feed that can be fetched. Attributes like
    title or episodes_count are retrieved from the feed.

    The file_name_pattern is settable and determines the naming
    schema for the audio files of podcast episodes. Podcast episodes
    live in a directory which is also settable. By default, it's
    derived from the title.
    """

    def __init__(
        self,
        *,
        feed,
        title,
        episodes_count,
        file_name_pattern="{index}_{title}.{file_format}",
        directory=None,
    ):
        self.feed = feed
        self.title = title
        self.file_name_pattern = file_name_pattern
        self.episodes_count = episodes_count
        self.directory = (
            self.title.lower().replace(" ", "_") if directory is None else directory
        )

    @classmethod
    def from_dict(cls, podcast):
        """Construct a podcast from a dict."""
        feed = Feed.from_dict(podcast.pop("feed"))
        return cls(**podcast, feed=feed)

    def dict(self):
        """Serialize a podcast to dict."""
        return {
            "title": self.title,
            "feed": self.feed.dict(),
            "episodes_count": self.episodes_count,
            "file_name_pattern": self.file_name_pattern,
            "directory": self.directory,
        }

    def __repr__(self):
        return f"{self.title} - {self.episodes_count} episodes"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        equal = self.feed == other.feed and self.title == other.title
        return equal

    def get_audio_file_name(self, episode):
        """
        Use the file_name_pattern to build a name for episodes audio files.
        """
        details = {
            # FIXME proper suffix from path? Or take info about format from feed?
            "file_format": episode.audio_url.split(".")[-1],
            "index": episode.index,
            "title": episode.title.lower().replace(" ", "_"),
        }
        return self.file_name_pattern.format(**details)


class Episode:
    """
    Episodes belong to a podcast. They have an index, which we
    calculate by ourselves. The guid, audio_url, published date
    and title are attributes which we get from the feed.

    We store a reference to downloaded audio files in the audio_file
    attribute.
    """

    def __init__(
        self,
        *,
        index,
        guid,
        audio_url,
        published,
        title,
        podcast=None,
        audio_file=None,
    ):
        self.podcast = podcast
        self.index = index
        self.guid = guid
        self.audio_url = audio_url
        self.published = published
        self.title = title
        self.audio_file = audio_file

    @classmethod
    def from_dict(cls, episode):
        """Construct an episode from a dict."""
        return cls(**episode)

    def __repr__(self):
        return f"{self.title}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.podcast == other.podcast and self.audio_url == other.audio_url

    def dict(self):
        """Serialize an episode to dict."""
        return {
            "index": self.index,
            "guid": self.guid,
            "audio_url": self.audio_url,
            "published": self.published,
            "title": self.title,
            "audio_file": self.audio_file,
        }

    @property
    def audio_file_name(self):
        return self.podcast.get_audio_file_name(self)
