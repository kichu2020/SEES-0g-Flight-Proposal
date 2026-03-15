import numpy as np
import cv2
import os

def streaming_metrics(img_path, thresh=128, exclude_bins=2, lowfreq_ignore=5):

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {img_path}")

    mask = (img < thresh).astype(np.float32)

    y_raw = mask.sum(axis=1)
    y = y_raw - y_raw.mean()
    y = y * np.hanning(len(y))

    F = np.fft.rfft(y)
    mag = np.abs(F)

    mag[0] = 0.0
    if len(mag) > 2:
        mag[:2] = 0.0

    k_star = int(np.argmax(mag))
    peak = float(mag[k_star])

    noise_mask = np.ones_like(mag, dtype=bool)

    lo = max(0, k_star - exclude_bins)
    hi = min(len(mag), k_star + exclude_bins + 1)
    noise_mask[lo:hi] = False

    noise_mask[:min(lowfreq_ignore, len(mag))] = False

    if not np.any(noise_mask):
        noise_floor = float(np.median(mag[mag > 0])) if np.any(mag > 0) else 0.0
    else:
        noise_floor = float(np.median(mag[noise_mask]))

    snr = peak / (noise_floor + 1e-12)

    N = len(y_raw)
    period_px = (N / k_star) if k_star > 0 else float("inf")

    contrast = float(y_raw.std() / (y_raw.mean() + 1e-12))

    return {
        "period_px": float(period_px),
        "fft_peak_bin": int(k_star),
        "fft_peak_snr": float(snr),
        "contrast": float(contrast),
    }

if __name__ == "__main__":
    FILES = [
        "/Users/krishnanujam/Desktop/bead_strong_8.png",
        "/Users/krishnanujam/Desktop/bead_medium_8.png",
        "/Users/krishnanujam/Desktop/bead_weak_8.png",
    ]

    for f in FILES:
        if not os.path.exists(f):
            print(f"WARNING: path not found -> {f}")

    for f in FILES:
        print(f"\nMetrics for {f}:")
        print(streaming_metrics(f, thresh=128, exclude_bins=2, lowfreq_ignore=5))
