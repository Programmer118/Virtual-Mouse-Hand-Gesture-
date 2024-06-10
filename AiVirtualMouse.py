import cv2
import numpy as np
import HandTrackingModule as htm
# from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key, Controller as KeyController
import time
import pyautogui
from pymouse import PyMouse
from pywinauto import Desktop
import warnings

class HandMouseController:
    def __init__(self, wCam=640, hCam=480, frameR=100, smoothening=7):
        """
        Initializes the HandMouseController class with camera settings, frame reduction,
        and smoothing parameters.

        Args:
            wCam (int): Width of the camera frame.
            hCam (int): Height of the camera frame.
            frameR (int): Frame reduction value.
            smoothening (int): Smoothening factor for mouse movement.
        """
        warnings.filterwarnings("ignore")

        # Constants1  
        self.isChanged = False 
        self.WindowIndex = 1
        self.WindowIndex = 1 
        self.wCam = wCam
        self.hCam = hCam
        self.frameR = frameR  # Frame Reduction
        self.smoothening = smoothening
        self.fingerConfiguration = {
            'Move': [0, 1, 0, 0, 0],
            "Scroll": [0, 1, 1, 0, 0],
            "LeftClick": [1, 1, 0, 0, 0],
            "RightClick": [1, 1, 1, 0, 0]
        }

        # Variables for tracking time and location
        self.pTime = 0
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0

        # Initialize the video capture
        self.cap = cv2.VideoCapture(0)  # Use 0 for the primary camera
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)

        # Hand detector setup
        self.detector = htm.handDetector()

        # Screen size
        self.wScr, self.hScr = pyautogui.size()

        # Mouse and keyboard controllers
        self.mouse = pyautogui
        self.keyboard = KeyController()

    

    def ChangeWindow(self):
        
        """
        Switches to the next window using pywinauto.
        """
        desktop = Desktop(backend="uia")

        # Get the list of all top-level windows
        windows = desktop.windows()

        if not windows:
            return  # No windows to switch to

        # Get the currently active window
        active_window = None
        for window in windows:
            if window == windows[1]:
                active_window = window
                break

        if not active_window:
            return  # No active window found

        # Find the next window in the list
        next_window = None
        for i, window in enumerate(windows):
            if window == active_window :
                next_window = windows[(i + self.WindowIndex) % len(windows)]
                # self.WindowIndex += 1
                break

        if next_window:
            next_window.set_focus()


    def moveMouse(self, x, y):
        """
        Moves the mouse cursor to the specified coordinates.

        Args:
            x (int): X-coordinate of the target position.
            y (int): Y-coordinate of the target position.
        """
        PyMouse().move(int(x), int(y))

    def scrollMouse(self, scrollY):
        """
        Scrolls the mouse wheel vertically by the specified amount.

        Args:
            scrollY (int): Amount to scroll vertically.
        """
        self.mouse.scroll(0, scrollY)

    def leftClick(self):
        """
        Simulates a left mouse button click.
        """
        self.mouse.leftClick(duration=0.008)
        self.mouse.sleep(0.008)


    def rightClick(self):
        """
        Simulates a right mouse button click.
        """
        self.mouse.rightClick(duration=0.008)

    def moveMouseFunction(self, x1, y1, z1):
        """
        Moves the mouse if the finger configuration corresponds to 'Move'.

        Args:
            x1 (float): X-coordinate of the finger tip.
            y1 (float): Y-coordinate of the finger tip.
            z1 (float): Z-coordinate of the finger tip.
        """
        if not all(self.fingers) and -z1 > -0.025:
            if self.fingers == self.fingerConfiguration['Move']:
                x3 = np.interp(x1, (self.frameR, self.wCam - self.frameR), (0, self.wScr))
                y3 = np.interp(y1, (self.frameR, self.hCam - self.frameR), (0, self.hScr))

                self.clocX = self.plocX + (x3 - self.plocX) / self.smoothening
                self.clocY = self.plocY + (y3 - self.plocY) / self.smoothening

                self.moveMouse(self.clocX, self.clocY)
                cv2.circle(self.img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                self.plocX, self.plocY = self.clocX, self.clocY

    def scrollMouseFunction(self, x1, y1):
        """
        Scrolls the mouse if the finger configuration corresponds to 'Scroll'.

        Args:
            fingers (list): List representing the status of each finger.
            x1 (float): X-coordinate of the finger tip.
            y1 (float): Y-coordinate of the finger tip.
            z1 (float): Z-coordinate of the finger tip.
        """
        if self.fingers == self.fingerConfiguration['Scroll'] and self.handType == 'Left':
            length1, self.img, lineInfo1 = self.detector.findDistance(8, 12, self.img)
            if length1 < 23:
                y3 = np.interp(y1, (self.frameR, self.hCam - self.frameR), (0, self.hScr))
                self.clocY = self.plocY + (y3 - self.plocY) / self.smoothening
                scrollY = int((self.clocY - self.plocY) / 30)  # Adjust divisor to reduce scroll amount
                if scrollY != 0:  # Only scroll if there's a noticeable movement
                    scrollY = (scrollY // abs(scrollY))
                    self.scrollMouse(-scrollY)
                cv2.circle(self.img, (lineInfo1[4], lineInfo1[5]), 5, (0, 255, 0), cv2.FILLED)

    def leftClickFunction(self):
        """
        Performs a left click if the finger configuration corresponds to 'LeftClick'.

        Args:
            fingers (list): List representing the status of each finger.
            x1 (float): X-coordinate of the finger tip.
            y1 (float): Y-coordinate of the finger tip.
            z1 (float): Z-coordinate of the finger tip.
        """
        if self.fingers[2:] == self.fingerConfiguration['LeftClick'][2:] and self.fingers[0] == self.fingerConfiguration['LeftClick'][0] and self.handType == 'Right':
            length, self.img, lineInfo = self.detector.findDistance(4, 8, self.img)
            if length < 20:
                cv2.circle(self.img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                if not self.isChanged:
                    self.leftClick()
                    self.isChanged = True
            else:
                self.isChanged = False
        
    def rightClickFunction(self):
        """Performs a right click if the finger configuration corresponds to 'RightClick'.

        Args:
            fingers (list): List representing the status of each finger.
            x1 (float): X-coordinate of the finger tip.
            y1 (float): Y-coordinate of the finger tip.
            z1 (float): Z-coordinate of the finger tip.
        """
        if self.fingers[3:] == self.fingerConfiguration['RightClick'][3:] and self.handType == 'Right':
            length, self.img, lineInfo = self.detector.findDistance(4, 12, self.img)
            if length < 20:
                cv2.circle(self.img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                self.rightClick()

    def ChangeWindowFuction(self):
        if self.fingers[1:] == [1,1,1,1] and self.handType == 'Left':
            length, self.img, lineInfo = self.detector.findDistance(4, 17, self.img)
            if length < 17:
                cv2.circle(self.img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                if not self.isChanged:
                    self.ChangeWindow()
                    self.isChanged = True
            else:
                self.isChanged = False


    def IsHandFliped(self,lmList):
        xof4,yof4,zof4 = lmList[1][1:]
        xof17,yof17,zof17 = lmList[17][1:]
        fliped = False
        upSide_down = False
        if self.handType == 'Right':
            if xof4 > xof17:
                fliped = True
        if self.handType == 'Left':
            if xof17 > xof4 :
                fliped = True
        if yof17 > yof4:
            upSide_down = True
        return fliped,upSide_down

    def run(self):
        """
        Main loop to capture video frames, detect hand landmarks, and perform
        corresponding mouse actions.
        """
        while True:
            # 1. Find hand Landmarks
            success, self.img = self.cap.read()
            self.img = cv2.flip(self.img, 1)
            self.img = self.detector.findHands(self.img)
            lmList, bbox = self.detector.findPosition(self.img)

            if lmList:
                # 2. Get the tip of the index finger
                x1, y1, z1 = lmList[8][1:]

                # 3. Check which self.fingers are up
                self.fingers, self.handType = self.detector.fingersUp()
                sfliped, up_down = self.IsHandFliped(lmList)
                # print(f'fliped: {sfliped} and Up_Down:{up_down}')

                if not sfliped and not up_down:
                    # Draw frame reduction rectangle
                    cv2.rectangle(self.img, (self.frameR, self.frameR),(self.wCam - self.frameR-50, self.hCam - self.frameR-50),(255, 0, 255), 2)
                    # 4. Move mouse if only the index finger is up
                    self.moveMouseFunction(x1, y1, z1)

                    # 5. Scroll if left hand's index and middle fingers are up
                    self.scrollMouseFunction( x1, y1)

                    # 6. Perform left click if right hand's thumb and index fingers are up
                    self.leftClickFunction( x1, y1)

                    # 7. Perform right click if right hand's thumb and all other fingers are up
                    self.rightClickFunction(x1, y1)

                    self.ChangeWindowFuction()

            # Frame Rate
            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            cv2.putText(self.img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.putText(self.img, f'hi', (600, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            # Display frame
            cv2.imshow("Image", self.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release capture and close all OpenCV windows
        self.cap.release()
        cv2.destroyAllWindows()

# Usage
if __name__ == "__main__":
    handMouseController = HandMouseController()
    handMouseController.run()
