import asyncio
from asyncio import AbstractEventLoop
from threading import Thread

from chapter_7.tkin.stress_test_ui import LoadTester


class ThreadedEventLoop(Thread):
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    asyncio_thread  = ThreadedEventLoop(loop=loop)
    asyncio_thread.start()

    app = LoadTester(loop=loop)
    app.mainloop()
