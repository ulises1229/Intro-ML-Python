from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Modelo SIR
def sir(y, t, beta, gamma):
    S, I, R, C = y
    N = S+I+R # Población total
    infectados = beta*I*S/N # Nuevos infectados
    removidos = gamma*I # Nuevos removidos
    dydt = [-infectados, infectados-removidos, removidos, infectados]
    return dydt

# Parámetros de simulación
beta = 0.52 # probabilidad de contagiarse
gamma = 1/7 # probabilidad de recuperarse o morir
poblacion = 1000 # población total
I0 = poblacion * 0.01 # infectados iniciales

y0 = [poblacion - I0, I0, 0.0, I0] # Conjunto de condiciones iniciales y(0)
t = np.linspace(0, 40, 40) # Tiempo de simulación (un paso por día)

sol = odeint(sir, y0, t, args=(beta, gamma)) # Solucionador

plt.plot(t, sol[:, 0], 'b', label='S')
plt.plot(t, sol[:, 1], 'g', label='I')
plt.plot(t, sol[:, 2], 'r', label='R')
plt.plot(t, sol[:, 3], 'o', label='C')
plt.legend(loc='best')
plt.title('Simulación modelo SIR')
plt.xlabel('días')
plt.ylabel('personas')
plt.grid()

C = sol[:, 3]
X = C[2:] - C[1:-1]
plt.bar(range(len(X)), X)
plt.title('Casos diarios')
plt.xlabel('días')
plt.ylabel('personas')
