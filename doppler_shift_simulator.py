import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class DopplerSimulator:
    SPEED_OF_LIGHT = 3e8

    @staticmethod
    def compute_doppler(fc, v, angle):
        lam = DopplerSimulator.SPEED_OF_LIGHT / fc
        fd = (v / lam) * math.cos(math.radians(angle))
        received_frequency = fc + fd
        Tc = 1 / abs(fd) if fd != 0 else float('inf')
        fading_type = 'Fast Fading' if Tc < 0.01 else "Slow Fading"
        return lam, fd, received_frequency, Tc, fading_type

    @staticmethod
    def plot_fd_speed(fc, angle):
        lam = DopplerSimulator.SPEED_OF_LIGHT / fc
        angle = math.radians(angle)
        speeds = np.linspace(0, 100, 200)
        fd = (speeds / lam) * np.cos(angle)

        plt.figure()
        plt.plot(speeds, fd)
        plt.xlabel("Speed (m/s)")
        plt.ylabel("Doppler Shift (Hz)")
        plt.title("Doppler Shift vs Speed")
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_fd_angle(fc, speed):
        lam = DopplerSimulator.SPEED_OF_LIGHT / fc
        angles = np.linspace(0, 360, 300)
        fd = (speed / lam) * np.cos(np.radians(angles))

        plt.figure()
        plt.plot(angles, fd)
        plt.xlabel("Angle (Degree)")
        plt.ylabel("Doppler Shift (Hz)")
        plt.title("Doppler Shift vs Angle")
        plt.grid(True)
        plt.show()
