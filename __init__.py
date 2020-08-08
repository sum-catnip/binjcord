from binaryninja import BackgroundTaskThread
from binaryninjaui import DockHandler

import asyncio
import time


try:
    from pypresence import Presence
except ModuleNotFoundError:
    from pip._internal import main
    main(['install', '--quiet', 'pypresence==4.0.0'])


class Binjcord(BackgroundTaskThread):
    def __init__(self):
        super().__init__('binjcord running', True)
        self.time_started = time.time()
        self.rpc = Presence("740982162249089034")
        self.done = False

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.rpc.connect()
        dock = DockHandler.getActiveDockHandler()
        while not self.done:
            frame = dock.getViewFrame()
            if frame:
                fname = frame.getShortFileName()
                offset = hex(frame.getCurrentOffset())
                self.rpc.update(start=self.time_started,
                                large_image='binja',
                                large_text='Binary Ninja',
                                state=fname,
                                details=offset)
                time.sleep(15)
        self.rpc.close()

    def finish(self): self.done = True
    def cancel(self): self.done = True


Binjcord().start()
