import abc

class IBaseAttachment(abc.ABC):
    @abc.abstractmethod
    def run(self):
        '''
        Run the attachment
        '''
        pass

class IControlledAttachment(IBaseAttachment):
    @abc.abstractmethod
    def step(self):
        '''
        Make a board step
        '''
        pass

    @abc.abstractmethod
    def boardReset(self):
        '''
        Reset the board...
        '''
        pass