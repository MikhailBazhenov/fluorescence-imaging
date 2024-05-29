# This is a batch image measurement program (BIMP-F),
# that was used for assessing the area of increased fluorescence on plant leaves,
# induced by droplets of bentazone herbicide

import os
import sys
import subprocess


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


positive_responses = ['Y', 'y']
try:
    import cv2
except:
    response_1 = input('There is no <cv2> library on computer. Do you want to install it? (Y/N): ')
    if response_1 in positive_responses:
        install('cv2')
    else:
        exit()
    import cv2

try:
    import numpy as np
except:
    response_2 = input('There is no <numpy> library on computer. Do you want to install it? (Y/N): ')
    if response_2 in positive_responses:
        install('numpy')
    else:
        exit()
    import numpy as np

try:
    import matplotlib.pyplot as plt
except:
    response_3 = input('There is no <matplotlib> library on computer. Do you want to install it? (Y/N): ')
    if response_3 in positive_responses:
        install('matplotlib')
    else:
        exit()
    import matplotlib.pyplot as plt


response_4 = input('''The images will be masked to find the boundaries of spots with increased intensity.
All that is below (Mean + A * Standard_Deviation) will be shown black.
The default A is 1.2. Do you want to change the A coefficient? (Y/N): ''')
a = 1.2
if response_4 in positive_responses:
    a = float(input('Input A coefficient (example -1.5): '))
    print('A coefficient now is: ' + str(a))
response_5 = input('Do you want to write masked images into files? (Y/N) ')
if response_5 in positive_responses:
    write_masked_images = True
else:
    write_masked_images = False
response_6 = input('Do you want to invert images? (Y/N): ')
if response_6 in positive_responses:
    inverting = True
else:
    inverting = False
n = 0

while True:
    suffix = ''
    if n > 0:
        suffix = str(n)
    if not os.path.exists('plots' + suffix):
        os.mkdir('plots' + suffix)
        hist_folder = 'plots' + suffix
        break
    else:
        n += 1

n = 0

while True:
    suffix = ''
    if n > 0:
        suffix = str(n)
    if not os.path.exists('output' + suffix + '.txt'):
        f1 = open('output' + suffix + '.txt', 'w')
        break
    else:
        n += 1

drawing = False
points = []
plt.clf()

