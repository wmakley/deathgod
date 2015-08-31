class Listener:
    def __init__(self, manager):
        self.evManager = manager
        
    """ Override this method """
    def notify(self, event):
        pass