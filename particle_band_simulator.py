import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import time

H, W = 1200, 800
SAVE_PATH = "/Users/krishnanujam/Desktop/"


pattern_strength = 0.6
dispersion = 40
bead_size = 4
num_bands = 8


def generate_image(pattern_strength, dispersion, bead_size, num_bands):
    img = np.ones((H, W))  

    num_points = 120


    n_band = int(num_points * pattern_strength)
    n_uniform = num_points - n_band


    x_uniform = np.random.randint(0, W, n_uniform)
    y_uniform = np.random.randint(0, H, n_uniform)


    x_band = np.random.randint(0, W, n_band)


    bands = np.linspace(0.1 * H, 0.9 * H, num_bands)

    y_band = []
    points_per_band = max(1, n_band // num_bands)

    for center in bands:
        y_band.append(np.random.normal(center, dispersion, points_per_band))

    y_band = np.concatenate(y_band)
    y_band = np.clip(y_band.astype(int), 0, H - 1)


    x = np.concatenate([x_uniform, x_band])
    y = np.concatenate([y_uniform, y_band])

    for xi, yi in zip(x, y):
        rr = int(bead_size)

        x_min = max(0, xi - rr)
        x_max = min(W, xi + rr + 1)
        y_min = max(0, yi - rr)
        y_max = min(H, yi + rr + 1)

        xs = np.arange(x_min, x_max)
        ys = np.arange(y_min, y_max)
        Xs, Ys = np.meshgrid(xs, ys)

        mask = (Xs - xi)**2 + (Ys - yi)**2 <= rr**2

        img[y_min:y_max, x_min:x_max][mask] = 0  

    return img


current_img = generate_image(pattern_strength, dispersion, bead_size, num_bands)

fig, ax = plt.subplots(figsize=(6, 9))
plt.subplots_adjust(left=0.25, bottom=0.35)

img_display = ax.imshow(current_img, cmap='gray', vmin=0, vmax=1)
ax.axis('off')


ax_strength = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_disp = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_size = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_bands = plt.axes([0.25, 0.10, 0.65, 0.03])

slider_strength = Slider(ax_strength, 'Pattern Strength', 0, 1, valinit=pattern_strength)
slider_disp = Slider(ax_disp, 'Dispersion', 5, 150, valinit=dispersion)
slider_size = Slider(ax_size, 'Bead Size', 1, 10, valinit=bead_size)
slider_bands = Slider(ax_bands, 'Bands', 1, 10, valinit=num_bands, valstep=1)


def update(val):
    global current_img

    ps = slider_strength.val
    d = slider_disp.val
    bs = int(slider_size.val)
    nb = int(slider_bands.val)

    current_img = generate_image(ps, d, bs, nb)
    img_display.set_data(current_img)
    fig.canvas.draw_idle()


slider_strength.on_changed(update)
slider_disp.on_changed(update)
slider_size.on_changed(update)
slider_bands.on_changed(update)


ax_button = plt.axes([0.75, 0.9, 0.2, 0.06])
btn_save = Button(ax_button, 'Save Image')

def save_image(event):
    timestamp = int(time.time())
    filename = f"{SAVE_PATH}bead_image_{timestamp}.png"

    # save high resolution
    plt.imsave(filename, current_img, cmap='gray', vmin=0, vmax=1)

    print(f"Saved to: {filename}")


btn_save.on_clicked(save_image)


plt.show()