def draw_polygon(event, x, y, flags, param):
    global drawing, points, image

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points = [(x, y)]
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x, y))
            pts = np.array(points, np.int32)
            cv2.polylines(image, [pts], isClosed=False, color=(255, 0, 0), thickness=2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


files = os.listdir()
counter = 0
print('''Circle the ROI and press:
m - to make measurement
d - to dismiss ROI
n - to go to the next image
p - to go to previous image
q - to quit the program
''')

image_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
image_files = []
for file in files:
    if (file[-4:] in image_extensions) and ('masked_' not in file):
        image_files.append(file)

n = 0

while True:
    if n >= len(image_files):
        break
    file = image_files[n]
    print(file)
    image = cv2.imread(file)
    if inverting:
        image = 255 - image  # inverting image
    # Making the mask
    image_data = np.array(image)
    image_masking_limit = int(image_data.mean() + a * image_data.std())
    # image_masking_limit = 130
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    smoothed_image = cv2.GaussianBlur(gray_image, (9, 9), 6)
    mask = cv2.inRange(smoothed_image, image_masking_limit, 255)
    image = cv2.bitwise_and(image, image, mask=mask)
    if write_masked_images:
        cv2.imwrite('masked_' + file, image)
    clone = image.copy()
    max_width = 800
    max_height = 600
    scale = 1
    if image.shape[1] > max_width or image.shape[0] > max_height:
        scale = min(max_width / image.shape[1], max_height / image.shape[0]) * 1.7
        image = cv2.resize(clone, None, fx=scale, fy=scale)

    cv2.namedWindow('Image')
    cv2.moveWindow('Image', 300, 50)
    cv2.setMouseCallback('Image', draw_polygon)

    while True:
        cv2.imshow('Image', image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('m'):  # make measurement
            if len(points) > 2:
                mask = np.zeros(clone.shape[:2], dtype=np.uint8)
                points_multiplied = []

                for i in points:
                    points_multiplied.append((int(i[0] / scale), int(i[1] / scale)))
                pts = np.array(points_multiplied, np.int32)
                cv2.fillPoly(mask, [pts], (255, 255, 255))

                result = cv2.bitwise_and(clone, clone, mask=mask)
                gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
                reshaped = result.reshape((-1, 3)).transpose()
                gray = np.mean(reshaped, axis=0)
                gray_mean = np.mean(gray[gray > 0])
                gray_median = np.median(gray[gray > 0])
                gray_std = np.std(gray[gray > 0])
                gray_n = np.count_nonzero(gray)
                red = reshaped[0]
                green = reshaped[1]
                blue = reshaped[2]
                red_mean = np.mean(red[red > 0])
                red_median = np.median(red[red > 0])
                red_std = np.std(red[red > 0])
                red_n = np.count_nonzero(red)
                green_mean = np.mean(green[green > 0])
                green_median = np.median(green[green > 0])
                green_std = np.std(green[green > 0])
                green_n = np.count_nonzero(green)
                blue_mean = np.mean(blue[blue > 0])
                blue_median = np.median(blue[blue > 0])
                blue_std = np.std(blue[blue > 0])
                blue_n = np.count_nonzero(blue)

                if counter == 0:
                    print('sample\tfile\tmean\tmedian\tstd\tpixels\t'
                          'red_mean\tred_median\tred_std\tred_pixels\t'
                          'green_mean\tgreen_median\tgreen_std\tgreen_pixels\t'
                          'blue_mean\tblue_median\tblue_std\tblue_pixels')
                    f1.write('sample\tfile\tmean\tmedian\tstd\tpixels\t'
                             'red_mean\tred_median\tred_std\tred_pixels\t'
                             'green_mean\tgreen_median\tgreen_std\tgreen_pixels\t'
                             'blue_mean\tblue_median\tblue_std\tblue_pixels\n')
                counter += 1
                print(str(counter) + '\t' + file + '\t' +
                      str(gray_mean) + '\t' + str(gray_median) + '\t' + str(gray_std) + '\t' + str(gray_n) + '\t' +
                      str(red_mean) + '\t' + str(red_median) + '\t' + str(red_std) + '\t' + str(red_n) + '\t' +
                      str(green_mean) + '\t' + str(green_median) + '\t' + str(green_std) + '\t' + str(green_n) +
                      '\t' + str(blue_mean) + '\t' + str(blue_median) + '\t' + str(blue_std) + '\t' + str(blue_n))
                f1.write(str(counter) + '\t' + file + '\t' +
                         str(gray_mean) + '\t' + str(gray_median) + '\t' + str(gray_std) + '\t' + str(gray_n) + '\t' +
                         str(red_mean) + '\t' + str(red_median) + '\t' + str(red_std) + '\t' + str(red_n) + '\t' +
                         str(green_mean) + '\t' + str(green_median) + '\t' + str(green_std) + '\t' + str(green_n) +
                         '\t' + str(blue_mean) + '\t' + str(blue_median) + '\t' + str(blue_std) + '\t' + str(blue_n)
                         + '\n')
                plt.hist(gray_result[gray_result > 0], bins=32, color='skyblue', edgecolor='black')
                plt.savefig(hist_folder + '/fig' + str(counter) + '.png')
                plt.clf()
            image = cv2.resize(clone, None, fx=scale, fy=scale)
        if key == ord('n'):  # next image
            n += 1
            break
        if key == ord('p'):  # previous image
            n -= 1
            break
        if key == ord('d'):  # dismiss ROI
            image = cv2.resize(clone, None, fx=scale, fy=scale)
        if key == ord('q'):  # quit
            f1.close()
            cv2.destroyAllWindows()
            exit()
    cv2.destroyAllWindows()
f1.close()
