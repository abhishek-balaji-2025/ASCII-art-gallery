import os
import time
import math

# ANSI color codes
COLORS = [
    '\033[33m',  # Yellow (gold ring)
    '\033[37m',  # White (diamond sparkle)
    '\033[36m',  # Cyan (diamond highlight)
    '\033[32m',  # Green
    '\033[34m',  # Blue
    '\033[35m',  # Magenta
]
RESET = '\033[0m'  # Reset color

def render_ring(A, B):
    # Screen dimensions (large ASCII grid)
    width = 80
    height = 40
    # Initialize z-buffer and screen buffer
    zbuffer = [0] * (width * height)
    screen = [' '] * (width * height)
    # Character set for shading (denser = closer)
    chars = '.,-~:;=!*#$@'
    # Characters for diamond sparkle
    diamond_chars = '*^'

    # Ring parameters
    R1 = 0.5  # Ring thickness (thinner for band-like effect)
    R2 = 2.5  # Ring radius
    K2 = 5    # Distance from viewer to ring
    K1 = height * K2 * 3 / (6 * (R1 + R2))  # Projection scaling

    # Precompute sines and cosines for rotation
    cosA, sinA = math.cos(A), math.sin(A)
    cosB, sinB = math.cos(B), math.sin(B)

    # Theta: angle around the ring
    for theta in range(0, 628, 8):  # 0 to 2pi, finer steps
        costheta, sintheta = math.cos(theta / 100), math.sin(theta / 100)
        # Phi: angle around the band
        for phi in range(0, 628, 8):
            cosphi, sinphi = math.cos(phi / 100), math.sin(phi / 100)

            # 3D coordinates of point on ring
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # Rotate around y-axis (A) and x-axis (B)
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z  # Depth

            # Project 3D to 2D
            xp = int(width / 2 + K1 * ooz * x)
            yp = int(height / 2 - K1 * ooz * y)

            # Calculate luminance (lighting)
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            if L > 0:  # Front-facing points
                idx = xp + yp * width
                if 0 <= idx < len(zbuffer) and ooz > zbuffer[idx]:
                    zbuffer[idx] = ooz
                    luminance_index = int(L * 8)
                    screen[idx] = chars[min(luminance_index, len(chars) - 1)]

    # Add diamond (simplified as a point with sparkle)
    diamond_theta = 0  # Diamond at top of ring (theta=0)
    costheta, sintheta = math.cos(diamond_theta), math.sin(diamond_theta)
    diamond_r = R2 + R1  # Position on outer edge
    diamond_y = 0.5   # Slightly above ring
    for offset in [(-0.1, 0), (0.1, 0), (0, -0.1), (0, 0.1)]:  # Sparkle points around diamond
        circlex = diamond_r + offset[0]
        circley = diamond_y + offset[1]
        for phi in [0]:  # Single point for simplicity
            cosphi, sinphi = math.cos(phi), math.sin(phi)
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z
            xp = int(width / 2 + K1 * ooz * x)
            yp = int(height / 2 - K1 * ooz * y)
            if L > 0 and 0 <= xp < width and 0 <= yp < height:
                idx = xp + yp * width
                if ooz > zbuffer[idx]:
                    zbuffer[idx] = ooz
                    screen[idx] = diamond_chars[min(int(L * 2), len(diamond_chars) - 1)]

    # Build the frame with colors
    output = []
    for j in range(height):
        row = ''
        for i in range(width):
            idx = i + j * width
            char = screen[idx]
            if char == ' ':
                row += char
            else:
                # Color diamond sparkles white/cyan, ring yellow
                color_idx = 1 if char in diamond_chars else 0  # White for diamond, yellow for ring
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
            frame = render_ring(A, B)
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
