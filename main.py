from fastapi import FastAPI
from deepface import DeepFace
from typing import List
import json
import logging

app = FastAPI()

models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
  "GhostFaceNet",
]

@app.get("/")
async def root():
    return {"message": "Server is running..."}

@app.get("/match", tags=["Face Match"])
async def isMatch(input_url: str, check_url: str):
    """
    This function checks if two pictures are the same person
    """
    result = DeepFace.verify(
      img1_path = input_url,
      img2_path = check_url,
      model_name = models[5],
    )
    return {"result": result}

# Function to load URLs from a JSON file
def load_urls():
    with open("files.json", "r") as file:  # Adjust the path to where your JSON file is stored
        data = json.load(file)
    return data["images"]

@app.get("/find", tags=["Database Searching"])
def match(input:str):
    """
    This function checks for if a face exists in the database
    """
    urls = load_urls()
    for image in urls:
      result = DeepFace.verify(
      img1_path = input,
      img2_path = image,
      model_name = models[5])
      logging.info(f"Checking match on {image}...")
      if(result['verified']):
          return {"message": f"Person Found {image}"}
      logging.info("match not found")
    return {"message": "Processed all URLs, person not found"}


@app.get("/images")
def list_images():
    """
    Gets all the images in the database as an a json
    """
    urls = load_urls()
    return {"images": urls }

@app.get("/tests")
def run_tests():
    for model in models:
        print(model)
    
"""
Testing and model evaluations:

Models:
1. x
2. y
3. z

Testing Data:
16 - Innocent People (False)
8 - Criminals Std
8 - Criminals variance

For each model, 
  For each image in testing, we will search for a match
    if it correctly matched, we will score it.

"""