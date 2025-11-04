import os
import time
import math

# ANSI color codes
COLORS = [
    '\033[31m',  # Red
    '\033[33m',  # Yellow
    '\033[32m',  # Green
    '\033[36m',  # Cyan
    '\033[34m',  # Blue
    '\033[35m',  # Magenta
    '\033[37m',  # White
]
RESET = '\033[0m'  # Reset color

def render_donut(A, B):
    # Screen dimensions (larger ASCII grid)
    width = 80
    height = 40
    # Initialize z-buffer and screen buffer
    zbuffer = [0] * (width * height)
    screen = [' '] * (width * height)
    # Character set for shading (denser = closer)
    chars = '.,-~:;=!*#$@'

    # Torus parameters
    R1 = 1    # Torus tube radius
    R2 = 2    # Torus ring radius
    K2 = 5    # Distance from viewer to torus
    K1 = height * K2 * 3 / (6 * (R1 + R2))  # Adjusted projection scaling for larger grid

    # Precompute sines and cosines for rotation
    cosA, sinA = math.cos(A), math.sin(A)
    cosB, sinB = math.cos(B), math.sin(B)

    # Theta: angle around the tube
    for theta in range(0, 628, 8):  # 0 to 2pi, finer steps for larger grid
        costheta, sintheta = math.cos(theta / 100), math.sin(theta / 100)
        # Phi: angle around the torus
        for phi in range(0, 628, 8):
            cosphi, sinphi = math.cos(phi / 100), math.sin(phi / 100)

            # 3D coordinates of point on torus
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # Rotate around y-axis (A) and x-axis (B)
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z  # "One over z" for depth

            # Project 3D to 2D
            xp = int(width / 2 + K1 * ooz * x)
            yp = int(height / 2 - K1 * ooz * y)

            # Calculate luminance (lighting)
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            if L > 0:  # Only render front-facing points
                idx = xp + yp * width
                if 0 <= idx < len(zbuffer) and ooz > zbuffer[idx]:
                    zbuffer[idx] = ooz
                    luminance_index = int(L * 8)  # Map luminance to 0-7
                    screen[idx] = chars[min(luminance_index, len(chars) - 1)]

    # Build the frame with colors
    output = []
    for j in range(height):
        row = ''
        for i in range(width):
            idx = i + j * width
            char = screen[idx]
            # Assign color based on character (approximating depth)
            if char == ' ':
                row += char
            else:
                color_idx = min(ord(char) % len(COLORS), len(COLORS) - 1)
                row += COLORS[color_idx] + char + RESET
        output.append(row)
    return '\n'.join(output)

def main():
    A, B = 0, 0  # Rotation angles
    try:
        while True:
            # Clear terminal (works on Ubuntu)
            os.system('clear')
            # Render and print frame
            frame = render_donut(A, B)
            print(frame)
            # Update rotation angles
            A += 0.07  # Rotate around x-axis
            B += 0.03  # Rotate around y-axis
            # Control frame rate
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nStopped by user")
        os.system('clear')

if __name__ == "__main__":
    main()
