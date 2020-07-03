# ---------- Utility script for the simulation of 6250 ----------
# Reset the mixer.prm in each mixer file
# ____________________
# Valérie Bibeau, 2020

from jinja2 import Template
import os
import sys
import numpy as np

path = os.getcwd() + "/"

velocity = np.linspace(0.1,500,10)

first = np.arange(1,6250,10)

progress = 1
total = 6250
for i in first:
    group = np.linspace(i,i+9,10)
    j = 0
    for v in velocity:
        # Open the parameter file
        fic_prm = open("mixer.prm","r")
        cte_prm = fic_prm.read()
        # Insert the parameters
        template_prm = Template(cte_prm)
        parameters = template_prm.render(omega = v)
        fic_prm.close()

        mixer = "mixer_" + str(int(group[j]))
        sim_path = path + mixer
        os.chdir(sim_path)
        wr_prm = open("mixer.prm","w")
        wr_prm.write(parameters)
        wr_prm.close()

        os.chdir("../")

        j += 1

        pourcentage = progress/total*100
        sys.stdout.write("\rProgress: " + str(pourcentage) + "%")
        sys.stdout.flush()
        progress += 1
sys.stdout.write("\n")