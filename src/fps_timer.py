import time

class FPS:
    def __init__(self):
        self.start_time = None
        self.num_frames = 0

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        if self.start_time is not None:
            raise RuntimeError("FPS timer is already running")
        self.start_time = time.time()
        return self

    def update(self):
        self.num_frames += 1
        
    def get_fps(self):
        if self.start_time is None:
            raise RuntimeError("FPS timer is not running")
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        fps = self.num_frames / elapsed_time
        return round(fps, 2)

    def stop(self):
        fps = self.get_fps()
        self.reset()
        return fps

    def reset(self):
        self.start_time = None
        self.num_frames = 0
