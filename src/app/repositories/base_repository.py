import abc


class BaseRepository(abc.ABC):
    @abc.abstractmethod
    def get_one(self, item_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, item):
        raise NotImplementedError
