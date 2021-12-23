# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qVQO6l-EvXBuMZP7oGzOCNOLVEwdOUCJ
"""

from google.colab import drive
drive.mount('/content/gdrive')

!ls /content/gdrive/My\ Drive/Hw2

import numpy as np
import os
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

root = '/content/gdrive/My Drive/Hw2'

images_csv_path = os.path.join(root, 'images.csv')

#mean centering and then applying PCA

dataF = pd.read_csv(images_csv_path)
k = 10
X = dataF.to_numpy()
X_meanValue = np.mean(X, axis=0)
X_2 = X - X_meanValue

cov = np.cov(X_2.T)



eigen_values, eigen_vectors = np.linalg.eig(cov)
#p = np.size(eigen_vectors, axis=1) 


indices = eigen_values.argsort()[::-1]   
eigen_values = eigen_values[indices]
eigen_vectors = eigen_vectors[:,indices]



pve = eigen_values / np.sum(eigen_values)
num = k
arr = []
for j in range(num):
        arr.append(j+1)
#print()
#pve_trans = pve.transpose()*100
#plt.plot( arr , pve_trans)
#plt.title("PVE for k = {}".format(num))
#plt.ylabel('Variance (%)')
#plt.xlabel('PC (k)')
#plt.show()  

pveP = (pve[:k] * 100)
print()
plt.plot( arr , pveP) 
plt.title("PVE for k = {}".format(num))
plt.ylabel('Variance (%)')
plt.xlabel('PC (k)')
plt.show

pvePercent = (pve[:k] * 100)
print(pvePercent)

plt.bar(range(0, k), pvePercent, color = ["Green"])
plt.xlabel('Principle Components')
plt.ylabel('Proportion of Explained Variance')

#reconstruct the first image 
k_check = [500] 
for d in k_check:
  ev = eigen_vectors.T[:d, :]
  compressed = np.dot(X[0], ev.T)
  reconstruct = np.dot(compressed, ev) + X_meanValue
  plt.title("Principle Component Number = " + str(d))
  plt.imshow(reconstruct.reshape(48, 48), 'gray')

for i in range(10):
  plt.title("PCA Component " + str(i + 1))
  plt.imshow((eigen_vectors.T)[i].reshape(48, 48), 'gray')

"""Question 2 """

q2Features = os.path.join(root, 'question-2-features.csv')
q2Labels = os.path.join(root, 'question-2-labels.csv')
features = pd.read_csv(q2Features)
X = np.matrix(features)
res = np.dot(X.T, X)
rank = np.linalg.matrix_rank(res)
print(rank)

feature_LSTAT_original = pd.read_csv(q2Features, usecols=[12])
labels1 = pd.read_csv(q2Labels)

feature_LSTAT_toTranspose = feature_LSTAT_original.to_numpy()
labels = labels1.to_numpy()
feature_LSTAT = feature_LSTAT_toTranspose.T #Transposed

np.set_printoptions(threshold=np.inf) #not truncated form 

X_toTranspose = np.matrix(np.vstack((np.ones_like(feature_LSTAT), feature_LSTAT)))
Y = np.matrix(labels)
X = X_toTranspose.T

X_T = np.matmul(X.T, X_toTranspose.T)
inverse = np.linalg.inv(X_T)
check = inverse @ X.T
beta = check @ Y 
Y_1 = np.dot(X, beta)
Y_2 = np.array(Y_1)

b0 = beta[0][0]
print("b0: ", b0)
b1 = beta[1][0]
print("b1: ", b1)

MSE = np.square( np.abs(labels - Y_1))
#print(beta)
#print(MSE)
mse = sum(MSE)/len(MSE)
print("The MSE is: ")
print(float(mse))

plt.title('Plot 1: LSTAT vs Price ')
plt.xlabel('LSTAT')
plt.ylabel('Price')
plt.scatter(feature_LSTAT.T, labels)
plt.scatter(feature_LSTAT.T, Y_2)
plt.legend(['Actual Price', 'Predicted Price'])
plt.show

X_toTranspose = np.matrix(np.vstack((np.ones_like(feature_LSTAT), feature_LSTAT, np.square(feature_LSTAT))))
Y = np.matrix(labels)
X = X_toTranspose.T

X_T = np.matmul(X.T, X_toTranspose.T)
inverse = np.linalg.inv(X_T)

check = inverse @ X.T
beta = check @ Y
Y_1 = np.dot(X, beta)
Y_2 = np.array(Y_1)

b0 = beta[0][0]
print("b0: ", b0)
b1 = beta[1][0]
print("b1: ", b1)
b2 = beta[2][0]
print("b2: ", b2)

MSE = np.square(np.abs(labels-Y_1))
mse = sum(MSE)/len(MSE)
print("The MSE is: ")
print(float(mse))

plt.title('Plot 1: LSTAT vs Price ')
plt.xlabel('LSTAT')
plt.ylabel('Price')
plt.scatter(feature_LSTAT.T, labels)
plt.scatter(feature_LSTAT.T, Y_2)
plt.legend(['Actual Price', 'Predicted Price'])
plt.show

"""Question 3"""

q3TrainFeatures = os.path.join(root, 'question-3-features-train.csv')
q3TrainLabels = os.path.join(root, 'question-3-labels-train.csv')
q3TestFeatures = os.path.join(root, 'question-3-features-test.csv')
q3TestLabels = os.path.join(root, 'question-3-labels-test.csv')

trainFeatures = pd.read_csv(q3TrainFeatures)
testFeatures = pd.read_csv(q3TestFeatures)
testLabels = pd.read_csv(q3TestLabels)
trainLabels = pd.read_csv(q3TrainLabels)

#Normalize Features
#train features
df_X = trainFeatures
amount_arr = df_X["Pclass"].values
amount_arr = (amount_arr - np.mean(amount_arr)) / np.std(amount_arr)
df_X["Pclass"] = amount_arr

amount_arr = df_X["Age"].values
amount_arr = (amount_arr - np.mean(amount_arr)) / np.std(amount_arr)
df_X["Age"] = amount_arr

amount_arr = df_X["Fare"].values
amount_arr = (amount_arr - np.mean(amount_arr)) / np.std(amount_arr)
df_X["Fare"] = amount_arr

X = df_X.to_numpy()

#print(X)
#train labels
df_Y = trainLabels #not in matrix form 
Y = df_Y.to_numpy()

#test features 
df_X_test = testFeatures
amount_arr = df_X_test["Pclass"].values
amount_arr = (amount_arr - np.mean(amount_arr)) / np.std(amount_arr)
df_X_test["Pclass"] = amount_arr

amount_arr = df_X_test["Age"].values
amount_arr = (amount_arr - np.mean(amount_arr)) / np.std(amount_arr)
df_X_test["Age"] = amount_arr

amount_arr = df_X_test["Fare"].values
amount_arr = (amount_arr - np.mean(amount_arr)) / np.std(amount_arr)
df_X_test["Fare"] = amount_arr

test_X = df_X_test.to_numpy()

#test labels 
df_Y_test = testLabels #not in matrix form 
test_Y = df_Y_test.to_numpy()

def sigmoid(X):
  return 1 / (1 + np.exp(-X))

def fit(X, Y, lr, iters):
  learningRate = lr
  n_iterations = iters
  n_samples, n_features = X.shape 
  bias = 0
  weights = np.zeros(n_features)

  #gradient ascent
  for _ in range(n_iterations):
    linearModel = np.dot(X, weights) + bias # wx + b
    y_predicted = sigmoid(linearModel)

    #update weights and bias
    dw = (1/n_samples) * np.dot(X.T, y_predicted - Y)
    db = (1/n_samples) * np.sum(y_predicted - Y)

    weights -= learningRate * dw
    bias -= learningRate * db
    return weights, bias

def predict(X, weights, bias):
  linearModel = np.dot(X, weights) + bias
  y_predicted = sigmoid(linearModel)
  y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
  return np.array(y_predicted_cls)

def accuracy(y_true, y_pred):
  return np.sum(y_true == y_pred) / len(y_true)

def calcAccuracyMatrix(y_act, y_pred):
  TP = sum((y_act == 1) & (y_pred == 1))
  TN = sum((y_act == 0) & (y_pred == 0))
  FP = sum((y_act == 0) & (y_pred == 1))
  FN = sum((y_act == 1) & (y_pred == 0))
  return TP, TN, FP, FN

weightsCheck, biasCheck = fit(X, Y.ravel(), 0.0001, 1000)
predictions = predict(test_X, weightsCheck, biasCheck)
print("Logistic regression Accuracy: ", accuracy(test_Y.ravel(), predictions)*100)

TP, TN, FP, FN = calcAccuracyMatrix(test_Y.ravel(), predictions)
print("TP: ", TP, " ", "TN: ", TN, " ", "FP: ", FP, " ", "FN: ", FN)
print("")
precision = (TP / (TP + FP))
recall = (TP / (TP + FN) )
FPR = ( FP / (TP + FP) )
F1 =  (2 * precision * recall) / (precision + recall)
F2 =  (5 * precision * recall) / ((4 * precision) + recall)
FDR = ( FP / (FN + TN))
NPV = (TN / (FN + TN))
print( "Precision: ", precision*100)
print( "Recall: ", recall*100)
print( "FPR: ", FPR*100)
print( "FDR: ", FDR*100)
print( "NPV: ", NPV*100)
print( "F1: ", F1*100)
print( "F2: ", F2*100)