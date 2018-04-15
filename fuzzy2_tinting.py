import numpy as np
import matplotlib.pyplot as plt

from fuzzython.fsets.triangular import Triangular
from fuzzython.adjective import Adjective
from fuzzython.variable import Variable


# =========================================================================
# =========================================================================
# =========================================================================


#Definicja zmiennych lingwistycznych
#Dla każdej ze zmiennych definiujemy wartości lingwistyczne, trójkątne zbiory rozmyte


# wartosci dla natężenia światła
l_low = Triangular((19.9,0), (20,1), (60,0))
l_medium = Triangular((20,0), (60,1), (100,0))
l_high = Triangular((60,0), (100,1), (100.1,0))
l_low = Adjective('l_low', l_low)
l_medium = Adjective('l_medium', l_medium)
l_high = Adjective('l_high', l_high)
LightIntensity = Variable('LightIntensity', 'klx', l_low, l_medium, l_high) #natężenie światła w kilo luxach (20[klx] - 60[klx]- 100[klx])


#wartości dla pory dnia
t_dawn = Triangular((5.9,0), (6,1), (6.5,0))
t_morning = Triangular((6.0,0), (6.5,1), (11.1,0))
t_afternoon = Triangular((6.5,0), (11,1), (17,0))
t_evening = Triangular((11,0), (17,1), (21,0))
t_dawn = Adjective('t_dawn', t_dawn)
t_morning = Adjective('t_morning', t_morning)
t_afternoon = Adjective('t_afternoon', t_afternoon)
t_evening = Adjective('t_evening', t_evening)
TimeOfDay = Variable('TimeOfDay', 'h', t_dawn, t_morning, t_afternoon, t_evening) #pory dnia (godz. 6:00 - godz. 21:00)


#Przyciemnianie okien
d_low = Triangular((-0.1,0), (0,1), (33.3,0))
d_lower_medium = Triangular((0,0), (33.3,1), (66.6,0))
d_higher_medium = Triangular((33.3,0), (66.6,1), (100,0))
d_high = Triangular((66.6,0), (100,1), (100.1,0))
d_low = Adjective('d_low', d_low)
d_lower_medium = Adjective('d_lower_medium', d_lower_medium)
d_higher_medium = Adjective('d_higher_medium', d_higher_medium)
d_high = Adjective('d_high', d_high)
WindowsDimming = Variable('WindowsDimming', '%', d_low, d_lower_medium, d_higher_medium, d_high, defuzzification='COG', default=0) # przyciemnienie okna -  od 0% do 100%


# Definicja reguł
scope = locals()

rule1 = 'if LightIntensity is l_low or TimeOfDay is t_dawn or TimeOfDay is t_evening then WindowsDimming is d_low'
rule2 = 'if LightIntensity is l_medium and TimeOfDay is t_morning or TimeOfDay is t_dawn then WindowsDimming is d_lower_medium'
rule3 = 'if LightIntensity is l_medium and TimeOfDay is t_afternoon or TimeOfDay is t_morning then WindowsDimming is d_higher_medium'
rule4 = 'if LightIntensity is l_high or TimeOfDay is t_afternoon then WindowsDimming is d_high'
rule5 = 'if LightIntensity is l_medium or LightIntensity is l_low or TimeOfDay is t_evening then WindowsDimming is d_lower_medium'

from fuzzython.ruleblock import RuleBlock
block = RuleBlock('first', operators=('MIN','MAX','ZADEH'), activation='MIN', accumulation='MAX')
block.add_rules(rule1, rule2, rule3, rule4, rule5, scope=scope)

# Stworzenie sterownika rozmytego typu Mamdani
from fuzzython.systems.mamdani import MamdaniSystem
mamdani = MamdaniSystem('ms1', block)


sampled = np.linspace(19.9, 100.1, 25)
sampled2 = np.linspace(5.9, 21, 25)
x, y = np.meshgrid(sampled, sampled2)
z = np.zeros((len(sampled),len(sampled2)))

for i in range(len(sampled)):
    for j in range(len(sampled2)):
        inputs = {'LightIntensity': x[i, j], 'TimeOfDay': y[i, j]}
        res = mamdani.compute(inputs)
        z[i, j] = res['first']['WindowsDimming']

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