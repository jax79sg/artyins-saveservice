from abc import ABC, abstractmethod
class SaverInterface(ABC):
    """  An abstract base class for saving tools """

    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def create(self, json):
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, json):
        raise NotImplementedError()
  
    @abstractmethod
    def get(self, json):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, json):
        raise NotImplementedError()

    def freequery(self, string):
        raise NotImplementedError()

