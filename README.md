# HandMouseController

## Overview
The `HandMouseController` is a Python program that uses computer vision and hand tracking to control mouse movements and perform various actions on a computer. This tool leverages the `HandTrackingModule` for detecting hand landmarks and performs actions such as moving the mouse, scrolling, left-clicking, right-clicking, and switching windows based on specific hand gestures.

## Features
- **Mouse Movement**: Move the mouse cursor by pointing with the index finger.
- **Scrolling**: Scroll vertically using a specific finger configuration.
- **Left Click**: Perform a left mouse click using a specific finger configuration.
- **Right Click**: Perform a right mouse click using a specific finger configuration.
- **Window Switching**: Switch between open windows using a specific hand gesture.

## Requirements
- Python 3.x
- OpenCV (`cv2`)
- NumPy (`numpy`)
- `pynput` for keyboard control
- `pyautogui` for mouse control
- `pymouse` for additional mouse functionality
- `pywinauto` for window management
- `warnings` module to handle warnings

## Installation
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/Programmer118/Virtual-Mouse-Hand-Gesture.git
   cd Virtual-Mouse-Hand-Gesture
   ```

2. **Install Required Packages**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Program**:
   ```sh
   python AiVirtualMouse.py
   ```

## Usage
1. **Initialize the Controller**:
   The `HandMouseController` class is initialized with camera settings, frame reduction, and smoothing parameters.
   ```python
   handMouseController = HandMouseController()
   ```

2. **Run the Controller**:
   Start the main loop to capture video frames, detect hand landmarks, and perform corresponding mouse actions.
   ```python
   handMouseController.run()
   ```

## Hand Gestures
- **Move Mouse**: Raise the index finger.
- **Scroll**: Raise the index and middle fingers of the left hand.
- **Left Click**: Raise the thumb and index finger of the right hand.
- **Right Click**: Raise the thumb and all other fingers of the right hand.
- **Switch Window**: Raise all fingers of the left hand and close them together.

## Configuration
The finger configurations and actions are defined in the `fingerConfiguration` dictionary within the `HandMouseController` class:
```python
self.fingerConfiguration = {
    'Move': [0, 1, 0, 0, 0],
    "Scroll": [0, 1, 1, 0, 0],
    "LeftClick": [1, 1, 0, 0, 0],
    "RightClick": [1, 1, 1, 0, 0]
}
```

## Additional Notes
- The program uses `cv2.imshow` to display the video feed with the detected hand landmarks and actions being performed.
- To exit the program, press the 'q' key.

## Troubleshooting
- Ensure your webcam is properly connected and working.
- Adjust the frame reduction and smoothing parameters if the mouse movement is not smooth.
- Check the hand gestures and finger configurations if the actions are not being performed correctly.

## Contributions
Feel free to fork the repository and submit pull requests for any improvements or bug fixes.

## License
This project is licensed under the MIT License.

---

For any issues or questions, please open an issue on the [GitHub repository]((https://github.com/Programmer118/Virtual-Mouse-Hand-Gesture)).
