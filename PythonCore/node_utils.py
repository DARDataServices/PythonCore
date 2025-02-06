from abc import ABC, abstractmethod

class AbstractNodeClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_total_stake(self, epoch):
        pass

    @abstractmethod
    def get_staking_rewards(self, epoch):
        pass

    @abstractmethod
    def get_settlement_time(self, epoch):
        pass

    @abstractmethod
    def get_current_epoch(self):
        pass