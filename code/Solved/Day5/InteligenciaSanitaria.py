import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt


#######################################################
############# PREPARACIÓN DE DATOS ####################
#######################################################
# Leer archivo
todosDatos = pd.read_csv("COVID19MEXICOsmall.csv")

# Set de train con el 70% de todos los datos
trainD = todosDatos.sample(frac=0.7)
# Set de test con el 30% restante de datos (excluimos los que ya están en train)
testD = todosDatos.drop(trainD.index)

# Separamos datos de entrada del modelo en el set de train
entradasTrain = torch.tensor(trainD.drop('DEF', axis = 1).values).type(torch.FloatTensor)
# Y el valor que deberá de predecir nuestro modelo
objetivoTrain = torch.tensor(trainD['DEF'].values).type(torch.FloatTensor)

# Hacemos lo mismo para el set de test
entradasTest = torch.tensor(testD.drop('DEF', axis = 1).values).type(torch.FloatTensor)
objetivoTest = torch.tensor(testD['DEF'].values).type(torch.FloatTensor)

#######################################################
############# DEFINICIÓN DEL MODELO ###################
#######################################################
# Creamos la arquitectura de la red utilizando la estructura de PyTorch
class Red(nn.Module):
    def __init__(self):
        super(Red, self).__init__()
        # Función de activación sigmoide
        self.sigmoid = nn.Sigmoid()
        # Función de activación relu
        self.relu = nn.ReLU()
        # Función de activación tangente hiperbólica (tanh)
        self.tanh = nn.Tanh()
        # Capa de entrada
        self.capaEntrada = nn.Linear(17, 17*2)
        # Capa oculta
        self.capaOculta = nn.Linear(17*2, 17)
        # Capa de salida
        self.capaSalida = nn.Linear(17, 1)

    def forward(self, x):
        # Aplicamos la capa de entrada a los datos con una función de activación tanh
        x = self.tanh(self.capaEntrada(x))
        # Aplicamos la capa oculta con función relu
        x = self.relu(self.capaOculta(x))
        # Aplicamos finalmente la capa de salida
        x = self.capaSalida(x)
        return self.sigmoid(x) # Normalizamos al rango 0 <= x <= 1 la salida

# Creamos el modelo a partir de la arquitectura antes definida
red = Red()
# Definimos función de pérdida
lossFunction = nn.MSELoss()
# Definimos el optimizador y le indicamos qué paraámetros debe de actualizar
optimizer = optim.SGD(red.parameters(), lr=0.45)

#######################################################
############# ENTRENAMIENTO DEL MODELO ################
#######################################################
# Loop de entrenamiento #
epochs = 1000 # número de épocas a entrenar
for epoch in range(epochs):
    # Establecemos gradientes en cero
    optimizer.zero_grad()
    # Calculamos las predicciones de la red para los datos de entrada
    pred = red(entradasTrain)
    pred = pred.view(pred.size()[0]) # Reacomodamos para que tenga el mismo tamaño
    # Evaluamos el error entre las predicciones de la red y los objetivos reales
    perdida = lossFunction(pred, objetivoTrain)
    # Actualizamos los parámetros de la red
    perdida.backward() # Backpropagate
    optimizer.step() # Update params
    #print(f"epoch: {epoch} loss: {perdida}") # Muestra la pérdida en cada época
    # Gráfica inicial y final
    if epoch == 0 or epoch == epochs - 1:
        # Creamos un diccionario con los datos
        d = {'Obj': objetivoTrain.numpy(), 'Pred': pred.detach().numpy()}
        # Lo convertimos en un DataFrame
        df = pd.DataFrame(d)
        # Hacemos el boxplot de la predicción agrupado por el valor objetivo
        bp = df.boxplot(by="Obj", column="Pred")
        # Agregamos nombres de ejes y título
        [ax_tmp.set_xlabel('Objetivo') for ax_tmp in np.asarray(bp).reshape(-1)]
        [ax_tmp.set_ylabel('Predicción') for ax_tmp in np.asarray(bp).reshape(-1)]
        [ax_tmp.set_title('') for ax_tmp in np.asarray(bp).reshape(-1)]
        fig = np.asarray(bp).reshape(-1)[0].get_figure()
        fig.suptitle('Rendimiento en época ' + str(epoch + 1))
        # Mostramos la gráfica
        plt.show()

#######################################################
############# EVALUACIÓN DEL MODELO ###################
#######################################################
# Evaluamos en el set de test sin actualizar los gradientes de la red
with torch.no_grad():
    testPred = pred = red(entradasTest) # Obtenemos predicción
    testPred = testPred.view(testPred.size()[0])
    d = {'Obj': objetivoTest.numpy(), 'Pred': testPred.detach().numpy()}
    df = pd.DataFrame(d)
    bp = df.boxplot(by="Obj", column="Pred")
    [ax_tmp.set_xlabel('Objetivo') for ax_tmp in np.asarray(bp).reshape(-1)]
    [ax_tmp.set_ylabel('Predicción') for ax_tmp in np.asarray(bp).reshape(-1)]
    [ax_tmp.set_title('') for ax_tmp in np.asarray(bp).reshape(-1)]
    fig = np.asarray(bp).reshape(-1)[0].get_figure()
    fig.suptitle('Rendimiento set de test')
    plt.show()
