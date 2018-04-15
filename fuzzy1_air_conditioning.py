# =========================================================================
#					MAMDANI

# import modułów
import numpy as np
import matplotlib.pyplot as plt

from fuzzython.fsets.triangular import Triangular
from fuzzython.adjective import Adjective
from fuzzython.variable import Variable


#Definicja zmiennych lingwistycznych
#Dla każdej ze zmiennych definiujemy wartości lingwistyczne, trójkątne zbiory rozmyte


# wartosci dla temperatury
t_low = Triangular((19.9,0), (20,1), (30,0))
t_medium = Triangular((20,0), (30,1), (40,0))
t_high = Triangular((30,0), (40,1), (40.1,0))
t_low = Adjective('t_low', t_low)
t_medium = Adjective('t_medium', t_medium)
t_high = Adjective('t_high', t_high)
Temperature = Variable('Temperature', 'degree', t_low, t_medium, t_high) # Temperatura powietrza (20 stopni do 40 stopni)


#wartosci dla wilgotnosci
h_low = Triangular((-0.1,0), (0,1), (40,0))
h_lower_medium = Triangular((0,0), (40,1), (60,0))
h_higher_medium = Triangular((40,0), (60,1), (100,0))
h_high = Triangular((60,0), (100,1), (100.1,0))


h_low = Adjective('h_low', h_low)
h_lower_medium = Adjective('h_lower_medium', h_lower_medium)
h_higher_medium = Adjective('h_higher_medium', h_higher_medium)
h_high = Adjective('h_high', h_high)
Humidity = Variable('Humidity', '%', h_low, h_lower_medium, h_higher_medium, h_high) # Wilgotnosc w skali od 0 do 100 %


#wartosci dla dzialania klimatyzacji
k_low = Triangular((-0.1,0), (0,1), (50,0))
k_medium = Triangular((0,0), (50,1), (100,0))
k_high = Triangular((50,0), (100,1), (100.1,0))
k_low = Adjective('k_low', k_low)
k_medium = Adjective('k_medium', k_medium)
k_high = Adjective('k_high', k_high)
Klimatyzacja = Variable('Klimatyzacja', '%', k_low, k_medium, k_high, defuzzification='COG', default=0) # Moc klimatyzatora od 0 do 100%


# Definicja reguł
from fuzzython.ruleblock import RuleBlock

scope = locals()

rule1 = 'if Temperature is t_low or Humidity is h_low then Klimatyzacja is k_low'
rule2 = 'if Temperature is t_medium or Humidity is h_lower_medium or Humidity is h_higher_medium then Klimatyzacja is k_medium'
rule3 = 'if Temperature is t_medium and Humidity is h_high then Klimatyzacja is k_medium'
rule4 = 'if Temperature is t_high or Humidity is h_high then Klimatyzacja is k_high'


block = RuleBlock('first', operators=('MIN','MAX','ZADEH'), activation='MIN', accumulation='MAX')
block.add_rules(rule1, rule2, rule3, rule4, scope=scope)

# Stworzenie sterownika rozmytego typu Mamdani
from fuzzython.systems.mamdani import MamdaniSystem
mamdani = MamdaniSystem('ms1', block)


sampled = np.linspace(20, 40, 25)
sampled2 = np.linspace(0, 100, 25)
x, y = np.meshgrid(sampled, sampled2)
z = np.zeros((len(sampled),len(sampled2)))

for i in range(len(sampled)):
    for j in range(len(sampled2)):
        inputs = {'Temperature': x[i, j], 'Humidity': y[i, j]}
        res = mamdani.compute(inputs)
        z[i, j] = res['first']['Klimatyzacja']

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                       linewidth=0.4, antialiased=True)

cset = ax.contourf(x, y, z, zdir='z', offset= -1, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='x', offset= 11, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='y', offset= 11, cmap='viridis', alpha=0.5)

ax.view_init(30, 200)

# =========================================================================
# =========================================================================
# =========================================================================
#					TAKAGI-SUGENO

#Definicja zmiennych lingwistycznych
#Dla każdej ze zmiennych definiujemy wartości lingwistyczne, trójkątne zbiory rozmyte

t_low = Triangular((19.9,0), (20,1), (30,0))
t_medium = Triangular((20,0), (30,1), (40,0))
t_high = Triangular((30,0), (40,1), (40.1,0))
t_low = Adjective('t_low', t_low)
t_medium = Adjective('t_medium', t_medium)
t_high = Adjective('t_high', t_high)
temperature = Variable('temperature', 'deg', t_low, t_medium, t_high) # Skala temperatury, w stopniach od 20 do 40.

h_low = Triangular((-0.1,0), (0,1), (40,0))
h_medium1 = Triangular((0,0), (40,1), (60,0))
h_medium2 = Triangular((40,0), (60,1), (100,0))
h_high = Triangular((60,0), (100,1), (100.1,0))
h_low = Adjective('h_low', h_low)
h_medium1 = Adjective('h_medium1', h_medium1)
h_medium2 = Adjective('h_medium2', h_medium2)
h_high = Adjective('h_high', h_high)
humidity = Variable('humidity', '%', h_low, h_medium1, h_medium2, h_high) #wilgotnosc (0-100)%

k_low = Triangular((-0.1,0), (0,1), (50,0))
k_medium = Triangular((0,0), (50,1), (100,0))
k_high = Triangular((50,0), (100,1), (100.1,0))
k_low = Adjective('k_low', k_low)
k_medium = Adjective('k_medium', k_medium)
k_high = Adjective('k_high', k_high)
klim = Variable('klim', '%', k_low, k_medium, k_high, defuzzification='COG', default=0) # Klimatyzacja (0-100)%

# Definicja reguł
from fuzzython.ruleblock import RuleBlock

scope = locals()

# Zmienne zdefiniowane jak poprzednio

# Definiujemy reguły
rule4 = 'if temperature is t_high or humidity is h_low then z=temperature*0.5 + humidity*0.5'
rule5 = 'if temperature is t_medium or humidity is h_medium1 then z=temperature*0.7+5'
rule6 = 'if temperature is t_low or humidity is h_high then z=temperature*0.4+humidity*0.6+15'

block = RuleBlock('second', operators=('MIN', 'MAX', 'ZADEH'), activation='MIN')
block.add_rules(rule4, rule5, rule6, scope=scope)

# Stworzenie sterownika rozmytego typu Takagi-Sugeno
from fuzzython.systems.sugeno import SugenoSystem

sugeno = SugenoSystem('ss1', block)

# wnioskowanie
inputs = {'temperature': 6.5, 'humidity': 9.8}
res = sugeno.compute(inputs)
print(res)

sampled = np.linspace(0, 10, 20)
x, y = np.meshgrid(sampled, sampled)
z = np.zeros((len(sampled),len(sampled)))

for i in range(len(sampled)):
    for j in range(len(sampled)):
        inputs = {'temperature': x[i, j], 'humidity': y[i, j]}
        res = sugeno.compute(inputs)
        z[i, j] = res['second']

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                       linewidth=0.4, antialiased=True)

cset = ax.contourf(x, y, z, zdir='z', offset= -1, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='x', offset= 11, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='y', offset= 11, cmap='viridis', alpha=0.5)

ax.view_init(30, 200)
plt.show()