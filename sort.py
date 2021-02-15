"""
Ianto Cannon, 2021 Feb 15, Okinawa Japan.

Solves the mobile game "Water Sort Puzzle" by IEC Global Pty Ltd.

1. Input the colours as numbers in the array initVials using the following:
0=empty 1=darkBlue 2=darkGreen 3=lightBlue 4=purple 5=pink 
6=lightGreen 7=grey 8=orange 9=red 10=yellow 11=turquoise 12=brown.
Each row in the array is a vial. [0,0,0,0] is an empty vial.
The first element of the row is the topmost colour in the vial.

2. Run the code by entering "python sort.py" into your terminal.

3. After a series of random pours, this code will output a sequence of 
"donor vials" and "receiver vials" that completes the level.
"""
import numpy as np
import random as ran

initVials = np.array([[1,8,2,10],
                  [2,5,6,11],
                  [9,3,4,10],
                  [4,8,3,2],
                  [1,5,7,11],
                  [11,12,10,2],
                  [9,5,3,12],
                  [7,11,1,8],
                  [6,6,7,10],
                  [12,5,6,3],
                  [7,9,4,12],
                  [8,4,1,9],
                  [0,0,0,0],
                  [0,0,0,0]])

def pour(donVial,recVial):
  #tries to pour from donVial to recVial
  global vials
  pourQuant = 0
  recInd = 3
  donInd = 0
  if donVial == recVial:
    return 0
  for i in range(5):
    while vials[recVial, recInd] != 0:
      #receiving spot is full
      recInd = recInd - 1
      if recInd < 0:
        return pourQuant
    while vials[donVial, donInd] == 0:
      #donor spot is empty
      donInd = donInd + 1
      if donInd > 3:
        return pourQuant
    if recInd == 3 and max(vials[donVial, donInd:]) == min(vials[donVial, donInd:]):
      #pointless to pour 
      return pourQuant
    if recInd == 3 or vials[donVial, donInd] == vials[recVial, recInd + 1]:
      #pour
      vials[recVial, recInd] = vials[donVial, donInd]
      vials[donVial, donInd] = 0
      donInd = donInd + 1
      recInd = recInd - 1
      pourQuant = pourQuant + 1
      if donInd > 3 or recInd < 0:
        return pourQuant
    else:
      return pourQuant

def complete():
  #returns True if each of the vials contains a single color
  for testVial in range(np.shape(vials)[0]):
    if np.any(vials[testVial] != vials[testVial][0]):
      return False
  return True

def seqPour(don,rec):
  #sequentially try all pouring all of the vials, starting with vial "don" into vial "rec"
  global recPast, donPast
  for recDon in range(numVials*numVials):
    poured = pour(don,rec)
    if poured != 0:
      recPast = np.roll(recPast,1)
      donPast = np.roll(donPast,1)
      recPast[0] = rec
      donPast[0] = don
      return True
    rec = (rec + 1) % numVials
    if rec == don:
      don = (don -1) % numVials
  return False
  
def attempt():
  #try a random sequence of pours, until either
  #1 the level is complete
  #2 there are no possible pours
  #3 we have poured back and forth 4 times from the same two vials  
  global completed, repeatedPours, noPossPours
  maxPours = 100
  donHist = np.zeros(maxPours, dtype=int)
  recHist = np.zeros(maxPours, dtype=int)
  for sucPours in range(maxPours):
    don = ran.randrange(numVials)
    rec = ran.randrange(numVials)
    if seqPour(don,rec) == False:
      noPossPours = True
      print('noPoss ',sucPours)
      return False
    donHist[sucPours] = donPast[0]
    recHist[sucPours] = recPast[0]
    if complete() == True:
      completed = True
      print('level complete ')
      print('donor vials   ',donHist)
      print('receiver vials',recHist)
      return True
    if np.all(np.roll(recPast, 1) == donPast):
      repeatedPours = True
      print('repeat ', sucPours)
      return False
  print('tooManyPours ',sucPours)
      
def solver():
  #attempt the level many times with a different random sequence of pours
  global vials, recPast, donPast, completed, repeatedPours, noPossPours
  ran.seed(11)
  for restarts in range(30000):
    vials = np.copy(initVials)
    completed = False
    repeatedPours = False
    noPossPours = False
    recPast = np.zeros(4, dtype=int)
    donPast = np.arange(4, dtype=int)
    attempt()
    if completed == True:
      print('restarts ', restarts)
      return True

numVials = initVials.shape[0]
recPast = np.zeros(5, dtype=int)
donPast = np.arange(5, dtype=int)
vials = np.zeros((numVials,4), dtype=int)
completed = False
repeatedPours = False
noPossPours = False
solver()
