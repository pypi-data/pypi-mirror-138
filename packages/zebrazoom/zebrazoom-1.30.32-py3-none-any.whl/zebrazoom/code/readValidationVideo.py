from zebrazoom.code.getHyperparameters import getHyperparametersSimple
import cv2
import zebrazoom.videoFormatConversion.zzVideoReading as zzVideoReading
import json
import numpy as np
import sys
import tkinter as tk
import os
from pathlib import Path

def readValidationVideo(videoPath, folderName, configFilePath, numWell, numAnimal, zoom, start, framesToShow=0, ZZoutputLocation=''):
  
  root = tk.Tk()
  horizontal = root.winfo_screenwidth()
  vertical   = root.winfo_screenheight()

  cv2.namedWindow("press q to quit")
  cv2.moveWindow("press q to quit", 0, 0)
  cv2.resizeWindow("press q to quit", horizontal, vertical)
  
  s1  = "ZZoutput"
  s2  = folderName
  s3b = "results_"
  s4  = folderName
  s5  = ".avi"
  s5b = ".txt"
  
  cur_dir_path = os.path.dirname(os.path.realpath(__file__))
  initialPath  = Path(cur_dir_path)
  initialPath  = initialPath.parent
  initialPath  = os.path.join(initialPath, s1)
  if len(ZZoutputLocation):
    initialPath = ZZoutputLocation
  
  with open(os.path.join(initialPath, os.path.join(s2, 'configUsed.json'))) as f:
    configTemp = json.load(f)
  hyperparameters = getHyperparametersSimple(configTemp)
  
  if hyperparameters["copyOriginalVideoToOutputFolderForValidation"] and os.path.exists(os.path.join(initialPath, os.path.join(s1, os.path.join(s2, 'originalVideoWithoutAnyTrackingDisplayed_pleaseUseTheGUIToVisualizeTrackingPoints.avi')))):
    # The "exist" check above is only to insure compatibility with videos tracked prior to this update
    videoPath = os.path.join(initialPath, os.path.join(s2, 'originalVideoWithoutAnyTrackingDisplayed_pleaseUseTheGUIToVisualizeTrackingPoints.avi'))
  else:
    videoPath = os.path.join(initialPath, os.path.join(s2, s4 + s5))
  
  resultsPath = os.path.join(initialPath, os.path.join(s2, s3b + s4 + s5b))
  
  if not(os.path.exists(videoPath)):
    mypath = os.path.join(initialPath, s2)
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    resultFile = ''
    for fileName in onlyfiles:
      if '.avi' in fileName:
        resultFile = fileName
    videoPath = os.path.join(initialPath, os.path.join(s2, resultFile))

  if not(os.path.exists(resultsPath)):
    mypath = os.path.join(initialPath, s2)
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    resultFile = ''
    for fileName in onlyfiles:
      if 'results_' in fileName:
        resultFile = fileName
    resultsPath = os.path.join(initialPath, os.path.join(s2, resultFile))
  
  cap = zzVideoReading.VideoCapture(videoPath)
  
  nx    = int(cap.get(3))
  ny    = int(cap.get(4))
  max_l = int(cap.get(7))
  
  with open(resultsPath) as f:
    supstruct = json.load(f)

  if not("firstFrame" in supstruct):
    supstruct["firstFrame"] = 1
    print("supstruct['firstFrame'] not found")
  
  infoWells = []
  
  HeadX = np.zeros(max_l + supstruct["firstFrame"])
  HeadY = np.zeros(max_l + supstruct["firstFrame"])
  
  if ((numWell != -1) and (zoom)):
    lastEnd = 0
    lastXpos = supstruct["wellPoissMouv"][numWell][numAnimal][0]["HeadX"][0]
    lastYpos = supstruct["wellPoissMouv"][numWell][numAnimal][0]["HeadY"][0]
    for k in range(0,len(supstruct["wellPoissMouv"][numWell][numAnimal])):
      beg = supstruct["wellPoissMouv"][numWell][numAnimal][k]["BoutStart"]
      end = supstruct["wellPoissMouv"][numWell][numAnimal][k]["BoutEnd"]
      for l in range(lastEnd, beg):
        HeadX[l] = lastXpos
        HeadY[l] = lastYpos
      for l in range(beg, end):
        HeadX[l]  = supstruct["wellPoissMouv"][numWell][numAnimal][k]["HeadX"][l-beg]
        HeadY[l]  = supstruct["wellPoissMouv"][numWell][numAnimal][k]["HeadY"][l-beg]
      lastEnd = end
      lastXpos = supstruct["wellPoissMouv"][numWell][numAnimal][k]["HeadX"][end-1-beg]
      lastYpos = supstruct["wellPoissMouv"][numWell][numAnimal][k]["HeadY"][end-1-beg]
      
    for l in range(lastEnd, max_l + supstruct["firstFrame"]):
      HeadX[l] = lastXpos
      HeadY[l] = lastYpos
  
  # /* Getting the info about well positions */
  analyzeAllWellsAtTheSameTime = 0
  if (analyzeAllWellsAtTheSameTime == 0):
    for i in range(0, len(supstruct["wellPositions"])):
      x = 0
      y = 0
      lengthX = 0
      lengthY = 0
      rectangleWellArea = 1
      if (rectangleWellArea == 0): # circular wells
        x = supstruct["wellPositions"][i]["topLeftX"]
        y = supstruct["wellPositions"][i]["topLeftY"]
        r = supstruct["wellPositions"][i]["diameter"]
        lengthX = 300 # wellOutputVideoDiameter;
        lengthY = 300 # wellOutputVideoDiameter;
      else:
        x = supstruct["wellPositions"][i]["topLeftX"]
        y = supstruct["wellPositions"][i]["topLeftY"]
        lengthX = supstruct["wellPositions"][i]["lengthX"]
        lengthY = supstruct["wellPositions"][i]["lengthY"]
      if (x < 0):
        x = 0
      if (y < 0):
        y = 0
      infoWells.append([x, y, lengthX, lengthY])
  else:
    infoWells.append([0, 0, nx, ny])

  x = 0
  y = 0
  lengthX = 0
  lengthY = 0
  if (numWell != -1):
    x = infoWells[numWell][0]
    y = infoWells[numWell][1]
    lengthX = infoWells[numWell][2]
    lengthY = infoWells[numWell][3]
  else:
    lengthX = nx
    lengthY = ny
  
  l = 0
  
  if (start > 0):
      l = start - supstruct["firstFrame"] + 1
  
  xOriginal = x
  yOriginal = y
  
  imageWaitTime = 1
  
  if hyperparameters["copyOriginalVideoToOutputFolderForValidation"]:
    frameToPosToPlot = {}
    for frameNumber in range(l, max_l + 400):
      frameToPosToPlot[frameNumber] = []
    for numWell in range(0, len(supstruct["wellPoissMouv"])):
      for numAnimal in range(0, len(supstruct["wellPoissMouv"][numWell])):
        for numBout in range(0, len(supstruct["wellPoissMouv"][numWell][numAnimal])):
          boutStart = supstruct["wellPoissMouv"][numWell][numAnimal][numAnimal]["BoutStart"]
          for i in range(0, len(supstruct["wellPoissMouv"][numWell][numAnimal][numAnimal]["HeadX"])):
            if boutStart + i in frameToPosToPlot:
              if (type(framesToShow) != np.ndarray) or (framesToShow[boutStart + i][numWell]):
                xPos = int(supstruct["wellPositions"][numWell]["topLeftX"] + supstruct["wellPoissMouv"][numWell][numAnimal][numAnimal]["HeadX"][i])
                yPos = int(supstruct["wellPositions"][numWell]["topLeftY"] + supstruct["wellPoissMouv"][numWell][numAnimal][numAnimal]["HeadY"][i])
                frameToPosToPlot[boutStart + i].append([xPos, yPos])
  
  while (l < max_l + 400):
    
    cap.set(1, l )
    ret, img = cap.read()
    
    if hyperparameters["copyOriginalVideoToOutputFolderForValidation"]:
      if l in frameToPosToPlot:
        for pos in frameToPosToPlot[l]:
          cv2.circle(img, (pos[0], pos[1]), hyperparameters["trackingPointSizeDisplay"], (0, 255, 0), -1)
    
    if ((numWell != -1) and (zoom)):
      
      length = 250
      xmin = int(HeadX[l + supstruct["firstFrame"] - 1] - length/2)
      xmax = int(HeadX[l + supstruct["firstFrame"] - 1] + length/2)
      ymin = int(HeadY[l + supstruct["firstFrame"] - 1] - length/2)
      ymax = int(HeadY[l + supstruct["firstFrame"] - 1] + length/2)
      
      x = xmin + xOriginal
      y = ymin + yOriginal
      lengthX = xmax - xmin
      lengthY = ymax - ymin
      
      # This is new
      if True:
        if y <= 0:
          y = 0
        if x <= 0:
          x = 0
        if y + lengthY >= len(img):
          lengthY = len(img) - y - 1
        if x + lengthX >= len(img[0]):
          lengthX = len(img[0]) - x - 1
    
    if (numWell != -1):
      img = img[int(y):int(y+lengthY), int(x):int(x+lengthX)]
      if lengthX > 100 and lengthY > 100:
        progress = ( l / max_l ) * lengthX
        cv2.line(img, (0,int(lengthY-7)), (int(lengthX),int(lengthY-7)), (255,255,255), 10)
        cv2.circle(img, (int(progress), int(lengthY-6)), 5, (0, 0, 255), -1)
    else:
      if lengthX > 100 and lengthY > 100:
        progress = ( l / max_l ) * nx
        cv2.line(img,(0,ny-7),(nx,ny-7), (255,255,255), 10)
        cv2.circle(img, (int(progress), int(ny-6)), 5, (0, 0, 255), -1)
    
    if lengthX > 100 and lengthY > 100:
      font = cv2.FONT_HERSHEY_SIMPLEX
      cv2.putText(img,str(l + supstruct["firstFrame"] - 1),(int(lengthX-110), int(lengthY-30)),font,1,(0,255,0))
    else:
      blank_image = np.zeros((len(img)+30, len(img[0]), 3), np.uint8)
      blank_image[0:len(img), 0:len(img[0])] = img
      img = blank_image
      font = cv2.FONT_HERSHEY_SIMPLEX
      cv2.putText(img, str(l + supstruct["firstFrame"] - 1), (int(0), int(lengthY+25)), font, 1, (0,255,0))
    
    vertical2   = vertical   - vertical   * 0.12
    horizontal2 = horizontal - horizontal * 0.015
    if ( (lengthX > horizontal2) or (lengthY > vertical2) ):
      sinkFactor = 1
      sinkFactorX = horizontal2 / lengthX
      sinkFactorY = vertical2   / lengthY
      if (sinkFactorX > sinkFactorY):
        sinkFactor = sinkFactorY
      else:
        sinkFactor = sinkFactorX
      newX = lengthX * sinkFactor
      newY = lengthY * sinkFactor
      
      imgResized2 = cv2.resize(img,(int(newX),int(newY)))
      
    else:
      imgResized2 = img
    
    cv2.imshow("press q to quit", imgResized2)
    r = cv2.waitKey(imageWaitTime)
    
    if (r == 54) or (r == 100):
      l = l + 1
      imageWaitTime = 0
    elif (r == 52) or (r == 97):
      l = l - 1
      imageWaitTime = 0
    elif (r == 56) or (r == 119):
      l = l + 20
      imageWaitTime = 0
    elif (r == 50) or (r == 115):
      l = l - 20
      imageWaitTime = 0
    elif (r == 102):
      l = l - 100
      imageWaitTime = 0
    elif (r == 103):
      l = l - 50
      imageWaitTime = 0
    elif (r == 104):
      l = l + 50
      imageWaitTime = 0
    elif (r == 106):
      l = l + 100
      imageWaitTime = 0
    elif (r == 113):
      l = max_l+500
      cv2.destroyWindow("press q to quit")
      root.destroy()
    else:
      l = l + 1
    
    if ((l > max_l-1) and (l != max_l+500)):
      l = max_l-1

    if (l < 0):
      l = 0
