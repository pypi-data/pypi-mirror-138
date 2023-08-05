"""
This module is using to make atom transfromations
i used both codes orthorhombic_transform and inverse_transform to make a great atomic transformations

Firstly i started with orthorombic_transform where the atoms were i am going to put in the orthorhombic box 
where the size is computed by using the previous size box associated to the system you are studied.

this transformation is really important when you want to compute the center of masses for each molecules 
does you system has, due to the periodic boundaries conditions it's really complicated to compute the reals 
centers of mass when the box is not orthorhombic.

then after this transformation i used the inverse_transform program to rebuild the real system    


So, The strategy is as follow i use the intial coordinates into the hexahonal box 


                                          orthorhombic_tranform ()
                                                    |
----> first transfromation :   hexagonal   --------------------> orthorhombic
                                                                     |
                                                                     | <-----> inverse_transform ()
                                                                     |
                                            hexagonal  <--------------                
"""


import numpy as np
from math import pi 

def orthorhombic_transform(x, y, z,  a, b, c, imcon, angle):
    def decor(func):
        def wrap():
            print("==================================")
            func()
            print("==================================")
        return wrap()

    if imcon in [1, 2, 4]: # cubic , quadratic, orthorhombic
        matrix_tranform = np.array([[a, 0.,  0.],
	    [ 0., b, 0.],
	    [0., 0., c]])

    elif imcon == 3: # hexagonal
        matrix_tranform = np.array([[a, -0.5 * a, 0.],
	    [ 0., a * np.cos(pi / 6.0), 0],
	    [0., 0., c]])

    elif imcon == 5: # rhomboedric
        gama = (angle[2] / 180.) * pi
        w2 = np.sin(gama - (pi / 2.))
        w1 = np.cos(gama - (pi / 2.))

        matrix_tranform = np.array([[a, -  w2 * b, 0.],
        [0.,  w1* b, 0.],
        [0., 0., c]])
        
    elif imcon == 6: # monoclinic
        beta = (angle[1] / 180.) * pi
        w3 = np.sin(beta - (pi / 2.))
        w2 = np.cos(beta - (pi / 2.)) 
        matrix_tranform = np.array([[a, 0., -  w3 * c],
        [0., b, 0.],
        [0., 0., w2 * c]])
    
    else:
        @decor
        def print_error():
            print("error")
            print("imcon not in [1, 2, 3, 4, 5, 6]")
        exit()

    matrix_inverse = np.linalg.inv(matrix_tranform)
    x_vector, y_vector, z_vector, new_vector= [],[],[],[]

    for i in range(0, x.shape[0]):
        old_vector = np.array([x[i], y[i], z[i]])
        x_transform, y_transform, z_transform = np.dot(matrix_inverse , old_vector)
        x_transform, y_transform, z_transform = x_transform * a, y_transform * b, z_transform * c
        x_vector.append(x_transform),y_vector.append(y_transform), z_vector.append(z_transform)
        new_vector.append([x_transform, y_transform, z_transform])

    x_vector, y_vector, z_vector = np.array(x_vector), np.array(y_vector), np.array(z_vector)

    return [x_vector, y_vector, z_vector]

def inverse_transform(x, y, z, imcon, angle):

    def decor(func):
        def wrap():
            print("==================================")
            func()
            print("==================================")
        return wrap()

    if imcon in [1, 2, 4]: # cubic , quadratic, orthorhombic
        matrix_tranform = np.array([[1., 0., 0.],
	    [ 0., 1., 0.],
	    [0., 0., 1.]])
   
    elif imcon == 3: #hexagonal

        matrix_tranform = np.array([[1., -0.5 * 1., 0.],
	    [ 0., np.cos(pi / 6.) * 1., 0.],
	    [0., 0., 1.]])
    
    elif imcon == 5: #trigonal
        gama = ( angle[2] / 180.) * pi
        matrix_tranform = np.array([[1., - np.sin(gama - (pi / 2.) ) * 1., 0.],
	    [ 0., np.cos(gama - (pi / 2.) ) * 1., 0.],
	    [0., 0., 1.]])
    
    elif imcon == 6: #monoclinic
        beta = ( angle[1] / 180.) * pi
        matrix_tranform = np.array([[1., 0., -np.sin(beta - (pi / 2.) ) * 1.],
	    [ 0., 1., 0.],
	    [0., 0., np.cos( beta - (pi / 2.) ) * 1.]])
   
    else:
        @decor
        def print_error():
            print("error")
            print("imcon not in [1, 2, 3, 4, 5, 6]")
        exit()

    old_vector = np.array([x, y, z])
    x_transform, y_transform, z_transform = np.dot(matrix_tranform , old_vector)    
    
    return [x_transform, y_transform, z_transform]

def inverse_(x, y, z, imcon, angle, old, new):

    def decor(func):
        def wrap():
            print("==================================")
            func()
            print("==================================")
        return wrap()

    if imcon in [1, 2, 4]: # cubic , quadratic, orthorhombic
        matrix_tranform = np.array([[1., 0., 0.],
	    [ 0., 1., 0.],
	    [0., 0., 1.]])
   
    elif imcon == 3: #hexagonal

        matrix_tranform = np.array([[1., -0.5 * 1., 0.],
	    [ 0., np.cos(pi / 6.) * 1., 0.],
	    [0., 0., 1.]])
    
    elif imcon == 5: #trigonal
        gama = ( angle[2] / 180.) * pi
        matrix_tranform = np.array([[1., - np.sin(gama - (pi / 2.) ) * 1., 0.],
	    [ 0., np.cos(gama - (pi / 2.) ) * 1., 0.],
	    [0., 0., 1.]])
    
    elif imcon == 6: #monoclinic
        beta = ( angle[1] / 180.) * pi
        matrix_tranform = np.array([[1., 0., -np.sin(beta - (pi / 2.) ) * 1.],
	    [ 0., 1., 0.],
	    [0., 0., np.cos( beta - (pi / 2.) ) * 1.]])
   
    else:
        @decor
        def print_error():
            print("error")
            print("imcon not in [1, 2, 3, 4, 5, 6]")
        exit()

    old_vector = np.array([x, y, z])
    x_transform, y_transform, z_transform = np.dot(matrix_tranform , old_vector)    
    x_transform, y_transform, z_transform = x_transform * (new[0][0] / old[0][0]), y_transform * (new[0][0] / old[0][0]), z_transform * (new[2][2] / old[2][2])
    
    return [x_transform, y_transform, z_transform]
