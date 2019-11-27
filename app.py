from flask import Flask
import pygame
import threading

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


app = Flask(__name__) 
pygame.init()
pygame.mixer.init()
is_playing = False
musicThread = None

@app.route("/")
def hello():                           
    return "<h1>Hello World!</h1>"


def thread_playMusic():
  pygame.mixer.music.load('babyMusic.mp3')
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy(): 
      pygame.time.Clock().tick(10)


@app.route("/playMusic")
def playMusic():
  global is_playing
  global musicThread
  if not is_playing:
    is_playing=True
    musicThread = StoppableThread(target=thread_playMusic)
    musicThread.start()
    return "Play"
  return "already music is playing"


@app.route("/stopMusic")
def stopMusic():
  global is_playing
  global musicThread
  if musicThread is not None:
    musicThread.stop()
    pygame.mixer.music.stop()
    is_playing=False
    musicThread = None
    return "Stop"
  return "already music stop"

if __name__ == "__main__":
  app.run()
