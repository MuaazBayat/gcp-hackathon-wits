import cv2
import numpy as np
import os
import random
import shutil

import os
import requests

# List of image URLs
image_urls = [
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62963095.jpg?alt=media&token=7fe3ab57-7ec8-404f-b53c-02600971974e",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62965392.jpg?alt=media&token=179fc516-c44a-4793-a9e7-80d84be803a5",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62967080.jpg?alt=media&token=8b9295e0-19ad-4364-b1fc-f048403dcaca",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62967094.jpg?alt=media&token=cdaf222e-9f56-49bc-b4d0-3f1965d1d3fb",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62967098.jpg?alt=media&token=9bf484ae-98f9-4e7f-ac4a-087ed28d61ae",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62967100.jpg?alt=media&token=4e78c5b2-6c60-4953-8896-a47e3e8d7376",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62967113.jpg?alt=media&token=a8c38048-f204-4745-85ae-e7740e5cd11b",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62967117.jpg?alt=media&token=833a34c2-4e47-49af-ad33-6f47affd192a",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62967124.jpg?alt=media&token=d080260f-e10d-4d7a-84c8-e6f74a270264",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62968356.jpg?alt=media&token=216acc7b-69ad-40f0-bd0d-2b288729f7aa",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62971459.jpg?alt=media&token=78ff7e0f-971a-4ed8-b678-815e2453283b",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62971883.jpg?alt=media&token=e7ed95ac-987c-4be3-8de3-efe14877ccb9",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62971885.jpg?alt=media&token=971af84b-2002-41ea-bd5a-4cd3b20c7573",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62974955.jpg?alt=media&token=677d4832-8228-4212-b73c-6e0ce7de4867",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62976343.jpg?alt=media&token=61c39240-3eeb-41cf-bf7c-345d0259fa4f",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62979234.jpg?alt=media&token=2f609a4a-38f0-4dd6-8658-7d04d229988f",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62979321.jpg?alt=media&token=d5dda534-4a6a-445d-a6c1-20c5d8a0c53a",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62979597.jpg?alt=media&token=2beef827-c3d0-42c9-8b64-6507e0c39424",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62984037.jpg?alt=media&token=5b370a09-9288-4d29-aaea-7310864a80e8",
    "https://firebasestorage.googleapis.com/v0/b/criminal-db-73ba9.appspot.com/o/62989004.jpg?alt=media&token=278ed771-b774-4f93-a78a-933f03d1496c"
]

# Create the 'testers' folder if it doesn't exist
os.makedirs("testers", exist_ok=True)

# Download and save each image
for url in image_urls:
    # Extract the image filename from the URL
    filename = os.path.basename(url).split("?")[0]
    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Save the image content to a file in the 'testers' folder
        with open(f"testers/{filename}", "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

print("All images have been downloaded.")


def add_random_noise(image):
    row, col, ch = image.shape
    mean = 0
    var = 0.1
    sigma = var**0.5
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    noisy = image + gauss * 255
    return noisy

def random_rotate(image):
    angle = random.randint(-30, 30)
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def random_scale(image):
    scale = random.uniform(0.5, 1.5)
    scaled = cv2.resize(image, None, fx=scale, fy=scale)
    return scaled

def random_translate(image):
    rows, cols, _ = image.shape
    max_trans = 50  # Max translation in pixels
    tx = random.randint(-max_trans, max_trans)
    ty = random.randint(-max_trans, max_trans)
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    translated = cv2.warpAffine(image, M, (cols, rows))
    return translated

def random_flip(image):
    flip_code = random.choice([-1, 0, 1])
    flipped = cv2.flip(image, flip_code)
    return flipped

def apply_random_transformations(image):
    transformations = [add_random_noise, random_rotate, random_scale, random_translate, random_flip]
    random.shuffle(transformations)
    for transform in transformations:
        image = transform(image)
    return image

# Input folder with all images
input_folder = 'testers'

i =4

# Folder for the first 10 images
first_10_folder = 'testers/batch-'+str(i)+'/first_10'
os.makedirs(first_10_folder, exist_ok=True)

# Folder for the remaining images
output_folder = 'testers/batch-'+str(i)+'/output'
os.makedirs(output_folder, exist_ok=True)

# List all image files in the input folder
all_images = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Separate the first 10 images and the rest
first_10_images = all_images[:10]
remaining_images = all_images[10:]

# Move the first 10 images to the first_10 folder
for filename in first_10_images:
    shutil.move(os.path.join(input_folder, filename), os.path.join(first_10_folder, filename))

# Move the remaining images to the output folder
for filename in remaining_images:
    shutil.move(os.path.join(input_folder, filename), os.path.join(output_folder, filename))

# Apply random transformations to images in the first_10 folder
for filename in os.listdir(first_10_folder):
    img_path = os.path.join(first_10_folder, filename)
    image = cv2.imread(img_path)
    transformed_image = apply_random_transformations(image)
    cv2.imwrite(img_path, transformed_image)

print("Images moved and transformations applied.")