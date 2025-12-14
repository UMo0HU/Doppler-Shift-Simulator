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
        angle_rad = math.radians(angle)

        speeds = np.linspace(0, 100, 200)
        fd = (speeds / lam) * np.cos(angle_rad)

        plt.figure(figsize=(10, 5))
        plt.plot(speeds, fd, linewidth=2, label="Doppler Shift")
        plt.axhline(0, linestyle="--", linewidth=1, label="Zero Doppler")

        max_fd = np.max(fd)
        max_speed = speeds[np.argmax(fd)]

        plt.scatter(
            max_speed,
            max_fd,
            s=80,
            zorder=3,
            label="Max Doppler"
        )

        for s in [20, 50, 80]:
            plt.axvline(s, linestyle=":", alpha=0.5)

        plt.xlabel("Speed (m/s)")
        plt.ylabel("Doppler Shift (Hz)")
        plt.title("Doppler Shift vs Speed")

        plt.text(
            0.02, 0.95,
            f"Angle = {angle}°",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment="top"
        )

        # Grid & legend
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_fd_angle(fc, speed):
        lam = DopplerSimulator.SPEED_OF_LIGHT / fc
        angles = np.linspace(0, 360, 360)
        fd = (speed / lam) * np.cos(np.radians(angles))

        plt.figure(figsize=(10, 5))
        plt.plot(angles, fd, linewidth=2, label="Doppler Shift")
        plt.axhline(0, linestyle="--", linewidth=1, label="Zero Doppler")

        max_fd = np.max(fd)
        min_fd = np.min(fd)

        plt.scatter(
            [angles[np.argmax(fd)], angles[np.argmin(fd)]],
            [max_fd, min_fd],
            s=80,
            zorder=3,
            label="Max / Min Doppler"
        )

        for a in [0, 90, 180, 270]:
            plt.axvline(a, linestyle=":", alpha=0.6)

        plt.xlabel("Angle (Degree)")
        plt.ylabel("Doppler Shift (Hz)")
        plt.title("Doppler Shift vs Angle")

        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()
