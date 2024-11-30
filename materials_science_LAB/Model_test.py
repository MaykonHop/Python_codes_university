# -*- coding: utf-8 -*-
"""
Model_test.py
"""

import pandas as pd
import matplotlib.pylab as plt
import numpy as np

df = pd.read_csv(r"G7.csv", sep = ';', encoding='ISO-8859-1', usecols = [2,5]) # Reading csv file with the data, force and deformation
df = df.iloc[1:]

# Data processing
df['Força'] = df['Força'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
df['Deformação à tração (Deformação)'] = df['Deformação à tração (Deformação)'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
df['Força'] = pd.to_numeric(df['Força'], errors='coerce')
df['Deformação à tração (Deformação)'] = pd.to_numeric(df['Deformação à tração (Deformação)'], errors='coerce')

# Unpack
Kforca = np.array(df['Força'])
defor = np.array(df['Deformação à tração (Deformação)'])

# Unit conversion
forca = Kforca * 1000 # leaves the force in N instead of kN
tensao = forca / 0.000032578 # calculates the stress sigma = F/A, A = (2.6 * 12.53 * 10^-6) m

E = (tensao[400] / (defor[400]*1E-2)) # Yield stress in the array

# Maximum point
defor_max = defor[7327]
tensao_max = tensao.max() # Stress maximum

# Stress of rupture point
defor_rup = defor[-1]
tensao_rup = tensao[-1] # Stress of rupture

# Tenacity
area = np.trapz(tensao, defor/100)

# Yield stress point 
defor_escoamento = defor[819]
tensao_escoamento = tensao[819]

# Defines the size of the figure
plt.figure(figsize=(25, 10))

plt.scatter(defor_escoamento, tensao_escoamento, color='red', s=25, label='Ponto de máximo')
# Maximum
plt.scatter(defor_max, tensao_max, color='red', s=25, label='Ponto de máximo')
# Failure
plt.scatter(defor_rup, tensao_rup, color='red', s=25, label='Ponto de falha')

# line
# Define the equation of the line
x = [0.2, defor[np.where(tensao >= tensao_escoamento)][0]]
y = [0, tensao_escoamento]  # Using the yield stress value you calculated previously

# Calculates the area under the line segment
base = x[1]
altura = tensao_escoamento
area_segmento = (base * altura) / 2

print("Área sob o segmento de reta:", area_segmento)


# Plot the line
plt.plot(x, y, "b--", label="Reta")

# Graphic
plt.plot(defor, tensao, "r",label = "Gráfico")

# Graphic
plt.xticks(np.arange(0, defor.max() + 5, 1))
plt.xlabel("Deformação (%)", fontsize = 14)
plt.ylabel("Tensão(N/m^2)", fontsize = 14)
plt.grid(True, linestyle='--', linewidth=1.25, alpha=1)
plt.title("Gráfico Tensão x Deformação", fontsize = 20)
plt.legend()
plt.show()

# Print of the main values with your units
print("Rigidez: ",E*1E-9, "GPa")
print("Tensão máxima: ",tensao_max*1E-6, "MPa")
print("Tenacidade: ",area*1E-6, "MJ/m^3 ou MPa")
print("Resiliência: ",area_segmento*1E-6, "MJ/m^3 ou MPa")
print("Tensão de escoamento: ",tensao_escoamento*1E-6, "MPa")
print("Tensão de ruptura: ",tensao_rup*1E-6, "MPa")
