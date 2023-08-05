"""
Repositories to store podcasts/episodes.

Atm only uses json. But this could also be a sqlite or a
remote api, maybe fastAPI... hmm.
"""
from datetime import datetime
from operator import itemgetter
from time import mktime

import feedparser
from pydantic import BaseModel, parse_file_as

from .models import Episode, Podcast


class FeedInDb(BaseModel):
    url: str
    updated: datetime


class EpisodeInDb(BaseModel):
    index: int
    guid: str
    audio_url: str
    published: datetime
    title: str
    audio_file: str | None

    @property
    def pk(self):
        return self.guid


class EpisodeListInDb(BaseModel):
    """
    Used to make a list of episodes serializable to json.
    """

    __root__: list[EpisodeInDb]


class PodcastInDb(BaseModel):
    feed: FeedInDb
    title: str
    episodes_count: int
    file_name_pattern: str
    directory: str | None

    @property
    def pk(self):
        return self.feed.url


class PodcastListInDb(BaseModel):
    """
    Used to make a list of podcasts serializable to json.
    """

    __root__: list[PodcastInDb]


class JsonRepository:
    """
    Store a dict of serialized pydantic models in a json store.

    Use model.pk as primary key to be able to quickly locate models
    and maybe get/update/remove them.
    """

    _all = None

    def __init__(self, base_dir):
        self.base_dir = base_dir

    @property
    def path(self):
        return self.base_dir / self.name

    def _fetch_all(self):
        """
        Fetch dict of pydantic models from json in self.path
        """
        try:
            return {
                model.pk: model
                for model in parse_file_as(list[self.storage_model_type], self.path)
            }
        except FileNotFoundError:
            return {}

    @property
    def all(self):
        """
        Cache fetching all models from file.
        """
        if self._all is None:
            self._all = self._fetch_all()
        return self._all

    def list(self, additional_attributes=None):
        """
        Just return a list of all stored models. Convert models from storage
        model type to domain model type.
        """
        if additional_attributes is None:
            return [
                self.domain_model_type.from_dict(model.dict())
                for model in self.all.values()
            ]
        else:
            return [
                self.domain_model_type.from_dict(model.dict() | additional_attributes)
                for model in self.all.values()
            ]

    def _write_models(self, locked):
        try:
            self.path.parent.mkdir(exist_ok=True)
        except AttributeError:
            # LocalPath in tests
            pass
        models = self.storage_model_list_type(__root__=list(locked.values()))
        with self.path.open("w") as f:
            f.write(models.json())

    def add(self, model):
        """Add a single model to the repository."""
        model_in_db = self.storage_model_type(**model.dict())
        # To avoid race conditions implement proper locking of json file FIXME
        locked = self._fetch_all()
        locked[model_in_db.pk] = model_in_db
        self._write_models(locked)

    def add_list(self, models):
        """Add a list of models to the repository."""
        models_in_db = [self.storage_model_type(**model.dict()) for model in models]
        # To avoid race conditions implement proper locking of json file FIXME
        locked = self._fetch_all()
        for model_in_db in models_in_db:
            locked[model_in_db.pk] = model_in_db
        self._write_models(locked)


class EpisodeRepository(JsonRepository):
    """
    Store episodes metadata and audio files for a podcast.
    """

    name = "episodes.json"
    storage_model_type = EpisodeInDb
    storage_model_list_type = EpisodeListInDb
    domain_model_type = Episode


class PodcastRepository(JsonRepository):
    """
    Store podcasts metadata.
    """

    name = "podcasts.json"
    storage_model_type = PodcastInDb
    storage_model_list_type = PodcastListInDb
    domain_model_type = Podcast


class FeedParserRepository:
    """
    Fetch/parse feed data from http.
    """

    @staticmethod
    def parse_feed_entries(entries):
        """
        Turn the entries attribute of a parsed podcast feed into dicts
        which could then be validated by pydantic and turned into domain
        models.
        """
        episodes = []
        for entry in entries:
            episodes.append(
                {
                    "guid": entry.id,
                    "audio_url": entry.enclosures[0]["href"],
                    "published": datetime.fromtimestamp(mktime(entry.published_parsed)),
                    "title": entry.title,
                }
            )
        episodes.sort(key=itemgetter("published"))
        # add index
        for index, episode in enumerate(episodes, 1):
            episode["index"] = index
        return episodes

    def get(self, url, directory, episode_name_pattern):
        """
        Fetch feed from http and parse/validate/build a podcast domain model.
        """
        document = feedparser.parse(url)

        # validate and build feed
        feed_in_db = FeedInDb(
            url=url, updated=datetime.fromtimestamp(mktime(document["updated_parsed"]))
        )

        # validate episodes
        episodes_from_feed = self.parse_feed_entries(document.entries)
        validated_episodes = [EpisodeInDb(**episode) for episode in episodes_from_feed]

        # validate and build podcast
        podcast_in_db = PodcastInDb(
            feed=feed_in_db,
            title=document["feed"]["title"],
            file_name_pattern=episode_name_pattern,
            episodes_count=len(validated_episodes),
            directory=directory,
        )
        podcast = Podcast.from_dict(podcast_in_db.dict())

        # validate and build episodes
        episodes = [
            Episode.from_dict(episode.dict() | {"podcast": podcast})
            for episode in validated_episodes
        ]

        return podcast, episodes
