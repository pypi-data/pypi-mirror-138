import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from math import cos, pi
from matrix_package.params import * 
from matrix_package.pbc import Redim_Atoms_In_BOX, Atoms_In_BOX
from matrix_package.coordinates_transform import inverse_transform, orthorhombic_transform, inverse_
from time import sleep
from alive_progress import alive_bar 


class COM:
    
    def Center_Of_Mass(self,mol_type : int = None, nmol : list = None,
        trajec_key : int = None, atoms_select = None, index_select : int = None,
        atoms_key : list= None, nsit : list = None, max_float = 5, key_num = int, dtype : float = np.float32,
        trajec_num : int = None, XYZ : list = None, Mass : list = None, CELL : list = None, imcon : int = None, angle : list = None,
        return_XYZ_CENTER : any = False, index_DF : int = None, return_XYZ_CENTER_AS : str = 'DataFrame'):

        """
        Center_Of_Mass is a module used to compute the center of masses. You need to compute the center of masses of the molecules of 
        your system, you have here the best module to do that. 

        Before using this module firstly you need to extract your data by using Lammps(), Classical_MD(), Ab_Initio_MD() modules.
        It depends witch configuration your system has.
        
        Center_Of_Mass computes the center of masses for all Bravais systems:
        >>> [cubic, quadratic, trigonal, orthorhombic, hexagonal, monoclinic, triclinic]
        
        It has several compulsory inputs:

        * mol_type: used for defining the number of molecules does your integral system has 
        * nmol: used to specify how many molecules does your system has. 
        * trajec_key : used to select the trajectory for the data.frame output
        * atoms_select : used to select atoms from your system
        * index_select : used to specify how many molecules do you use to compute the center of masses
        * atoms_key: used to select witch molecules would you like to computes the center of masses
        * nsit: used to specify how many atoms does your system has per molecules .
        * key_num : select a center of mass to follow its displacement during the simulation
        * max_float : it's same with dtype
        * dtype: used to specify the max float
        * trajec_num: is defining how many trajectrories does your input file has.
        * XYZ : contains the values of the positions 
        * Mass : contains the values of the masses
        * CELL : the values for the box
        * imcon: used for the periodic boundaries conditions 
        * angle : used when the angles of your box are different of 90. and 120.
        * return_XYZ_CENTER : takes two values [True or False] to return the values of the center of masses
        * index_DF : select a molecule for data.frame output
        * return_XYZ_CENTER_AS : witch output do you want, [data.frame or XYZ, or None]
       

        >>>>>>>>>>>>>> INPUTS EXAMPLES  AND DETAILS >>>>>>>>>>>>>>
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        >>> mol_type = 2 
        >>> nmol = [20 , 20] because mol_type = 2 if mol_type = 1 so nmol = [20] etc ....
        >>> nsit = [16, 1]
        >>> trajec_num = 1000 
        
        """
        #new_m, new_xyz, tab_trajec = params_tab()
        
        global xb, idd, XYZ_scale, ind

        idd = key_num
        def decor(func):
            def wrap():
                print("=======================================================")
                func()
                print("=======================================================")
            return wrap() 
        bravais = ['Cubic', 'Quadratic','Hexagonal', 'Orthorhombic', 'Rhomboedric', 'Monoclinic', 'Triclinic']

        t1 = list([])
        t2 = float()
        t3 = int()
        t4 = bool()
        t5 = str()
        t6 = dict()
        t7 = np.ndarray([])

        if XYZ:
            if type(XYZ) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print('XYZ is a list not any other type')
                    print('XYZ, ', type(t1))
                    print('Put a list as an input and run again')
                exit()
            else:
                for i, val in enumerate(XYZ):
                    if type(XYZ[i]) != type(t7):
                        @decor
                        def print_error():
                            print('TypeError 😊')
                            print('The type of XYZ elments are ', type(t7), 'instead ', type(XYZ[i]))
                            print('problem with this list ', 'index = ', i , 'from XYZ')
                            print('Change of the type input and run again')
                        exit()
        else:
            @decor 
            def print_error():
                print('InputError 😊')
                print('XYZ cannot be Empty')
            exit()

        if CELL:
            if type(CELL) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print('CELL is a list not any other type')
                    print('CELL, ', type(t7))
                    print('Put a list as an input and run again')
                exit()
        else:
            @decor 
            def print_error():
                print('InputError 😊')
                print('CELL cannot be Empty')
            exit()

        if Mass:
            if type(Mass) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print('Mass is a list not any other type')
                    print('Mass, ', type(t1))
                    print('Put a list as an input and run again')
                exit()
            else:
                for i, val in enumerate(Mass):
                    if type(Mass[i]) != type(t7):
                        @decor
                        def print_error():
                            print('TypeError 😊')
                            print('The type of Mass elments are ', type(t7), 'instead ', type(Mass[i]))
                            print('problem with this list ', 'index = ', i , 'from Mass')
                            print('Change of the type input and run again')
                        exit()
        else:
            @decor 
            def print_error():
                print('InputError 😊')
                print('Mass cannot be Empty')
            exit()
        
        if not nsit:
            @decor 
            def print_error():
                print('InputError 😊')
                print('nsit cannot be Empty')
            exit()
        else:
            if type(nsit) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("nsit is a list not any other type")
                    print('nsit, ', type(t1))
                    print("Put nmol as list and try again")
                exit()   
            else:
                for i, val in enumerate(nsit):
                    if type(val) != type(t3):
                        @decor 
                        def print_error():
                            print('TypeError 😊')
                            print("The values in nsit should be integers")
                            print(type(t3))
                            print("Check your values and correct the bad values")
                            print('The bad found is :', val, 'index = ', i, 'from', nsit)
                        exit()
                    else:
                        if val <= 0:
                            @decor 
                            def print_error():
                                print('ValueError 😊')
                                print("The values in nsit should be bigger than 0")
                                print("Check your values and correct the bad values")
                                print('The bad found is :', val, 'index = ', i, 'from', nsit)
                            exit()

        if not mol_type:
            @decor 
            def print_error():
                print('InputError 😊')
                print("mol_type is Empty")
            exit() 
        else:
            if type(mol_type) != type(t3):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("mol_type is an integer not any other type")
                    print('mol_type, ', type(t3))
                    print("Put mol_type as an integer and try again")
                exit()
            else:
                if mol_type < 0:
                    @decor 
                    def print_error():
                        print('ValueError 😊')
                        print('mol_type cannot be negative')
                    exit()

        if not index_select:
            @decor 
            def print_error():
                print('InputError 😊')
                print("index_select is Empty")
            exit() 
        else:
            if type(index_select) != type(t3):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("index_selectis an integer not any other type")
                    print('index_select, ', type(t3))
                    print("Put index_select as an integer and try again")
                exit()
            else:
                if index_select < 0:
                    @decor 
                    def print_error():
                        print('ValueError 😊')
                        print('index_select cannot be negative')
                    exit()

        if not trajec_num:
            @decor 
            def print_error():
                print('InputError 😊')
                print('trajec_num connot be Empty')
            exit()
        else:
            if type(trajec_num) != type(t3):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print('trajec_num is an integer not any other type')
                    print('trajec_num, ', type(t3))
                    print('Put an integer as an input and run again')
                exit()
            else:
                if trajec_num < 0:
                    @decor 
                    def print_error():
                        print('ValueError 😊')
                        print('trajec_num cannot be negative')
                    exit() 

        if len(nsit) != mol_type :
            @decor
            def print_error():
                print("ValueError 😊")
                print("lenght nsit  is not the same with mol_type")
                print('Check your value and try again')
            exit() 
        if len(nmol) != mol_type:
            @decor
            def print_error():
                print("ValueError 😊")
                print("lenght nmol is not the same with mol_type")
                print('Check your value and try again')
            exit()
  
        if index_DF > mol_type:
            @decor
            def print_error():
                print("ValueError 😊")
                print("bad index_DF value, index_DF should be lower than mol_type ")
                print('Check your value and try again')
            exit()        
        if key_num > nmol[index_DF] :
            @decor
            def print_error():
                print("ValueError 😊")
                print("bad key_num value, key_num should be lower")
                print("than the values in the list below  ")
                print(nmol)
            exit()

        if atoms_select:
            if type(atoms_select) == type(t5):
                if atoms_select != 'ALL':
                    @decor
                    def print_error():
                        print("InputError 😊")
                        print("atoms_select is different of 'ALL'")
                        print("Check your value and try again")
                    exit()
                else:
                    if (atoms_select == 'ALL' and index_select != mol_type):
                        @decor
                        def print_error():
                            print("InputError 😊")
                            print("index_select is lower or bigger than mol_type ")
                            print("If atoms_select is defined on 'ALL' , index_select sould be identical to mol_type")
                        exit()
            else:        
                if type(atoms_select) == type(t1):
                    if len(atoms_select) != index_select:
                        @decor
                        def print_error():
                            print("InputError 😊")
                            print("lenght atom_select is diffrent of index_select value")
                            print('Check your values and correct them')
                        exit()
                    else:
                        if not atoms_key:
                            @decor
                            def print_error():
                                print('InputError 😊')
                                print("If atoms_select != 'ALL', atoms_key cannot be Empty")
                                print("Check your value and run again")
                            exit()
                        else:
                            if len(atoms_key) != index_select:
                                @decor
                                def print_error():
                                    print('InputError 😊')
                                    print("lenght atom_key is diffrent from index_select value")
                                    print("Check your value and run again")
                                exit()
                else:
                    @decor
                    def print_error():
                        print('TypeError 😊')
                        print('atoms_select type not in ', [type(t1), type(t5)])
                        print('Put the correct value and try again')
                    exit()
        else:
            @decor
            def print_error():
                print('TypeError 😊')
                print('atoms_select cannot be Empty')
                print('Check your value and try again')
            exit()

        params_(nmol = index_select)

        c, tab_storage, new_tabx, new_taby, new_tabz = params_gdr1()[0:5]
        XYZ_scale, Y1, Z1 = new_array1()
        center_of_mass, gam2, gam3 = new_array2()
	
        Data, DataFrame = params_data(), params_DF()
        ind = atoms_select
	
        if  atoms_select != 'ALL' and len(atoms_select) == index_select: 
            for i in range(0,index_select):
                for k in atoms_select[i]:
                    if k > nsit[atoms_key[i]]:
                        @decor
                        def print_error():
                            print("ValueError 😊")
                            print(k ,'is bigger than', nsit[atoms_key[i]], ' in mol = ', atoms_key[i])
                        exit()
                    else:
                        c[i].append(k)
            c[i] = np.array(c[i])  
        elif atoms_select == 'ALL' :
            for i in range(0,len(nmol)):
                for k in range(0,nsit[i]):
                    c[i].append(k)
                c[i] = np.array(c[i])
 
        boxx, boxy, boxz = CELL
        
        if imcon > 4 :
            if not angle:
                @decor
                def print_error():
                    print('InputError 😊')
                    print('When imcon is bigger 4, the keyword angle cannot be empty')
                    print('your system is ', bravais[imcon-1])
                    print("Put the angle values, [alpha, beta, gamma] and try again")
                exit()
            else:
                if type(angle) != type(t1):
                    @decor
                    def print_error():
                        print('TypeError 😊')
                        print('angle is a list not any other type')
                        print('Put the value as a list and try again')
                        print("angle = [alpha, beta, gamma]")
                    exit()
                else:
                    if len(angle) != 3:
                        @decor
                        def print_error():
                            print('InputError 😊')
                            print('angle length is egal to 3')
                            print('Check your values and try again')
                            print("angle = [alpha, beta, gamma]")
                        exit()
                    else:
                        for ang in angle:
                            if type(ang) not in [type(t2), type(t3)]:
                                @decor
                                def print_error():
                                    print('TypeError 😊')
                                    print('problem with angle list')
                                    print('Bad value : ', ang, 'from the list ', angle)
                                    print('this bad value should be a float or integer type not any other type')
                                exit()
        
        if imcon in [1, 2, 4]:
            bx, by, bz =  boxx[0], boxy[1], boxz[2] 
        elif imcon in [3, 5]:
            bx, by, bz =  boxx[0], boxx[0], boxz[2] 
        elif imcon == 6:
            bx, by =  boxx[0], boxx[0]
            bz = np.sqrt( np.square(boxx[2]) + np.square(boxz[2]) )
        else:
            @decor
            def print_error():
                print('InputError ')
                print('Bad value of keyword imcon')
                print('imcon not in the list ', [1,2,3,4,5,6], 'corresponding to the list below')
                print(bravais)
                print('Check your value and try again')
            exit()
        
        ib = bx / (2.0 * pi)
        jb = by / (2.0 * pi) 
        kb = bz / (2.0 * pi)
        
        with alive_bar(index_select, title='Computing__COM ') as bar:
            for i in range(0,index_select):  
                for t in range(0, trajec_num): 
                    shape_ = XYZ[atoms_key[i]].shape[2]
                    xc, yc, zc, gc , gc_xyz = [],[],[], [], [] 
                    for j in range(0, nmol[atoms_key[i]]):
                        Mass_ = Mass[atoms_key[i]][t, j, c[i]]
                        if imcon in [1, 2, 3, 4, 5, 6]:

                            #################################################################################
                            ######## firstly i start putting atoms in the orthorombic box               #####
                            ######## to do that i use a module's colled orthorhombic_transform          #####
                            ######## it's very usefull and efficient enough  when the systems           #####
                            ######## aren't  orthorhombic surch as hexagonal, triclinic or              #####
                            ######## monoclinic, the centers of mass are always situated in the         #####
                            ######## orthorhombic box and we can not use correctly the minimal          #####
                            ######## image convention if you the system has not been defined like that  ##### 
                            #################################################################################

                            xx_ = XYZ[atoms_key[i]][t, j, :][c[i], 0:1]
                            yy_ = XYZ[atoms_key[i]][t, j, :][c[i], 1:2]
                            zz_ = XYZ[atoms_key[i]][t, j, :][c[i], 2:3]
                         
                            xx, yy, zz = orthorhombic_transform(xx_, yy_, zz_, bx, by, bz, imcon=imcon, angle=angle)  # orthorhombic transformation
                            xx, yy, zz =  xx/ ib, yy/ jb, zz/ kb
                    
                        mss = Mass_
    
                        sin_x, cos_x = np.sin(xx) * ib, np.cos(xx) * ib
                        sin_y, cos_y = np.sin(yy) * jb, np.cos(yy) * jb
                        sin_z, cos_z = np.sin(zz) * kb, np.cos(zz) * kb

                        prod_sin_x = (sin_x * mss).sum() / mss.sum()
                        prod_sin_y = (sin_y * mss).sum() / mss.sum()
                        prod_sin_z = (sin_z * mss).sum() / mss.sum()
                        prod_cos_x = (cos_x * mss).sum() / mss.sum()
                        prod_cos_y = (cos_y * mss).sum() / mss.sum()
                        prod_cos_z = (cos_z * mss).sum() / mss.sum()
                        
                        argu_x = np.arctan2(-prod_sin_x, - prod_cos_x) + pi
                        argu_y = np.arctan2(-prod_sin_y, - prod_cos_y) + pi
                        argu_z = np.arctan2(-prod_sin_z, - prod_cos_z) + pi

                        ###############################################################################
                        ###########    final values of centers of mass in the orthorhombic box  #######
                        ###############################################################################

                        cmx = (argu_x * ib).round(max_float)    # center of mass x in orthorhombic system
                        cmy = (argu_y * jb).round(max_float)    # center of mass y in orthorhombic system
                        cmz = (argu_z * kb).round(max_float)    # center of mass y in orthorhombic system
                            
                        if  atoms_select == 'ALL':
                            
                            ###########################################################################
                            ######       reconstruction of the complet atomic system            #######
                            ######       only when the key word is defined on 'ALL'             #######
                            ######       because the present code need to use all atoms         #######
                            ######       to compute the true centers of mass before building    #######
                            ######       the complet system, you can't split the molecules      #######
                            ###########################################################################

                            xx, yy, zz = xx * ib, yy * jb, zz * kb
                            xx1, yy1, zz1 = Atoms_In_BOX(x = xx, y = yy, z = zz, imcon = imcon, CELL = CELL)     # putting atoms inside the box
                            dx, dy, dz = (cmx-xx1), (cmy-yy1), (cmz-zz1)
                            new_xyz_val = Redim_Atoms_In_BOX(x = xx1, y = yy1, z = zz1, dx = dx, dy = dy, dz = dz, 
                            imcon = imcon, CELL = CELL, angle = angle)  # criteria minimal image convention 
                            gc_xyz.append(new_xyz_val)
                                                                
                        xc.append(cmx),yc.append(cmy),zc.append(cmz) 

                        ###########################################################################
                        #######    the true centers of mass in the real box.              #########
                        #######    To compute these values i used the inverse scheme      #########
                        #######    using in the orthorhombic_transform, it has been       #########
                        #######    implemented in the module called inverse_transform     #########
                        ###########################################################################

                        cmx, cmy, cmz = inverse_transform(cmx, cmy, cmz, imcon, angle) 
                        gc.append([cmx, cmy, cmz])
                
                    new_tabx[i].append(xc), new_taby[i].append(yc), new_tabz[i].append(zc)
                    center_of_mass[i].append(gc)
                    if atoms_select == 'ALL' :
                        XYZ_scale[i].append(gc_xyz)
                        
                center_of_mass[i] = np.array(center_of_mass[i])
                if atoms_select == 'ALL' :
                    XYZ_scale[i] = np.array(XYZ_scale[i]).reshape((trajec_num, nmol[atoms_key[i]] , nsit[atoms_key[i]], 3))
   
                sleep(.001)
                bar()

        for i in range(0, index_select):
            c[i] = 0

            Data[i] = center_of_mass[i]
            for t in range(0, trajec_num):
                cc = ['COM {} - {}'.format( trajec_key, int(w)) for w in range(0,nmol[atoms_key[i]])]
                gam2[i].append(cc)

            dic = dict(NAME = gam2[i], CENTER_X = new_tabx[i], CENTER_Y = new_taby[i], CENTER_Z = new_tabz[i])
            DataFrame[i] = pd.DataFrame(dic)
            DataFrame[i].set_index('NAME', inplace = True)
        
        ###########################################################################
        ########## the  history for each molecule has been computing here n########
        ###########################################################################

        xb = np.array([pd.DataFrame(Data[index_DF][w], columns=['CENTER_X', 'CENTER_Y', 'CENTER_Z']).iloc[key_num, [0, 1]].values for w in range(0, trajec_num)])

        if return_XYZ_CENTER == True:
            if return_XYZ_CENTER_AS == 'DataFrame':
                return DataFrame[index_DF]
            elif return_XYZ_CENTER_AS == 'XYZ':
                return   Data
            else:
                @decor
                def print_error():
                    print("ValueError 😊")
                    print('return_XYZ_CENTER_AS | XYZ or DataFrame |')
                    print('Put on of these values above and run again')
                exit()
        
        elif return_XYZ_CENTER == False:
            return "END COMPUTING OF CENTER OF MASS"
        else:
            @decor
            def print_error():
                print("ValueError 😊")
                print('return_XYZ_CENTER is a bolean type')
                print('change your value and try again')
            exit()

    def DataViZ(self, key = 'plot', color = 'g',
    ls = 'dashdot', fontsize = 'medium',
    loc = 'lower right', lw = 1., s = 50, edgecolor = 'k'):

        def decor(func):
            def wrap():
                print("=======================================================")
                func()
                print("=======================================================")
            return wrap() 
            
        linestyle = ['-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted']
        fs = ['x-small', 'medium', 'x-large', 'large', 'small']
        location = ['best','upper right','upper left','lower left','lower right','right','center left',
        'center right','lower center','upper center','center']
        
        if loc not in location:
            @decor 
            def print_error():
                print('Error 😊')
                print('loc not in list >>>', location)
            exit()


        
        if ls not in linestyle:
            @decor 
            def print_error():
                print('Error 😊')
                print('ls not in list >>>', linestyle)
            exit()

        if fontsize not in fs:
            @decor 
            def print_error():
                print('Error 😊')
                print('fontsize not in list >>> ', fs)
            exit()
           	
        if key == 'plot':
            
            plt.style.use('ggplot')
            fig = plt.figure(figsize = (5,5))
            ax = fig.add_subplot(111)

            ax.plot(xb[:,0], xb[:,1], linestyle = ls, color = color, lw = lw,label = 'brownian motion')
            ax.scatter(xb[:,0], xb[:,1], c = xb[:, 0], edgecolor = edgecolor, s = s, cmap = plt.cm.Set1)
            ax.set_xlabel('X COORDINATE', fontsize = fontsize)
            ax.set_ylabel('Y COORDINATE', fontsize = fontsize)
            ax.set_title('COM {} TRAJECTORY'.format(idd), fontsize = fontsize)
            ax.legend(loc = loc, fontsize = fontsize)

            return plt.show()
       
        else:
            @decor
            def print_error():
                print("Error 😊")
                print("Impossible to show the curve,  key is not defined on 'plot' ")
            exit()
    			
    def Build_System(self):
        def decor(funct):
            def wrap():
                print("==========================================================")
                funct()
                print("==========================================================")
            return wrap()

        if ind == 'ALL':
            return XYZ_scale
        else:
            @decor
            def print_error():
                print('InputError 😊')
                print('Impossible to show the news XYZ_new positions')
                print("It only works when the keyword atoms_select is defined on 'ALL'")
                print('because you use all the atoms to compute the real centers of mass')
                print("So, if you want to view new atomic positions use 'ALL' on atoms_select")
                print('')
                print('Do you want to continue ? Yes/No')
                response = str(input())
                if response == 'Yes':
                    print('CNTINUE ...')
                elif response == 'No':
                    print('EXIT() ...')
                else:
                    while response not in ['Yes', 'No']:
                        print('Bad response')
                        response = str(input())

                        if response == 'Yes':
                            print('Continue ...')
                        elif response == 'No':
                            print('EXIT() ...')

    def INVERSE_TRANSFORM(self, coordinates: np.ndarray, new_dim : np.ndarray, old_dim: np.ndarray, 
    imcon : int, type = 'hexagonal', center: np.ndarray=None, fcs: float = None, name = None):
        
        self.shape = coordinates[0].shape  
        self.store = []
        self.val_i = [16, 1]

        file = open('cation__.xyz', 'w')
        file.write('340\n')
        file.write('cation\n')


        if imcon in [1, 2, 4] and type == 'hexagonal':
            for t in range(1):
                for j in range(self.shape[1]):
                    for k in range(self.shape[2]):
                        x, y, z = coordinates[t, j, k, :]
                        if imcon in [1, 2, 4] and type == 'hexagonal':
                            
                            pbc = 2. * np.cos(pi/6.) * x + y 
                            if pbc < 0:
                                x = x + old_dim[0][0]
                            elif pbc > (2. * np.cos(pi / 6.) * old_dim[0][0]):
                                x = x - old_dim[0][0] 

                            if z < 0:
                                z  = z + old_dim[2][2]
                            elif z > old_dim[2][2]:
                                z = z - old_dim[2][2]


                            # build orthorhombic system

                            if x < 0:
                                x = x + old_dim[0][0]
                            else:
                                x = x 
                            
                            if old_dim[0][0] <= new_dim[0][0]:
                                d = new_dim[0][0] -  old_dim[0][0]
                                x = x + d / 2.
                            else:
                                print("ErrorDim : the value along x direction from new_dim is lower than x value from old_dim" )
                                exit()

                            if old_dim[0][0] <= new_dim[1][1]:
                                d = new_dim[0][0] -  old_dim[1][1]
                                y = y + d / 2.
                            else:
                                print("ErrorDim : the value along y direction from new_dim is lower than y value from old_dim" )
                                exit()

                            if old_dim[2][2] <= new_dim[2][2]:
                                d = new_dim[2][2] -  old_dim[2][2]
                                z = z + d / 2.
                            else:
                                print("ErrorDim : the value along z direction from new_dim is lower than z  value from old_dim" )
                                exit()
    
                        self.store.append([name[k], np.round(x, 5), np.round(y,5), np.round(z,5) ])
                        value = '{}    {}    {}    {}'.format( name[k], np.round(x, 5), np.round(y,5), np.round(z,5) )
                        file.write(value+'\n') 
        
        elif imcon == 3 and type in ['cubic', 'orthorhombic', 'quadratic']:

            a_new, b_new, c_new = new_dim[0][0], new_dim[1][1], new_dim[2][2]
            a_old, b_old, c_old = old_dim[0][0], old_dim[1][1], old_dim[2][2]
            b_h = (b_old * np.cos(pi / 6))
            self.site = [(a_old / 4., b_h / 4.), ((a_old - a_old/4.), b_h/4.), (a_old / 4.0, (b_h-b_h/4.)), ((a_old - a_old/4.) , (b_h-b_h/4.))]
            self.distance = c_old

            for t in range(1):
                self.p, self.f, self.nm = 0, 1, None
                for j in range(self.shape[1]):
                    for i in range(2):
                        test, b = [], 0
                        x, y, z = coordinates[i][t, j, :, 0], coordinates[i][t, j, :, 1], coordinates[i][t, j, :, 2]
                        x_c, y_c, z_c = center[i][t, j, 0], center[i][t, j, 1], center[i][t, j, 2]
                        dx, dy, dz = x-x_c, y-y_c, z-z_c

                        for k in range(self.val_i[i]):#range(self.shape[2]):
                            if y[k] < 0: 
                                y[k] = y[k] + b_old 
                            elif y[k] > b_old:
                                y[k] = y[k] - b_old
                            
                            #if z[k] < 0: 
                            #    z[k] = z[k] + c_old 
                            #elif z[k] > c_old:
                            #    z[k] = z[k] - c_old
    
                            #if x[k] < 0: 
                            #    x[k] = x[k] + a_old 
                            #elif x[k] > a_old:
                            #    x[k] = x[k] - a_old
                        
                            pbc = 2. * np.cos(pi / 6.) * x[k] + y[k]

                            if pbc > (2.* a_old * np.cos(pi/ 6.)):
                                x[k] = x[k] - a_old
                            elif pbc < 0:
                                x[k] = x[k] + a_old
                            else:
                                x[k] = x[k]

                        for w in range(self.val_i[i]):#range(self.shape[2]):
                            if y[w] <= b_new * np.cos(pi / 6.):
                                test.append(True)
                            else:
                                test.append(False)

                        if  False not in test:
                            for k in range(self.val_i[i]):#range(self.shape[2]):
                                if i == 1:
                                    b = self.val_i[0]
                                else:
                                    b = k

                                coordinates[i][t, j, k, 0], coordinates[i][t, j, k, 1], coordinates[i][t, j, k, 2] = x[k], y[k], z[k]
                                center[i][t, j, 0], center[i][t, j, 1], center[i][t, j, 2] = x_c, y_c, z_c
                                self.store.append([name[k], np.round(x[k], 5), np.round(y[k],5), np.round(z[k],5) ])
                                value = '{}    {}    {}    {}'.format( name[b], np.round(x[k], 5), np.round(y[k],5), np.round(z[k],5) )
                                file.write(value+'\n') 

                        else:
                            self.p += 1

                            if self.p < 3 :
                                z_c = self.distance + fcs * self.f#+c_old 
                            else:
                                self.f += 1
                                self.p = 0
                                z_c = self.distance + self.f * fcs #+ c_old 
                                rdn = np.random.rand()
                                self.site = [((a_old + rdn) / 4., b_h / 4.), ((a_old - a_old/4.), b_h/4.), (a_old / 4.0, (b_h-b_h/4.+rdn)), ((a_old - a_old/4.-rdn) , (b_h-b_h/4.))]

                            n = None 
                            if self.site:
                                n = np.random.choice(len(self.site))
                            else:
                                rdn = np.random.rand()
                                self.site = [(a_old / 4., b_h / 4.), ((a_old - a_old/4.-rdn), b_h/4.), (a_old / 4.0, (b_h-b_h/4.)), ((a_old - a_old/4. - rdn) , (b_h-b_h/4.+rdn))]
                                n = np.random.choice(len(self.site))
                            
                            x_c, y_c = self.site[n]
                            del self.site[n]

                            for w in range(self.val_i[i]):#range(self.shape[2]):
                                b += 1
                                x[w] = dx[w] + x_c
                                y[w] = dy[w] + y_c
                                z[w] = dz[w] + z_c 

                                while z[w] < (self.distance-5): 
                                    z[w] = z[w] + 0.1

                                for v in range(j):
                                    for q in range(2):
                                        ddz = np.sqrt((center[q][t, v, 2] - z_c)**2+(center[q][t, v, 1] - y_c)**2+(center[q][t, v, 0] - x_c)**2)
                                        while ddz < 4.5:
                                            z_c = z_c + 1.
                                            x_c = x_c + 0.2
                                            y_c = y_c + 0.2 * np.cos(pi / 6.0)

                                            x[w] = dx[w] + x_c
                                            y[w] = dy[w] + y_c
                                            z[w] = dz[w] + z_c
                                            ddz = np.sqrt((center[q][t, v, 2] - z_c)**2+(center[q][t, v, 1] - y_c)**2+(center[q][t, v, 0] - x_c)**2)
                                            self.distance = z_c

                                pbc = 2. * np.cos(pi / 6.) * x[w] + y[w]

                                if pbc > (2.* a_old * np.cos(pi/ 6.)):
                                    x[w] = x[w] - a_old
                                else:
                                    x[w] = x[w]
                                if i == 1:
                                    b = self.val_i[0]
                                else:
                                    b = w
                                coordinates[i][t, j, w, 0], coordinates[i][t, j, w, 1], coordinates[i][t, j, w, 2] = x[w], y[w], z[w]
                                center[i][t, j, 0], center[i][t, j, 1], center[i][t, j, 2] = x_c, y_c, z_c

                                self.store.append([name[b], np.round(x[w], 5), np.round(y[w],5), np.round(z[w],5) ])
                                value = '{}    {}    {}    {}'.format( name[b], np.round(x[w], 5), np.round(y[w],5), np.round(z[w],5) )
                                file.write(value+'\n') 
            
    