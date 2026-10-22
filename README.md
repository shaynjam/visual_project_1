# ASCII Motion Highlighter(Ai was used to guide me, all the code is written by me, Ai was only used as a guidance/mentor since this is a learnign project)

live webcam feed, redrawn as ASCII characters in the terminal, where **only the parts that move light up**
Built with Python, OpenCV and NumPy. This was a personal growth project: my first time working with video frames, and my first time profiling why something was slow and fixing it.

## How it works

For every webcam frame:

1. Read the frame and mirror it (`cv2.flip`).
2. Convert it to grayscale and shrink it to **200 x 80** (one pixel per character cell).
3. Subtract the previous frame (`cv2.absdiff`) to see how much each pixel changed.
4. Threshold out tiny changes (`cv2.threshold`, `THRESH_TOZERO`) to remove camera noise.
5. Boost the contrast of what's left (`cv2.convertScaleAbs`, `alpha=1.5`).
6. Map each value to a character from a density ramp and print the whole frame in place.

```python
chars = np.asarray(list(" .:-=+*#%@"))   # light -> dense

diff = cv2.absdiff(curr_small, prev_small)                 # how much each pixel changed
_, diff = cv2.threshold(diff, 25, 255, cv2.THRESH_TOZERO)  # ignore tiny changes (noise)
diff = cv2.convertScaleAbs(diff, alpha=1.5)                # boost contrast of motion

final_pixel = ((diff / 255) * (len(chars) - 1)).astype(int)        # value -> ramp index
output = "\n".join("".join(row) for row in chars[final_pixel])
print("\033[H" + output, end="", flush=True)               # cursor to top-left, redraw in place
```

## What I learned

### 1. Turning pixels into characters

The first hurdle was deciding which character goes where. I used a **"light to dense" ASCII ramp**, a string of characters ordered by how much of the cell they fill. A `.` covers only a few percent of the cell, while `@` covers far more. In a dark terminal, a denser character looks brighter, so brightness can be mapped to density.

To do that I needed each pixel's brightness. `cap.read()` returns a frame, which is a 3D array holding every pixel's colour values (in OpenCV the order is **B, G, R**). Converting it to **grayscale** collapses this into a 2D array with a single value per pixel, from 0 (black) to 255 (white). That value is then scaled to an index into the ramp: the brightest (most changed) pixels get the densest characters.

### 2. Colour vs. monochrome

I started with colour because it looked more "natural". But the colour version used a `for` loop that ran for every one of the 200 x 80 = 16,000 pixels, building the output string piece by piece. The terminal struggled to display motion smoothly and was clearly slower than the monochrome version. And after all that cost, the colour barely showed up in the output, so it wasn't worth it. I dropped colour.

### 3. NumPy instead of per-pixel loops

To smooth things further I learnt NumPy. Instead of looping over each pixel in Python, I let NumPy turn the **whole** frame into characters in one step:

```python
final_pixel = ((diff / 255) * (len(chars) - 1)).astype(int)
chars[final_pixel]
```

One line replaces the nested loop. In hindsight the real bottleneck was the Python loop, not the colour itself, which means colour could probably come back cheaply with a vectorised approach (see "What's next").

### 4. The output is just the difference between frames

What gets printed isn't the camera image itself, it's the **difference between the current and previous frame**:

- `cv2.absdiff` takes the *absolute* difference. This matters: frames are `uint8`, so plain subtraction can't go negative. It wraps around (in NumPy) or clips to 0 (`cv2.subtract`), either of which gives wrong results when the new frame is darker than the old one. `absdiff` handles both directions.
- `cv2.threshold(..., 25, ..., THRESH_TOZERO)` zeroes out any pixel that changed by 25 or less, filtering sensor noise and tiny lighting flicker.
- `cv2.convertScaleAbs(..., alpha=1.5)` multiplies by 1.5 (clipping at 255) to boost the contrast of real motion.

## Run it

```bash
pip install opencv-python numpy
python motion_tracker.py
```

- Press `q` (with the preview window focused) to quit.
- The output is 200 x 80 characters. Maximise your terminal and zoom out (`Ctrl` + `-` in VS Code) until it fits, or it will wrap and look garbled.
- Use a dark terminal theme. On a light theme the brightness mapping looks inverted.
  

## What's next
- [ ] Turn motion *highlighting* into motion *tracking*: find the largest moving blob, draw its centroid and a trail
- [ ] Gesture recognition with a small scikit-learn classifier trained on my own recordings
- [ ] Show a live FPS counter
