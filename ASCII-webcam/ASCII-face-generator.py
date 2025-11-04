import cv2
import numpy as np
import os
import time
from PIL import Image

# ANSI color codes
COLORS = [
    '\033[37m',  # White
    '\033[36m',  # Cyan
    '\033[34m',  # Blue
    '\033[32m',  # Green
    '\033[33m',  # Yellow
    '\033[31m',  # Red
]
RESET = '\033[0m'

def image_to_ascii(image, width=100, height=50):
    try:
        # Resize image to fit terminal
        image = image.resize((width, int(height * image.size[1] / image.size[0] * width / height)))
        image = image.convert('L')  # Convert to grayscale
        pixels = np.array(image)
        chars = ' .,:;irsXA253hMHGS#9B&@'  # ASCII characters (denser = brighter)
        ascii_image = []
        for i in range(height):
            row = ''
            for j in range(width):
                pixel = pixels[i, j]
                char_index = int(pixel / 255 * (len(chars) - 1))
                color_index = int(pixel / 255 * (len(COLORS) - 1))
                row += COLORS[color_index] + chars[char_index] + RESET
            ascii_image.append(row)
        return '\n'.join(ascii_image)
    except Exception as e:
        return f"Error processing image: {e}"

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(2)  # Default webcam
    if not cap.isOpened():
        print("Error: Could not open webcam. Ensure it is connected and accessible.")
        print("Try: sudo apt install cheese && cheese to test camera.")
        return

    try:
        # Check terminal size
        term_cols, term_rows = os.get_terminal_size().columns, os.get_terminal_size().lines
        if term_cols < 100 or term_rows < 50:
            print(f"Warning: Terminal size ({term_cols}x{term_rows}) is small. Resize to at least 100x50 for best results.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame. Check webcam connection.")
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            ascii_art = image_to_ascii(image, width=100, height=50)
            if "Error" in ascii_art:
                print(ascii_art)
                break
            os.system('clear')  # Clear terminal
            print(ascii_art)
            time.sleep(0.1)  # 10 FPS for smooth display
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        os.system('clear')

if __name__ == "__main__":
    main()
