import numpy as np
from math import pi, cos
from matrix_package.coordinates_transform import inverse_transform

def Periodic_BC(dx = float, dy = float, dz = float, CELL = None, imcon = int):
    def decor(func):
            def wrap():
                print("===================================================================")
                func()
                print("===================================================================")
            return wrap()
    boxx, boxy, boxz = CELL

    if imcon in [1, 2, 4]:

        if (np.abs(dx) > boxx[0] / 2.):
            dx = dx - np.sign(dx) * boxx[0]
        else:
            dx = dx

        if (np.abs(dy) > boxy[1] / 2.):
            dy = dy - np.sign(dy) * boxy[1]
        else:
            dy = dy

        if (np.abs(dz) > boxz[2] / 2.):
            dz = dz - np.sign(dz) * boxz[2]
        else:
            dz = dz

    elif imcon == 3:

        if (np.abs(dz) > boxz[2] / 2.):
            dz = dz - np.sign(dz) * boxz[2]
        else:
            dx = dx

        if (np.abs(dy) > boxy[1] / 2.):
            if (np.abs(2. * dx * np.cos(pi / 6.) + dy) > (boxx[0] * np.cos(pi / 6.))):
                dx = dx - np.sign(dx) * boxx[0]
            else:
                dx = dx
            dy = dy - np.sign(dy) * boxy[1]
        else:
        	if (np.abs(2. * dx * np.cos(pi / 6.) + dy) > (boxx[0] * np.cos(pi / 6.))):
        		dx = dx - np.sign(dx) * boxx[0]
        	else:
        		dx = dx   
        	dy = dy   	
            
    else:
        @decor
        def print_error():
            print('bad imcon value for PBC'.upper())
            print('imcon = [1, 2, 3, 4]')
            print('1 = cubic| 2 = orthorhombic , | 3 = hexagonal, | 4 = quadratic')
        exit()

    return [dx, dy, dz]

def Volume(CELL = None, imcon = int, angle = None):

    boxx, boxy, boxz = CELL
    if imcon in [1, 2, 4]:
        alpha, beta, gama = pi / 2., pi / 2., pi / 2.
    elif imcon == 3:
        alpha, beta, gama = pi / 2., pi / 2., (2. * pi) / 3.
    else:
        alpha, beta, gama = (angle[0] / 180.) * pi, (angle[1] / 180.) * pi, (angle[2] / 180.) * pi
    
    diff = np.square(cos(alpha)) + np.square(cos(beta)) + np.square(cos(gama)) 
    prod = 2. * cos(alpha) * cos(alpha) * cos(alpha)
    volume = boxx[0] * boxy[1] * boxz[2] * np.sqrt(1. - diff + prod)

    return volume

def PBC_Bulk_System(dx = float, dy = float, dz = float, x = float, y = float, z = float, CELL = None, imcon = int):
    def decor(func):
            def wrap():
                print("===================================================================")
                func()
                print("===================================================================")
            return wrap()
    boxx, boxy, boxz = CELL
 
    if imcon in [1, 2, 4]:

        if (np.abs(dx) > boxx[0] / 2.):
            x1 = x + np.sign(dx) * boxx[0]
        else:
            x1 = x

        if (np.abs(dy) > boxy[1] / 2.):
            y1 = y + np.sign(dy) * boxy[1]
        else:
            y1 = y

        if (np.abs(dz) > boxz[2] / 2.):
            z1 = z + np.sign(dz) * boxz[2]
        else:
            z1 = z

    elif imcon == 3:

        if (np.abs(dz) > boxz[2] / 2.):
            z1 = z + np.sign(dz) * boxz[2]
        else:
            z1 = z

        if (np.abs(dy) > boxy[1] / 2.):
            if (np.abs(2. * dx * np.cos(pi / 6.) + dy) > (boxx[0] * np.cos(pi / 6.))):
                x1 = x + np.sign(dx) * boxx[0]
            else:
                x1 = x
            y1 = y + np.sign(dy) * boxy[1]
        else:
            y1 = y

    else:
        @decor
        def print_error():
            print('bad imcon value for PBC')
            print('imcon = [1, 2, 3, 4]')
            print('1 = cubic| 2 = orthorhombic , | 3 = hexagonal, | 4 = quadratic')
        exit()

    return [x1, y1, z1]

def Atoms_In_BOX(x = None, y = None, z = None, imcon = int, CELL = list):
    def decor(funct):
        def wrap():
            print("===================================================")
            funct()
            print("===================================================")
        return wrap()
	

    boxx, boxy, boxz = CELL
    if imcon in [1, 2, 4]:
        bx, by, bz =  boxx[0], boxy[1], boxz[2]
    elif imcon in [3, 5]:
        bx, by, bz =  boxx[0], boxx[0], boxz[2]
    elif imcon == 6:
        bx, by, bz =  boxx[0], boxx[0], np.sqrt( np.square(boxx[2]) + np.square(boxz[2]) )
	
    new_xyz_val = []
    for p in range(0, x.shape[0]):
        if imcon in [1, 2, 3, 4, 5, 6]:
            if x[p] < 0.0:
                x[p] = x[p] + bx
            elif x[p] > bx:
                x[p] = x[p] - bx
            else:
                x[p] = x[p]

            if y[p] < 0.0:
                y[p] = y[p] + by
            elif y[p] > by:
                y[p] = y[p] - by
            else:
                y[p] = y[p]

            if z[p] < 0.0:
                z[p] = z[p] + bz
            elif z[p] > bz:
                z[p] = z[p] - bz
            else:
                z[p] = z[p]

        new_xyz_val.append([x[p], y[p], z[p]]) 
    return [x, y, z]
    		
def Redim_Atoms_In_BOX(x = None, y = None, z = None, dx = None, dy = None, dz = None, 
imcon = int, CELL = list, angle = list):

    boxx, boxy, boxz = CELL
    if imcon in [1, 2, 4]:
        bx, by, bz =  boxx[0], boxy[1], boxz[2]
    elif imcon in [3, 5]:
        bx, by, bz =  boxx[0], boxx[0], boxz[2]
    elif imcon == 6:
        bx, by, bz =  boxx[0], boxx[0], np.sqrt( np.square(boxx[2]) + np.square(boxz[2]) )  

    new_xyz_val = []
    for i in range(0, x.shape[0]):
        if imcon in [1, 2, 3, 4, 5, 6]:
            if (np.abs(dx[i]) >= bx / 2.0):
                x[i] = x[i] + np.sign(dx[i]) * bx
            else:
                x[i] = x[i]
            if (np.abs(dy[i]) >= by / 2.0):
                y[i] = y[i] + np.sign(dy[i]) * by
            else:
                y[i] = y[i]
            if (np.abs(dz[i]) >= bz / 2.0):
                z[i] = z[i] + np.sign(dz[i]) * bz 
            else:
                z[i] = z[i]

            x[i], y[i], z[i] = inverse_transform(x[i], y[i], z[i],imcon, angle) 
 
        new_xyz_val.append([x[i], y[i], z[i]])
    return new_xyz_val

	

		 
		
	


			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
		
	
