import numpy as np
from math import pi
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
    	bx, by, bz =  boxx[0], boxy[1], boxz[2]
    elif imcon ==3:
        bx, by, bz =  boxx[0], boxx[0], boxz[2]
	
    if imcon in [1, 2, 3, 4]:

        if (np.abs(dx) > boxx[0] / 2.):
            dx = dx - np.sign(dx) * bx
        else:
            dx = dx

        if (np.abs(dy) > boxy[1] / 2.):
            dy = dy - np.sign(dy) * by
        else:
            dy = dy

        if (np.abs(dz) > boxz[2] / 2.):
            dz = dz - np.sign(dz) * bz
        else:
            dz = dz

    elif imcon == 5:

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
