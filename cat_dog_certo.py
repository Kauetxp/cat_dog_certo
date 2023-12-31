
# imports

import numpy as np
import os
import random
import matplotlib as plt
import pickle
import cv2

#Diretorio, categorias, tamanho

directory = "/workspaces/codespaces-blank/cat_dog_certo/datasets"
categories = ["cats","dogs"]
img_size = 100
data = []

#Arrumando as imagens

for category in categories:
    folder = os.path.join(directory, category)
    label = categories.index(category)
    for img in os.listdir(folder):
        img_path = os.path.join(folder, img)
        img_arr = cv2.imread(img_path)
        img_arr = cv2.resize(img_arr, (img_size, img_size))
        data.append([img_arr, label])

print(len(data))

#organizando os arrays
#pickle

random.shuffle(data)
x = []
y = []

for features, labels in data:
    x.append(features)
    y.append(labels)

x = np.array(x)
y = np.array(y)

print(len(x))
print(len(y))

pickle.dump(x, open('x.pkl','wb'))
pickle.dump(y, open('y.pkl','wb'))

x = pickle.load(open('x.pkl','rb'))
y = pickle.load(open('y.pkl','rb'))


x = x/255

#Importando o tensor flow

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

#Um monte de Model

model = Sequential()

model.add(Conv2D(64, (3,3), activation = 'relu'))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(64, (3,3), activation = 'relu'))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(64, (3,3), activation = 'relu'))
model.add(MaxPooling2D((2,2)))


model.add(Flatten())

model.add(Dense(128, input_shape = x.shape[1:], activation='relu'))

model.add(Dense(128, activation='relu'))

model.add(Dense(2, activation='softmax'))

model.compile(optimizer = 'adam', loss='sparse_categorical_crossentropy', metrics = ['accuracy'])

model.fit(x,y,epochs=5,validation_split=0.1, batch_size=32)

#TUDO ISSO QUE FOI FEITO ATÉ AGORA FOI A FASE DE TREINO

# Salvando o modelo já treinado


model.save("modelo_gato_cachorro.h5")

# Aqui eu estou chamando a rede neural

from keras.models import load_model
model = load_model("modelo_gato_cachorro.h5")

# Aqui o usuario irá colocar a imagem dele

image_path = input("Digite o caminho da imagem: ")

# arrumando a imagem
user_image = cv2.imread(image_path)
user_image = cv2.resize(user_image, (img_size, img_size))
user_image = user_image / 255.0

# Prevendo
predictions = model.predict(np.array([user_image]))
predicted_class = np.argmax(predictions)

if predicted_class == 0:
    result = "É um gato."
else:
    result = "É um cachorro."

print(result)