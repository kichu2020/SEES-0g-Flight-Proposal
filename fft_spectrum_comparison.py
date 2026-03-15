import numpy as np
import cv2
import matplotlib.pyplot as plt

def compute_fft_magnitude(img_path, thresh=128):

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(img_path)

    mask = (img < thresh).astype(np.float32)

    y = mask.sum(axis=1)
    y = y - y.mean()
    y = y * np.hanning(len(y))

    F = np.fft.rfft(y)
    mag = np.abs(F)

    mag[0] = 0
    mag[:2] = 0
    k_star = np.argmax(mag)
    print(k_star)

    return mag

FILES = {
    "Weak": "/Users/krishnanujam/Desktop/bead_weak_8.png",
    "Medium": "/Users/krishnanujam/Desktop/bead_medium_8.png",
    "Strong": "/Users/krishnanujam/Desktop/bead_strong_8.png",
}

colors = {
    "Weak": "red",
    "Medium": "orange",
    "Strong": "green",
}

plt.figure(figsize=(8,5))

for label, path in FILES.items():
    mag = compute_fft_magnitude(path)
    plt.plot(mag, label=label, color=colors[label], linewidth=2)

plt.xlim(0, 200)
plt.title("FFT Magnitude Spectrum Comparison")
plt.xlabel("Spatial Frequency (FFT bin)")
plt.ylabel("Magnitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("fft_comparison_overlay.png", dpi=300)
plt.show()
