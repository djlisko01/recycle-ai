#---------Imports
from matplotlib import patheffects
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
import numpy as np
from PIL import Image
import os
import time
import cv2
#---------End of imports

class RecyclePredict:

  def __init__(self) -> None:
    """ Creates Recycle Predict Object """
    torch.cuda.empty_cache() # Releases all unoccupied cached memory - won't free GPU
    self.model = None
    self.device = None
    self.prediction = None
    self.probabilities = None

  def prep_model(self, classes):
    """ This Preps the ResNet18 Model, which the classes were
     trained on and then the pushes the model to the GPU if it's available."""

    self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Loading to {self.device}")
    self.model = torchvision.models.resnet18(pretrained=True)
    print(f"Pushing Resnet18 Model to {self.device}")
    self.model.fc = torch.nn.Linear(512, len(classes))
    self.model.to(self.device)
    print("Done...")

  def load_trained_model(self, trained_path):
    """ Load's trained model garabage classification dataset """
    print("Loading Your Trained Dataset")
    self.model.load_state_dict(torch.load(trained_path))
    self.model = self.model.eval()
    print("Done...")


  def preprocess_image(self,image):
    """ Converts the Image to a tensor object and pushes it the GPU if it's available """
    print("Preping Image for Prediction")
    # mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
    # std = torch.Tensor([0.229, 0.224, 0.225]).cuda()

    image = transforms.functional.to_tensor(image).to(self.device)
    # image.sub_(mean[:, None, None]).div_(std[:, None, None])
    print("Done...")
    return image[None, ...]

  def get_probabilities(self, image):
    """ Returns the prediction probabilities """
    with torch.no_grad():
      print("Get Probs...")
      output = self.model(image)
      self.probabilities = F.softmax(output, dim=1).detach().cpu().numpy().flatten()
    return self.probabilities

  def get_prediction(self):
    """ Return's the preduction, which is the calss witht the highest probability """
    if self.get_probabilities:
      print(("Get Prediction..."))
      self.prediction = self.probabilities.argmax()
    
    return self.prediction

  def test_predict(self):

    print("Making Test Prediction - to speed up predictor during live run.")
    img_path = "../data/testing_data/test/cardboard/cardboard381.jpg"
    img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
    img = cv2.resize(img, (224, 224))
    img = Image.fromarray(img)
    img = self.preprocess_image(img)

    print("Probabilites for test")
    print(self.get_probabilities(img))
    print("Test Prediction:", self.get_prediction())

    print("Test Prediction Done...")

  

  
  def __del__(self):
    """ Clears the cache after closing the program """

    print("Removing Model From GPU")
    torch.cuda.empty_cache()
    print("Program Closed")
  

############## Quick Test to See if the Program Works  - Comment out when running JetCam Live App ###################
# import cv2

# RECYCLE_TYPE = ["Cardbrd", "Glass", "Metal", "Paper", "Plastic", "Trash"]

# # Load Saved Images
# crbd_path = "data/testing_data/test/cardboard"
# list_imgs = os.listdir(crbd_path)

# path = "data/resnet18_recycle_train.pth"

# test = RecyclePredict()

# start_time = time.time()
# test.prep_model(RECYCLE_TYPE)
# end_time = time.time()
# print("Time to Load ResNet:", (end_time - start_time))

# start_time = time.time()
# test.load_trained_model(path)
# end_time = time.time()
# print("Time to Load Trained Model:", (end_time - start_time))
# print("* " * 50)

# correct_pred = []
# wrong_pred = []

# for img in list_imgs:
#   img_path = crbd_path + "/" + img
#   # Converts to Tensor Format 
#   img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
#   img = cv2.resize(img, (224, 224))
#   img = Image.fromarray(img)
#   img = test.preprocess_image(img)

#   print("Shape", img.shape)


#   # Makes Prediction
#   start_time = time.time()
#   print(test.get_probabilities(img))

#   i = test.get_prediction()
#   if RECYCLE_TYPE[i] == RECYCLE_TYPE[0]:
#     correct_pred.append(RECYCLE_TYPE[i])
#   else:
#     wrong_pred.append(RECYCLE_TYPE[i])
  
#   end_time = time.time()
#   print(RECYCLE_TYPE[i])
#   print("Time to Predict:", (end_time - start_time))

