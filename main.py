import numpy as np
import cv2

# IMG DOMINANT COLORS WITH CV2 CLUSTERING


def create_bar(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    # ahora le añadimos la data
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    return bar, (red, green, blue)


def max_width(width, height):
    factor = 950 * (100 / width)
    print(f"factorc1: {factor}")
    new_width = int(width * (factor / 100))
    new_height = int(height * (factor / 100))
    print(f"nuevo ancho: {new_width}")
    print(f"nuevo alto: {new_height}")
    img_resized = cv2.resize(img, (new_width, new_height))
    return [img_resized, new_width, new_height]


def max_height(width, height):
    factor = 550 * (100 / height)
    print(f"factorc2: {factor}")
    new_width = int(width * (factor / 100))
    new_height = int(height * (factor / 100))
    print(f"nuevo ancho: {new_width}")
    print(f"nuevo alto: {new_height}")
    img_resized = cv2.resize(img, (new_width, new_height))
    return [img_resized, new_width, new_height]


img = cv2.imread("img/berserk.jpg")


# resize basado en tamaño inicial:


height, width, _ = np.shape(img)
max_size = [950, 550]  # x,y

print(f" ancho: {width}")
print(f" alto: {height}")

if width < max_size[0] and height <= max_size[0]:
    new_width = width
    new_height = height
    img_data = [img, new_width, new_height]
if width > max_size[0] and height <= max_size[1]:
    img_data = max_width(width, height)

if width <= max_size[0] and height > max_size[1]:
    img_data = max_height(width, height)

if width > max_size[0] and height > max_size[1]:
    # who is further from his max size
    comparison = [(width - 950), (height - 550)]
    if comparison[0] > comparison[1]:  # use width > max_size function
        img_data = max_width(width, height)
    if comparison[0] < comparison[1]:  # use height > max_size function
        img_data = max_height(width, height)


data = np.reshape(img_data[0], (img_data[2] * img_data[1], 3))
data = np.float32(data)

# CLUSTERING
number_clusters = 6
# cuando se cumpla cualquiera de las 2 termina
criteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    10,
    1.0,
)  # 10: iteraciones, 1.0: epsilon
flags = cv2.KMEANS_RANDOM_CENTERS  # los centros se toman de forma aletoria

compactness, labels, centers = cv2.kmeans(
    data, number_clusters, None, criteria, 5, flags
)

# print(centers) #Colores dominantes

# Creacion segunda barra con colores
bars = []
rgb_values = []

for index, row in enumerate(centers):
    bar, rgb = create_bar(int(img_data[1] / 6), int(img_data[1] / 6), row)
    bars.append(bar)
    rgb_values.append(rgb)

img_bar = np.hstack(bars)  # stackeamos la barra de colores
height1, width1, _1 = np.shape(img_bar)

print(height, width)
print(height1, width1)

img_bar = cv2.resize(img_bar, (img_data[1], height1))

final_img = np.concatenate((img_data[0], img_bar), axis=0)

cv2.imshow("Dominant Collors Final", final_img)

cv2.waitKey(0)