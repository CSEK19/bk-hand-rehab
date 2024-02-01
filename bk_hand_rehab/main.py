import multiprocessing
from rehab_games.bk_rehab import BKRehab
from hand_gesture_recognition import run_HGR

if __name__ == "__main__":
  multiprocessing.freeze_support()
  # start the gesture recognition process
  p = multiprocessing.Process(target=run_HGR)
  p.daemon=True
  p.start()

  # start the gaming application
  app = BKRehab()
  app.start_app()