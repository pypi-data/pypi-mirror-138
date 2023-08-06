from keygim.imageUtils import BasicUtils, ImageUtils 
from keyscraper.utils import TimeName, FileName
from pynput.keyboard import Listener as KeyListener, KeyCode, Key 
from pynput.mouse import Listener as Listener, Controller
import time, sys, cv2, os
class PFPC:
    __MODES = [ 10, 20 ]
    MODE_SHUTDOWN = __MODES[0]
    
    __FILENAME = "intruder.png"
    
    __WAIT_QUANTUM = 0.01
    def __init__(self, password, savepath = "./", exceptions = []):
        self.password = BasicUtils.verify_type(password, [str])
        self.savepath = BasicUtils.verify_folder(BasicUtils.verify_type(savepath, [str]), True)
        self.password = [ KeyCode(char = char.lower()) for char in self.password ]
        self.exceptions = BasicUtils.verify_type(exceptions, [list])
        self.pressed = [ False for _ in self.password ]
    def __shutdown(self):
        os.system("shutdown -s -t 0 -f")
    def __capture_webcam(self):
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        cam.release()
        return frame
    def __capture_save(self):
        filename = FileName(self.savepath + self.__FILENAME)
        filename = TimeName().get_name(filename["folder"] + filename["name"], filename["extension"])
        try:
            ImageUtils.ImageSaver(filename).save_image(
                self.__capture_webcam(), overwrite = False    
            )
        except:
            pass
    def __penalize(self):
        self.__capture_save()
        os.system("start chrome.exe")
        self.pressed = [ True for _ in self.pressed ]
    def __check_penalty(self):
        if (self.__chances):
            self.__chances = max(0, self.__chances - 1)
        else:
            self.__penalise = True
    def __on_press(self, key):
        for __index, __key in enumerate(self.password):
            if (__key == key):
                if ((__index == 0) or (self.pressed[__index - 1])):
                    self.pressed[__index] = True 
                return 
        if (key in self.exceptions):
            return
        self.pressed = [ False for _ in self.pressed ]
        self.__check_penalty()
    def __on_move(self, x, y):
        if ((self.bbox["sx"] <= x <= self.bbox["ex"]) and (self.bbox["sy"] <= y <= self.bbox["ey"])):   
            self.__calibrate = False
            return
        self.__calibrate = True
        self.__check_penalty()
    def run(self, chances = 3, verbose = True):
        self.__calibrate = False
        self.__penalise = False
        self.__chances = max(0, BasicUtils.verify_type(chances, [int]))
        verbose = bool(BasicUtils.verify_type(verbose, [int,bool]))
        snapshot = ImageUtils.SnapshotTaker().take_screenshot(Key.esc, "Press Esc to take screenshot.")
        self.bbox = ImageUtils.BoundaryBoxSelector(snapshot).draw()
        KListener = KeyListener(on_press = self.__on_press)
        MListener = Listener(on_move = self.__on_move)
        KListener.start()
        MListener.start()
        while any([ not x for x in self.pressed ]):
            if (verbose):
                sys.stdout.write(BasicUtils.format_length(f"\r[{self.__chances}] chances left", 50))
            if (self.__calibrate):
                Controller().position = (self.bbox["cx"], self.bbox["cy"])
            if (self.__penalise):
                self.__penalize()
                self.__penalise = False
            time.sleep(self.__WAIT_QUANTUM)
            if (verbose):
                sys.stdout.flush()
        MListener.stop()
        KListener.stop()
if (__name__ == "__main__"):
    listener = PFPC("abcd", "./", [Key.ctrl, KeyCode(char = 'o'), Key.end])
    listener.run(10)