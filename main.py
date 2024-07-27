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
    return {"message": "Hello World"}

@app.get("/match")
async def isMatch(input_url: str, check_url: str):
    result = DeepFace.verify(
      img1_path = input_url,
      img2_path = check_url,
      model_name = models[5],
    )
    """
    {
    img1: "brad01",
    img2: "jason01",
    }
    """
    return {"result": result}

bucket_name = "criminal-db-73ba9.appspot.com"

# Function to load URLs from a JSON file
def load_urls():
    with open("files.json", "r") as file:  # Adjust the path to where your JSON file is stored
        data = json.load(file)
    return data["images"]

def get_urls():
    urls = load_urls()
    print(urls)

@app.get("/match/", tags=["URLs"])
def match(input:str):
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

@app.get("/images/", response_model=List[str])
def list_images():
    """
    Gets all the images in the database as an a json
    """
    urls = load_urls()
    return {"images": urls }
    
@app.get("/find")
async def findInDB(image_path: str):
  dfs = DeepFace.find(
    img_path = image_path, 
    db_path = "faces",
  )
  return {"result": dfs}