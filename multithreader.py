import threading


class MThreading(object):
    def __init__(self):
        self.threads = []

    def _run_thread(self, fn, *args, **kwargs):
        self.threads = [t for t in self.threads if t.is_alive()]
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        self.threads.append(thread)


MT = MThreading()