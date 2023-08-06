# -*- coding: utf-8 -*-
import logging


class Controls:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._event_callbacks = dict()
    
    def get_callbacks(self, event=None):
        """
        Primarily used for debugging
        """
        if event is None:
            return self._event_callbacks
        elif event in self._event_callbacks:
            return self._event_callbacks[event]
        else:
            raise ValueError("Event not found")
    
    def add_event_callback(self, event, callback):
        if event not in self._event_callbacks:
            self._event_callbacks[event] = list()
        self._event_callbacks[event].append(callback)
        #self.logger.debug(f"Added cb to {event}: {callback}")
    
    def clear_by_obj(self, obj):
        for event in self._event_callbacks:
            for i, cb in enumerate(self._event_callbacks[event]):
                if cb.__self__ is obj:
                    #self.logger.debug(f"Deleted cb: {cb}")
                    del self._event_callbacks[event][i]
    
    def _event(self, event, *args, **kwargs):
        try:
            #self.logger.debug(f"Event called: {event}")
            for callback in self._event_callbacks[event]:
                callback(*args, **kwargs)
        except KeyError:
            self.logger.debug(f'Event called, but no callbacks: {event}')