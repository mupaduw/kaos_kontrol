#!looping.py 
from mididings import *
from mididings.event import CtrlEvent
  
class KaosKontrol:

    notes_sounding = []
    YVAL = 0

    def handle_event(self, ev, **kwargs):
        '''
        event handler
        '''
        C3, C5 = 48, 72

        if ev.type == NOTEON:
            if (C3 <= ev.note <= C5 ):
                if ev.note == C3:
                    yield CtrlEvent(ev.port, ev.channel, 12, 0)
                elif ev.note == C5:
                    yield CtrlEvent(ev.port, ev.channel, 12, 127)
                else:
                    yield CtrlEvent(ev.port, ev.channel, 12, (ev.note-C3) * int(127/25) + 4)
                yield CtrlEvent(ev.port, ev.channel, 13, self.YVAL)
                yield CtrlEvent(ev.port, ev.channel, 92, 127)
                self.notes_sounding.append(ev.note)

        elif ev.type == NOTEOFF:
            self.notes_sounding.remove(ev.note)
            if len(self.notes_sounding) == 0:
                yield CtrlEvent(ev.port, ev.channel, 92, 0)

        elif ev.type == CTRL:
            if ev.ctrl == 1:
                self.YVAL = ev.value
                yield  CtrlEvent(ev.port, ev.channel, 13, ev.value)
    