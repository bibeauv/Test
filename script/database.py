# ------------------------------------------------------------------------
# Script python permettant de générer une base de données :
# La base de données contient les maillages de différentes géométries et les
# paramètres physiques d'un mélangeur muni d'une turbine pitch blade.
# ______________
# Valérie Bibeau, Polytechnique Montréal, 2020

from jinja2 import Template
import os
import numpy as np

# Create arrays for every ratios of the mixer's geometry
array_ratioTD = np.linspace(2,5,2)
array_ratioHT = np.linspace(1,1.5,2)
array_ratioTC = np.linspace(2,5,2)
array_ratioDW = np.linspace(3,6,2)

# Constants
theta = 0.785398163
p_thick = 0.1

first = len(array_ratioTD)                                      # Here!

# Create array for the impeller velocity (omega)
velocity = np.linspace(10,500,2)

path = "/home/bibeauv/soft/lethe/mixer-database/script"

total = (len(array_ratioTD)*
         len(array_ratioHT)*
         len(array_ratioTC)*
         len(array_ratioDW)*
         len(velocity)     * 2)

print ("First adimensional geometry is TD")                     # Here!
print ("Size of the first adimensional geometry =", first)
print ("Total of possible folders =", total)
print ("Set the start segment :")
start = int(input())
print ("Set the stop segment :")
stop = int(input())
print ("Number of folders =", (stop-start+1)*total/first)

number = (start-1)*total/first+1
stop_number = stop*total/first

for rTD in array_ratioTD[start-1:stop]:                         # Here!
    for rTC in array_ratioTC:
        for rDW in array_ratioDW:
            for rHT in array_ratioHT:
                array_ratioDW_Hub = [rTD, rTD-0.4*rTD]
                for rDW_Hub in array_ratioDW_Hub:
                    for v in velocity:
                        # Open the geometry file
                        fic_geo = open("mixer.geo","r")
                        cte_geo = fic_geo.read()
                        # Insert the geometry
                        template = Template(cte_geo)
                        geometries = template.render(ratioTD = rTD,
                                                     ratioHT = rHT,
                                                     ratioTC = rTC,
                                                     ratioDW = rDW,
                                                     ratioDW_Hub = rDW_Hub,
                                                     theta = theta,
                                                     p_thick = p_thick)
                        fic_geo.close()

                        # Open the parameter file
                        fic_prm = open("mixer.prm","r")
                        cte_prm = fic_prm.read()
                        # Insert the parameters
                        template_prm = Template(cte_prm)
                        parameters = template_prm.render(omega = v)
                        fic_prm.close()

                        # Create the folder where the simulation will launch
                        path_number = str(int(number))
                        newPath = path + "/mixer_" + path_number
                        os.mkdir(newPath)
                        os.chdir(newPath)
                        # Write the geometry file and the parameter file
                        wr_geo = open("mixer.geo","w")
                        geo_file = wr_geo.write(geometries)
                        wr_geo.close()

                        wr_prm = open("mixer.prm","w")
                        prm_file = wr_prm.write(parameters)
                        wr_prm.close()

                        # Write the tag file
                        fic_tag = open("mixer.txt","w")
                        fic_tag.write("T/D\t%f\n" % rTD)
                        fic_tag.write("H/T\t%f\n" % rHT)
                        fic_tag.write("T/C\t%f\n" % rTC)
                        fic_tag.write("D/W\t%f\n" % rDW)
                        fic_tag.write("D/W_Hub\t%f\n" % rDW_Hub)
                        fic_tag.write("theta\t%f\n" % theta)
                        fic_tag.write("E\t%f\n" % p_thick)

                        os.chdir("../")

                        if number == stop_number:
                            break
                        else:
                            number = number+1