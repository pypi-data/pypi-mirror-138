from typing import Iterable
import numpy as np
import pandas as pd
from matrix_package.params import params_control, params_, param_time
from matrix_package.params import params_gdr
from alive_progress import alive_bar
from time import sleep

class Control:
    
    def Classical_MD(self,mol_type : int = None, nmol : list = None, multi_treatment : any = False,
    nsit : list = None, input_name : str = None, trajec_num : int = None, keytrj = 0, header : any = False, 
    dtype = np.float32):

        """
        Classical_MD is a programming code only used to read the HISTORY files from DL_POLY and extracts several
        useful data for the next processes surch as computing center-of-masses, structural, dynamics and 
        thermodynamics properties.

        It has several compulsory inputs:

        * mol_type: used for defining the number of molecules does your integral system has 
        * input_name: is the name of your input contening all informations, but WARNING: being sure that your input file name has the HISTORY extension [.hist or .HIST]. 
        It means that if the name of your input file is <<coordinates>> then you may write <<coordinates.hist or coordinates.HIST>>.
        * nsit: used to specify how many atoms does your system has per molecules . 
        * nmol: used to specify how many molecules does your system has. 
        * trajec_num: is defining how many trajectrories does your input file has. 
        * keytrj used to specify what informations does your HISTORY file has. 

        >>> keytrj = 0 means only positions
        >>> keytrj = 1 means positions + velocities 
        >>> keytrj = 2 means positions + velocities + forces
        
        for the keyword keytrj the default value is 0. 
        * header: used to specify if your HISTORY file has a header, generally printed before the first timestep (first two lines)
        * dtype: used to specify the max float
        * multi_treatment: used to read several files at the same time but doesn't work yet for this version.

        >>>>>>>>>>>>>> INPUTS EXAMPLES  AND DETAILS >>>>>>>>>>>>>>
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        >>> mol_type = 2 
        >>> nmol = [20 , 20] because mol_type = 2 if mol_type = 1 so nmol = [20] etc ....
        >>> nsit = [16, 1]
        >>> trajec_num = 1000 
        
        """

        params_(mol_type)

        global data, cell, Time, data_, coordinates, atom_name
        global xyz_, dataframe_, mass_,name_init, charge, keytrajec, vel, forces, n_mol
        name_init = input_name

        t1 = list()
        t2 = float()
        t3 = int()
        t4 = bool()
        t5 = str()
        t6 = dict()

        coordinates, mass, natom, charge,data  = params_control()
        Time = []

        keytrajec = keytrj
        n_mol =nmol

        def decor(func):
            def wrap():
                print("==========================================")
                func()
                print("==========================================")
            return wrap()
        
        if input_name:
            if type(input_name) != type(t5):
                @decor
                def print_error():
                    print("TypeError  😊")
                    print("input_name is a string")
                    print('Put a string and run again')
                exit()
            else:
                if input_name[-5:] not in  ['.HIST', '.hist']:
                    @decor
                    def print_error():
                        print("NameError 😊")
                        print("Wrong input name. Try 'YourInputName.HIST' or 'YourInputName.hist ")
                    exit()
        else:
            @decor
            def print_error():
                print("FileNotFoundError 😊")
                print("input_name cannot be Empty")
            exit()

        if not nmol:
            @decor 
            def print_error():
                print('InputError 😊')
                print('nmol cannot be Empty')
            exit()
        else:
            if type(nmol) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("nmol is a list not any other type")
                    print('nmol, ',type(t1))
                    print("Put nmol as list and try again")
                exit()   
            else:
                for i, val in enumerate(nmol):
                    if type(val) != type(t3):
                        @decor 
                        def print_error():
                            print('TypeError 😊')
                            print("The values in nmol should be integers")
                            print(type(t3))
                            print("Check your values and correct them")
                            print('The bad found is :', val, 'index = ', i, 'from', nmol)
                        exit()
                    else:
                        if val <= 0:
                            @decor 
                            def print_error():
                                print('ValueError 😊')
                                print("The values in nmol should be bigger than 0")
                                print("Check your values and correct them")
                                print('The bad found is :', val, 'index = ', i, 'from', nmol)
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
                    print("Put nmol as a list and try again")
                exit()   
            else:
                for i, val in enumerate(nsit):
                    if type(val) != type(t3):
                        @decor 
                        def print_error():
                            print('TypeError 😊')
                            print("The values in nsit should be integers")
                            print(type(t3))
                            print("Check your values and correct them")
                            print('The bad found is :', val, 'index = ', i, 'from', nsit)
                        exit()
                    else:
                        if val <= 0:
                            @decor 
                            def print_error():
                                print('ValueError 😊')
                                print("The values in nsit should be bigger than 0")
                                print("Check your values and correct them")
                                print('The bad found is :', val, 'index = ', i, 'from', nsit)
                            exit()

        if len(nsit) != mol_type or len(nmol) != mol_type:
            @decor
            def print_error():
                print("InputError 😊")
                print("Length nsit or Length nmol are not the same with mol_type")
                print('You should always have Length(nsit or nmol) = mol_type')
                print('Have a look on your inputs to see what happened, correct your mistake and try again')
            exit()

        if type(keytrj) != type(t3):
            @decor 
            def print_error():
                print('TypeError 😊')
                print('keytrj is an integer not any other type')
                print('keytrj, ', type(t3))
                print('Put an integer as an input and run again')
            exit()
        else:
            if keytrj < 0:
                @decor 
                def print_error():
                    print('ValueError 😊')
                    print('keytrj cannot be negative')
                exit()

        if type(header) != type(t4):
            @decor
            def print_error():
                print('TypeError 😊')
                print('header a boolean type not any other type')
                print('header ',type(t4))
                print('Put a boolean type and run again')
            exit()

        if type(multi_treatment) != type(t4):
            @decor
            def print_error():
                print('TypeError 😊')
                print('multi_treatmentis a boolean type not any other type')
                print('multi_treatment ',type(t4))
                print('Put a boolean type and run again')
            exit()
        
        # opening  input and reading input file to extract all informations
        # that will be using later by another code programming 
         
        file = open(input_name, "r")

        with alive_bar(trajec_num, title='Initialization') as bar:

            for t in range(0, trajec_num):
            
                if header == True and t==0:
                    sys_name = file.readline().split() 
                    sys_info = file.readline().split()
        
                line = file.readline().split()
    
                timestep, time, magatm, levcgf, imcon0, lf = line
                Time.append(float(time))
                
                celx = [float(value) for value in file.readline().split()]
                cely = [float(value) for value in file.readline().split()]
                celz = [float(value) for value in file.readline().split()]

                cell = [celx, cely, celz]

                for i in range(0,mol_type):
                    vel, forces = [],[]

                    for j in range(0,nmol[i]):
                        for k in range(0,nsit[i]):
                            firstline = file.readline().split()
                            ntm, rang, mas, chg = firstline

                            if keytrj == 0:
                                secondline = file.readline().split()

                                posx, posy, posz = secondline
                                coordinates[i].append([float(posx), float(posy), float(posz)])
                                mass[i].append(round(float(mas),10))
                                natom[i].append(str(ntm))
                                charge[i].append(round(float(chg),10)) 
                            
                            elif keytrj == 1:
                                secondline = file.readline().split()
                                thirdline = file.readline().split()

                                posx, posy, posz = secondline
                                vx, vy, vz = thirdline

                                coordinates[i].append([float(posx), float(posy), float(posz),float(vx), float(vy), float(vz)])
                                mass[i].append(round(float(mas),10))
                                natom[i].append(str(ntm))
                                charge[i].append(round(float(chg),10)) 
                                vel.append([float(vx), float(vy), float(vz)])

                            elif keytrj == 2:
                                secondline = file.readline().split()
                                thirdline = file.readline().split()
                                fourthline = file.readline().split() 

                                posx, posy, posz = secondline
                                vx, vy, vz = thirdline
                                fx, fy, fz = fourthline

                                coordinates[i].append([float(posx), float(posy), float(posz),float(vx), float(vy), float(vz),float(fx), float(fy), float(fz)])
                                mass[i].append(round(float(mas),10))
                                natom[i].append(str(ntm))
                                charge[i].append(round(float(chg),10)) 
                                vel.append([float(vx), float(vy), float(vz)])
                                forces.append([float(fx), float(fy), float(fz)])
                            
                            else:
                                @decor
                                def print_error():
                                    print('ValueError 😊')
                                    print(" Bad keytrj value")
                                    print("keytrj not in [0, 1, 2]")
                                    print("Check your value and try again")
                                    info = """ 
                        - keytrj = 0 means only positions
                        - keytrj = 1 means positions + velocities 
                        - keytrj = 2 means positions + velocities + forces\n"""
                                    print(info)
                                    
                                exit()

                sleep(.001)
                bar()

        for i in range(0,mol_type):
            data[i] = pd.DataFrame(natom[i], columns = ['atom name'])
            
            if keytrj == 0:
                data[i][['X', 'Y', 'Z']] = coordinates[i]
            
            elif keytrj == 1:
                data[i][['X', 'Y', 'Z', 'VX', 'VY', 'VZ']] = coordinates[i] 
            
            elif keytrj == 2:
                data[i][['X', 'Y', 'Z', 'VX', 'VY', 'VZ', 'FX', 'FY', 'FZ']] = coordinates[i]
            
            data[i]['mass'] = mass[i]
            data[i]['charge'] = charge[i]
            #data[i].set_index('atom name', inplace=True) #reset index for all data frame 
        
        # creating a dictionary to store three kinds of informations 
        # Molecule data, box size and time simulation 

        data_ = {'Molecule data' : data, 'box size' : cell, 'time simulation' : Time}

        xyz_, dataframe_, mass_ = params_gdr()
        atom_name = []

        for i in range(0, len(xyz_)):
            dataframe_[i] = data[i]
            xyz_[i] = dataframe_[i].iloc[:, [1,2,3]].values 
            atom_name.append(dataframe_[i].iloc[:, 0])

        for i in range(0, len(charge)):
            charge[i] = np.array(charge[i], dtype = dtype) 
            mass[i] = np.array(mass[i], dtype = dtype)
            mass_[i] = mass[i]
            atom_name[i] = np.array(atom_name[i])

            if keytrj == 1:
                vel[i] = np.array(vel[i], dtype = dtype)
            
            elif keytrj == 2:
                vel[i] = np.array(vel[i], dtype = dtype)
                forces[i] = np.array(forces[i], dtype = dtype)

        # Final result is returning as a data.frame for more clarity 

        return data_

    def Ab_Initio_MD(self, mol_type : int = None, nmol : list = None, input_name : str = None, trajec_num : int = None,
    M_array : list = None, nsit_M : list = None, multi_treatment : any = False,
    mass_atom : dict = None, CELL : list = None, dtype = np.float32):

        """

        Ab_initio_MD is a programming code only used to read the XYZ files and extracts several
        data, useful for the next processes surch as computing center-of-masses, structural, dynamics and 
        thermodynamics properties.

        It has several compulsory inputs
        * mol_type: used for defining the number of molecules does your systems has 
        * input_name: is the name of your input contening all informations, but WARNING: being sure that your input file name has the XYZ extension [.XYZ or .xyz]. 
        It means that if the name of your input file is <<coordinates>> then you may write <<coordinates.xyz or coordinates.XYZ>>.
        * trajec_num: used to define how many trajectrory does your input file has. 
        * mass_atom: is contening the atom names and theirs masses. As you know the must XYZ files don't contain the atomic masses, nor even charges,
        that why in this code you've the possibility to add yourself these values. If it doesn't contain any values the default 
        values will be 1. for all atoms 
        * M_array: is a kernel used to select atoms properly in your input file, this keyword specifies how would you like 
        to select and classify atoms. 
        * nsit_M: used to specify how many atoms does your system has per molecules. 
        * multi_treatment: used to read several files at the same time but doesn't work yet for this version.
        * The Last one is CELL, same like mass_atom the XYZ files don't have the values for the box sizes but you may difine them here.  
        If there are not any values in CELL the default values are [[1.0, 0., 0.], [0., 1., 0.], [0., 0., 1.]], values for a unitary cubic cell. 

        >>>>>>>>>>>>>> INPUTS EXAMPLES  AND DETAILS >>>>>>>>>>>>>>
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        >>> mol_type = 2 
        >>> nmol = [20 , 20] because mol_type = 2 if mol_type = 1 so nmol = [20] etc ....
        >>> M_array = [[[0,40],[40,140],[140,320]],[[320,340]]]
        >>> nsit_M = [[2, 5, 9],[1]]
        >>> mass_atom = {'C':12.011, 'H':1.008, 'N':14.007,'Cl':35.453}
        >>> trajec_num = 1000 
        >>> CELL = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]] default values
        

        M_array shows that this system has four different atoms, for example (C, N, H, Cl) split in two categories given by keyword mol_type
        and each lists corresponding to each atoms, it means that:

        >>> [0, 40] = N, [40, 140] = C, [140, 320] = H, [320, 340] = Cl 
        your can compute the total nombers of atoms for each molecules by doing 
        
        >>> 40 - 0 = 40 N, 140 - 40 = 100 C, 320 - 140 = 180 H, 340 - 320 = 20 Cl 
        
        Here the system has two different molecules with 20 molecules. So we can compute how many atoms do we have per molecules 
        and these values are stored in the keyword nsit_M 

        So, to do that i divide :
        >>> 40 / 20 = 2 N, 100 / 20 = 5 N, 180 / 20 = 9 N and 20 / 20 = 1 Cl 
        That is why we have nsit_M = [[2, 5, 9], [1]], it means we have 16 atoms for the first molecule and 1 atom for the second.

        keyword mass_atom is a distionary contening several informations surch as the symbols for each atoms identical with the periodic table symbols.

        >>> let's take the case of carbon
        >>> 'C' = symbol 
        >>> 12.011 = is atomic mass of carbon

        """

        params_(mol_type)
        global data, cell, Time, data_, coordinates, atom_name
        global xyz_, dataframe_, mass_, name_init, tri_m
        name_init = input_name

        t1 = list()
        t2 = float()
        t3 = int()
        t4 = bool()
        t5 = str()
        t6 = dict()

        coordinates, mass, natom, charge, data  = params_control()

        [U_array, arr, atom_err,Time] = [[],[0],[],[]]

        def decor(func):
            def wrap():
                print("==========================================")
                func()
                print("==========================================")
            return wrap()

        if input_name:
            if type(input_name) != type(t5):
                @decor
                def print_error():
                    print("TypeError 😊")
                    print("input_name is a string")
                    print('Put a string and run again')
                exit()
            else:
                if input_name[-4:] not in ['.XYZ', '.xyz']:
                    @decor
                    def print_error():
                        print("NameError  😊")
                        print("Wrong input name. Try 'YourInputName.XYZ' or YourInputName.xyz ")
                    exit()
        else:
            @decor
            def print_error():
                print("FileNotFoundError 😊")
                print("input_name cannot be Empty")
            exit()
        
        if not nsit_M:
            @decor 
            def print_error():
                print('InputError 😊')
                print('nist_M cannot be Empty')
            exit()
        else:
            if type(nsit_M) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("nsit_M is a list not any other type")
                    print('nsit_M, ',type(t1))
                    print("Put nsit_M as list and try again")
                exit()
            else:
                for var in nsit_M:
                    if type(var) != type(t1):
                        @decor 
                        def print_error():
                            print('TypeError 😊')
                            print("The elements of nsit_M should be a list")
                            print(var, 'is not a', type(t1))
                        exit()
                    else:
                        for val in var:
                            if type(val) != type(t3): 
                                @decor 
                                def print_error():
                                    print('TypeError 😊')
                                    print("Problem with this list, ", var)
                                    print('All elements in the list above are not integers')
                                    print('bad value : ', val, 'correct that value and try again')
                                exit()
                            else:
                                if val < 0:
                                    @decor 
                                    def print_error():
                                        print('ValueError 😊')
                                        print("Problem with this list, ", var)
                                        print('All elements in the list above are not positive')
                                        print('bad value : ', val, 'correct that value and try again')
                                    exit()

        if not M_array:
            @decor 
            def print_error():
                print('InputError 😊')
                print('M_array cannot be Empty')
            exit()
        else:
            if type(M_array) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("M_array is a list not any other type")
                    print('M_array, ',type(t1))
                    print("Put M_array as list and try again")
                exit()
            else:
                for var in M_array:
                    if type(var) != type(t1):
                        @decor 
                        def print_error():
                            print('ErrorType 😊')
                            print("The elements of M_array should be a list")
                            print(var, 'is not a', type(t1))
                        exit()
                    else:
                        for val in var:
                            if type(val) != type(t1): 
                                @decor 
                                def print_error():
                                    print('ErrorType 😊')
                                    print("The sub elements of M_array should be a list")
                                    print(val, 'is not a', type(t1))
                                    print('Bad value : ', val, ' Correct that value and run again')
                                exit()
                            elif len(val) != 2:
                                @decor
                                def print_error():
                                    print('ErrorInput')
                                    print('The Length of the sub elemnts of M_array are not the same' )
                                    print('The size of, ', val, 'is different from 2')
                                exit()
                            else:
                                for val1 in val:
                                    if type(val1) != type(t3):
                                        @decor
                                        def print_error():
                                            print('ErrorType 😊')
                                            print("Problem with this list, ", val)
                                            print('All elements in the list above are not integers')
                                            print('bad value : ', val1, 'correct that value and try again')
                                        exit()
                                    else:
                                        if val1 < 0:
                                            @decor 
                                            def print_error():
                                                print('ValueError 😊')
                                                print("Problem with this list, ", val)
                                                print('All elements in the list above are not positive')
                                                print('bad value : ', val1, 'correct that value and try again')
                                            exit()
                  
        if not nmol:
            @decor 
            def print_error():
                print('InputError 😊')
                print('nmol cannot be Empty')
            exit()
        else:
            if type(nmol) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("nmol is a list not any other type")
                    print('nmol, ',type(t1))
                    print("Put nmol as list and try again")
                exit()   
            else:
                for i, val in enumerate(nmol):
                    if type(val) != type(t3):
                        @decor 
                        def print_error():
                            print('TypeError 😊')
                            print("The values in nmol should be integers")
                            print(type(t3))
                            print("Check your values and correct them")
                            print('The bad found is :', val, 'index = ', i, 'from', nmol)
                        exit()
                    else:
                        if val <= 0:
                            @decor 
                            def print_error():
                                print('ValueError 😊')
                                print("The values in nmol should be bigger than 0")
                                print("Check your values and correct them")
                                print('The bad found is :', val, 'index = ', i, 'from', nmol)
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
                    def print_eror():
                        print('ValueError 😊')
                        print('mol_type cannot be negative')
                    exit()

        if  not CELL:
            cell = np.array([[1., 0., 0.], [0., 1., 0.],[0., 0., 1.]]) 
            @decor
            def print_error():
                print('CELL is empty or not specified')
                print('Default values will be used')        
        else:
            if type(CELL) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("CELL is a list not any other type")
                    print('CELL, ',type(t1))
                    print("Put a list as an input and try again")
                exit()
            else:
                cell = CELL

        if mass_atom:
            if type(mass_atom) != type(t6):
                @decor
                def print_error():
                    print('TypeError 😊')
                    print('mass_atom is a dictionary not any other type')
                    print('mass_atom', type(t6))
                    print('Put a dict as an input and try again')
                exit()
            else:
                mass_list = list(mass_atom.keys())
                for val in mass_list:
                    if type(mass_atom[val]) != type(t2):
                        @decor
                        def print_error():
                            print('TypeError 😊')
                            print('The items values of mass_atom should be a float')
                            print('Bad value : ', dict(val = mass_atom[val]))
                            print('Correct this mistake and run again')
                        exit() 
                    else:
                        if mass_list.count(val) > 1 : 
                            @decor
                            def print_error():
                                print('ValueError 😊')
                                print('Several items are identical')
                                print('Bad value : ', val)
                                print('Remove the repeated value and run again')
                            exit()
                        else:
                            if mass_atom[val] < 0:
                                @decor 
                                def print_error():
                                    print('ValueError 😊')
                                    print("Problem with this dict, ", dict(val = mass_atom[val]), 'with val = {}'.format(val))
                                    print('The values of the items in this list below')
                                    print(mass_list, 'cannot be negative')
                                    print('Correct your mistakes try again')
                                exit()
        else:
            @decor
            def print_error():
                print('InputError 😊')
                print('mass_atom cannot be Empty')
            exit()

        if len(nsit_M) != mol_type or len(nmol) != mol_type:
            @decor
            def print_error():
                print("ValueError  😊")
                print("Length nsit or Length nmol not the same with mol_type")
                print('You should always have Length(nsit or nmol) = mol_type')
                print('Have a look on your inputs to see what happened, correct your mistake and try again')
            exit()

        if len(M_array) != len(nsit_M):
            @decor 
            def print_error():
                print('InputError 😊')
                print("M_array doesn't have the same Length with nsit_M ")
                print("Correct your mistake and run again")
            exit()
        
        if type(multi_treatment) != type(t4):
            @decor
            def print_error():
                print('TypeError 😊')
                print('multi_treatmentis a boolean type not any other type')
                print('multi_treatment ',type(t4))
                print('Put a boolean type and run again')
            exit()
        
        summ = 0

        for i in range(0, mol_type):
            summ = summ + np.sum(len(list(M_array[i])))
        
        summ = 0     

        for i in range(0, mol_type):
                for j in range(0,nmol[i]):
                    for u in range(0,len(nsit_M[i])):
                        for k in range(0,nsit_M[i][u]):
                            if j == 0:
                                v = k + M_array[i][u][0] 
                            elif j >=1:
                                v = k + nsit_M[i][u] * j + M_array[i][u][0]
                            U_array.append(v) 
        
        MATRIX_MOL = np.array(list(U_array))

        sum_ = 0
        
        for i in range(0, mol_type):
            sum_ = sum_ + np.sum(nsit_M[i]) * nmol[i]
            arr.append(sum_)
        
        sum_ = 0
        
        # opening and reading input file to extract all informations
        # that will be using later by another programming code
        # atoms extract process 

        file = open(input_name, "r")

        with alive_bar(trajec_num, title='Initialization') as bar:
            for t in range(0, trajec_num):
                [alloc1, alloc2,columnX,columnY,columnZ] = [[],[],[],[],[]]

                total_atom = file.readline()
                Time_, time = file.readline().split() 

                Time.append(float(time))

                for i in range(0, int(total_atom)):
                    firstline = file.readline().split()

                    if len(firstline) == 4:
                        ntm, posx, posy, posz = firstline
                        alloc1.append([str(ntm), float(posx), float(posy), float(posz)])
                    else:
                        ntm, posx, posy, posz, vx, vy, vz = firstline
                        alloc1.append([str(ntm), float(posx), float(posy), float(posz)])

                df = pd.DataFrame(alloc1, columns = ['atom name', 'X', 'Y', 'Z'])
                
                for x in df['X']:
                    columnX.append(float(x))
                
                for y in df['Y']:
                    columnY.append(float(y))
                
                for z in df['Z']:
                    columnZ.append(float(z))
                
                for mas_ in df['atom name']:
                    #if mass_atom:
                    if mas_ in  mass_atom.keys():
                        value = mass_atom[mas_]
                    else:
                        atom_err.append([mas_, 'not in', list(mass_atom.keys())])
                        @decor
                        def print_error():
                            print('NameError 😊')
                            print('atom name not in TRAJEC.XYZ')
                            print('Have a look on your mistakes below and correct them')
                            print('The problem comes from mass_atom\n')
                            print(atom_err)
                        exit()
                    alloc2.append(float(value))
                    #else:
                    #    alloc2.append(1.)

                df['X'],df['Y'],df['Z'], df['mass'] = columnX, columnY, columnZ, alloc2
                M_2D_array = df.values 
                M_2D_array = M_2D_array[MATRIX_MOL,]
                
                for j in range(0, mol_type):
                    if mol_type > 1:
                        for val1 in M_2D_array[arr[j]:arr[j+1], 0:5]:
                            coordinates[j].append(val1)
                    elif mol_type == 1:
                        for val1 in M_2D_array[0:arr[1], 0:5]:
                            coordinates[j].append(val1)
                    else:
                        @decor
                        def print_error():
                            print('ValueError 😊')
                            print('mol_type not in [1, ->[')
                            print("Put the correct value and try again")
                        exit()
            
                sleep(.001)
                bar()     

        for i in range(0,mol_type):
            data[i] = pd.DataFrame(coordinates[i], columns=['name','X','Y','Z','mass'])
            #data[i].set_index('atom name', inplace=True) #reset index for all data frame
        
        data_ = {'Molecule data' : data, 'box size' : cell, 'time simulation' : Time}

        xyz_, dataframe_, mass_ = params_gdr()
        atom_name = []

        for i in range(0, len(xyz_)):
            dataframe_[i] = data[i]
            xyz_[i] = dataframe_[i].iloc[:, [1,2,3]].values 
            mass_[i] = dataframe_[i].iloc[:, 4:5]
            mass_[i] = np.array(mass_[i], dtype = dtype)
            atom_name.append(dataframe_[i].iloc[:, 0])

        for i in range(0, len(xyz_)):
            atom_name[i] = np.array(atom_name[i])
        
        # returning the Final result as a data.frame for more clarity

        return data_
    
    def Lammps(self, mol_type : int =  None, nmol : list =  None, input_name : str = None, trajec_num : int = None,
    M_array : list = None, nsit_M : list = None, multi_treatment : any = False, mass_atom : Iterable [dict]  = None, CELL : list = None, 
    dtype = np.float32, keytrj : int = 0):

        """

        Lammps is a programming code only used to read Trajectories from LAMMPS outputs files and extracts several\n 
        data, useful for the next processes such as computing center-of-masses, structural, dynamics and\n
        thermodynamics properties.\n

        It has several compulsory inputs\n
        
        * mol_type  :\n 
        Used for defining the number of molecules does your integral system has.\n
        
        * trajec_num:\n 
        Used to specify how many trajectories does your system has.\n 
        
        * input_name  :\n 
        Is your lammps input name but warning don't forget to put lammps extentions [.lps]\n 
        of file at the end of your input file name. It means that if your input file name is <<coordinates>>\n 
        then you may write <<coordinates.lps>>.\n 
        
        * mass_atom :\n 
        Is containing atoms names, atoms id and theirs masses. As you know the must LAMMPS outputs files don't\n 
        contain the atomic masses, nor even charges,that why in this code you've the possibility to add yourself\n 
        these values. If it doesn't contain any values the default values will be 1. for all atoms\n 
        
        * M_array   :\n 
        Is a kernel used to select atoms properly in your input file, this keyword specifies how would you like\n 
        to select and classify atoms.\n 
        
        * nsit_M    : \n
        Is different from the nsit keyword used in Classical_MD, the structure is different, you use this keyword\n 
        to specify how many atoms does your system has per molecules. \n
        
        * keytrj    : \n
        Used to specify what informations does your LAMMPS output file has. \n

        >>> keytrj = 0 means only positions
        >>> keytrj = 1 means positions + velocities 
        >>> keytrj = 2 means positions + velocities + forces
        
        for the keyword keytrj the default value is 0. 
        * dtype    :\n 
        Used to specify the max float
        
        * multi_treatment: \n
        Used to read several files at the same time but doesn't work yet for this version.\n
        
        * CELL     :\n 
        Used to define the default values of the simulations box.\n

        
        >>>>>>>>>>>>>> INPUTS EXAMPLES  AND DETAILS >>>>>>>>>>>>>>
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        >>> mol_type = 2 
        >>> nmol = [20 , 20] because mol_type = 2 if mol_type = 1 so nmol = [20] etc ....
        >>> M_array = [[[0,40],[40,140],[140,320]],[[320,340]]]
        >>> nsit_M = [[2, 5, 9],[1]]
        >>> mass_atom = {'C': [1, 12.011], 'H': [2, 1.008], 'N': [3, 14.007] ,'Cl': [4, 35.453] }
        >>> trajec_num = 1000 
        >>> CELL = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]] default values
        

        M_array shows that this system has four different atoms, for example (C, N, H, Cl) split in two \n
        categories given by keyword mol_type and each list corresponding to each atom, it means that:\n

        >>> [0, 40] = N, [40, 140] = C, [140, 320] = H, [320, 340] = Cl 
        your can compute the total nomber of atoms for each molecule by doing \n
        
        >>> 40 - 0 = 40 N, 140 - 40 = 100 C, 320 - 140 = 180 H, 340 - 320 = 20 Cl 
        
        Here the system has two different molecules with 20 molecules. So we can compute how many atoms 
        do we have per molecules and these values are stored in the keyword nsit_M \n

        So, to do that i divide :
        >>> 40 / 20 = 2 N, 100 / 20 = 5 C, 180 / 20 = 9 H and 20 / 20 = 1 Cl 
        That is why we have nsit_M = [[2, 5, 9], [1]], it means we have 16 atoms for the first (2 Nitrogens, 5 Carbons, 9 Hydrogens)\n
        molecule and 1 atom for the second (Only the chlorine).\n

        the keyword mass_atom is a distionary containing several informations such as the symbols for each atom identical with the \n
        periodic table symbols.\n

        >>> For the case of Carbon
        >>> 'C' is the symbol 
        >>> [1, 12.011] = 1 is index of the carbon in the lammps ouput (always an integer number) 
        and 12.011 is its atomic mass (always a real number)

        """

        def decor1(func):
            def wrap():
                print("=============================================================================")
                func()
                print("=============================================================================")
            return wrap()

        def decor(func):
            def wrap():
                print("==========================================")
                func()
                print("==========================================")
            return wrap()
        
        params_(mol_type)
        global data, cell, Time, data_, coordinates, atom_name, tri_m
        global xyz_, dataframe_, mass_, name_init, vel_all, force_all, keytrajec
        name_init = input_name

        t1 = list([])
        t2 = float()
        t3 = int()
        t4 = bool()
        t5 = str()
        t6 = dict()

        coordinates, mass, natom, charge, data  = params_control()

        [U_array, arr, atom_err,Time] = [[],[0],[],[]]

        keytrajec = keytrj

        if type(multi_treatment) != type(t4):
            @decor
            def print_error():
                print('TypeError 😊')
                print('multi_treatment a boolean type not any other type')
                print('multi_treatment ',type(t4))
                print('Put a boolean type and run again')
            exit()

        if multi_treatment == True:
            if input_name :
                if type(input_name) != type(t1):
                    @decor
                    def print_error():
                        print("TypeError 😊")
                        print("input_name is a list not any other type")
                        print('Put a list and run again')
                    exit()
                else:
                    for name_in in input_name:
                        if name_in[-7:] not in ['.LAMMPS', '.lammps']:
                            @decor
                            def print_error():
                                print("NameError 😊")
                                print('Bad value : ', name_in, 'from ', input_name)
                                print("Wrong input name. Try 'YourInputName.LAMMPS' or 'YourInputName.lammps")
                            exit()
            else:
                @decor
                def print_error():
                    print("InputError 😊")
                    print("name_init cannot be Empty")
                exit()
        else:
            if input_name:
                if type(input_name) != type(t5):
                    @decor
                    def print_error():
                        print("TypeError 😊")
                        print("input_name is a string")
                        print('Put a string and run again')
                    exit()
                else:
                    if input_name[-7:] not in ['.LAMMPS', '.lammps']:
                        @decor
                        def print_error():
                            print("NameError 😊")
                            print("Wrong input name. Try 'YourInputName.LAMMPS' or 'YourInputName.lammps")
                        exit()
            else:
                @decor
                def print_error():
                    print("InputError 😊")
                    print("input_name cannot be Empty")
                exit()

        if not nsit_M:
            @decor 
            def print_error():
                print('InputError 😊')
                print('nist_M cannot be Empty')
            exit()
        else:
            if type(nsit_M) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("nsit_M is a list not any other type")
                    print('nsit_M, ',type(t1))
                    print("Put nsit_M as list and try again")
                exit()
            else:
                for var in nsit_M:
                    if type(var) != type(t1):
                        @decor 
                        def print_error():
                            print('TypeError 😊')
                            print("The elements of nsit_M should be a list")
                            print(var, 'is not a', type(t1))
                        exit()
                    else:
                        for val in var:
                            if type(val) != type(t3): 
                                @decor 
                                def print_error():
                                    print('TypeError 😊')
                                    print("Problem with this list, ", var)
                                    print('All elements in the list above are not integers')
                                    print('bad value : ', val, 'correct that value and try again')
                                exit()
                            else:
                                if val < 0:
                                        @decor 
                                        def print_error():
                                            print('ValueError 😊')
                                            print("Problem with this list, ", var)
                                            print('All elements in the list above are not positive')
                                            print('bad value : ', val, 'correct that value and try again')
                                        exit()

        if not M_array:
            @decor 
            def print_error():
                print('InputError 😊')
                print('M_array cannot be Empty')
            exit()
        else:
            if type(M_array) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("M_array is a list not any other type")
                    print('M_array, ',type(t1))
                    print("Put M_array as list and try again")
                exit()
            else:
                for var in M_array:
                    if type(var) != type(t1):
                        @decor 
                        def print_error():
                            print('TypeError 😊')
                            print("The elements of M_array should be a list")
                            print(var, 'is not a', type(t1))
                        exit()
                    else:
                        for val in var:
                            if type(val) != type(t1): 
                                @decor 
                                def print_error():
                                    print('TypeError 😊')
                                    print("The sub elements of M_array should be a list")
                                    print(val, 'is not a', type(t1))
                                    print('Bad value : ', val, ' Correct that value and run again')
                                exit()
                            elif len(val) != 2:
                                @decor
                                def print_error():
                                    print('InputError')
                                    print('The Length of the sub elemnts of M_array are not the same' )
                                    print('The size of, ', val, 'is different from 2')
                                exit()
                            else:
                                for val1 in val:
                                    if type(val1) != type(t3):
                                        @decor
                                        def print_error():
                                            print('TypeError 😊')
                                            print("Problem with this list, ", val)
                                            print('All elements in the list above are not integers')
                                            print('bad value : ', val1, 'correct that value and try again')
                                        exit()
                                    else:
                                        if val1 < 0:
                                            @decor 
                                            def print_error():
                                                print('ValueError 😊')
                                                print("Problem with this list, ", val)
                                                print('All elements in the list above are not positive')
                                                print('bad value : ', val1, 'correct that value and try again')
                                            exit()
                  
        if not nmol:
            @decor 
            def print_error():
                print('InputError 😊')
                print('nmol cannot be Empty')
            exit()
        else:
            if type(nmol) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("nmol is a list not any other type")
                    print('nmol, ',type(t1))
                    print("Put nmol as list and try again")
                exit()   
            else:
                for i, val in enumerate(nmol):
                    if type(val) != type(t3):
                        @decor 
                        def print_error():
                            print('TypeError 😊')
                            print("The values in nmol should be integers")
                            print(type(t3))
                            print("Check your values and correct the bad values")
                            print('The bad found is :', val, 'index = ', i, 'from', nmol)
                        exit()
                    else:
                        if val <= 0:
                            @decor 
                            def print_error():
                                print('ValueError 😊')
                                print("The values in nmol should be bigger than 0")
                                print("Check your values and correct the bad values")
                                print('The bad found is :', val, 'index = ', i, 'from', nmol)
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
                    def print_eror():
                        print('ValueError 😊')
                        print('mol_type cannot be negative')
                    exit()

        if  not CELL:
            cell = np.array([[1., 0., 0.], [0., 1., 0.],[0., 0., 1.]])       
        else:
            if type(CELL) != type(t1):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print("CELL is a list not any other type")
                    print('CELL, ',type(t1))
                    print("Put a list as an input and try again")
                exit()
            else:
                cell = CELL

        if mass_atom:
            if type(mass_atom) != type(t6):
                @decor
                def print_error():
                    print('TypeError 😊')
                    print('mass_atom is a dictionary not any other type')
                    print('mass_atom', type(t6))
                    print('Put a dict as an input and try again')
                exit()
            else:
                mass_list = list(mass_atom.keys())
                for val in mass_list:
                    if type(mass_atom[val]) != type(t1):
                        @decor
                        def print_error():
                            print('TypeError 😊')
                            print('The items values of mass_atom should be a list with length 2')
                            print(dict(Bad_value = mass_atom[val], item = val))
                            print('Correct this mistake and run again')
                        exit() 
                    else:
                        if len(mass_atom[val]) != 2:
                            @decor
                            def print_error():
                                print('InputError 😊')
                                print(" The size if ", mass_atom[val], 'is different from 2')
                                print("Correct the mistake and try again")
                            exit()
                        else:
                            id1, id2  = mass_atom[val]
                            if type(id2) != type(t2):
                                @decor
                                def print_error():
                                    print('InputError 😊')
                                    print([id2], 'not in ', [type(t2)] )
                                    print("Correct the mistake and try again")
                                exit()
                            elif type(id1) != type(t3) :
                                @decor
                                def print_error():
                                    print('InputError 😊')
                                    print([id1], 'not in ', [type(t3)] )
                                    print("Correct the mistake and try again")
                                exit()
                            else:
                                if id1 < 0 or id2 < 0.:
                                    id0 = mass_list.index(val)
                                    @decor 
                                    def print_error():
                                        print('ValueError 😊')
                                        print("Problem with this dict, ", dict(val = mass_atom[val]), 'with val = {}'.format(val))
                                        print('The values of the items in this list below')
                                        print(mass_list, 'cannot be negative')
                                        print('Correct your mistakes try again')
                                    exit()
        else:
            @decor
            def print_error():
                print('InputError')
                print('mass_atom cannot be Empty')
            exit()

        if len(M_array) != len(nsit_M):
            @decor 
            def print_error():
                print('InputError 😊')
                print("M_array doesn't have the same Length with nsit_M ")
                print("Correct your mistake and run again")
            exit()

        if len(nsit_M) != mol_type or len(nmol) != mol_type:
            @decor
            def print_error():
                print("ValueError  😊")
                print("Length nsit or Length nmol not the same with mol_type")
                print('You should always have Length(nsit or nmol) = mol_type')
                print('Have a look on your inputs to see what happened, correct your mistake and try again')
            exit()

        if len(M_array) != len(nsit_M):
            @decor 
            def print_error():
                print('InputError 😊')
                print("M_array doesn't have the same Length with nsit_M ")
                print("Correct your mistake and run again")
            exit()
        
        if type(keytrj) != type(t3):
            @decor 
            def print_error():
                print('TypeError 😊')
                print('keytrj is an integer not any other type')
                print('keytrj, ', type(t3))
                print('Put an integer as an input and run again')
            exit()

        summ = 0
        
        for i in range(0, mol_type):
            summ = summ + np.sum(len(list(M_array[i])))

        summ = 0

        for i in range(0, mol_type):
                for j in range(0,nmol[i]):
                    for u in range(0,len(nsit_M[i])):
                        for k in range(0,nsit_M[i][u]):
                            if j == 0:
                                v = k + M_array[i][u][0] 
                            elif j >=1:
                                v = k + nsit_M[i][u] * j + M_array[i][u][0]
                            U_array.append(v) 
        
        MATRIX_MOL = np.array(list(U_array))

        sum_ = 0
        
        for i in range(0, mol_type):
            sum_ = sum_ + np.sum(nsit_M[i]) * nmol[i]
            arr.append(sum_)
        
        sum_ = 0
        
        # opening  input and reading input file to extract all informations
        # that will be using later by another programming code 
        # atomic extract process 

        file = open(input_name, "r")

        with alive_bar(trajec_num, title='Initialization') as bar:
            for t in range(0, trajec_num):
                error = []
                [alloc1, alloc2,columnX,columnY,columnZ] = [[],[],[],[],[]]

                item1 = file.readline().split (':')
                
                time = float(file.readline())
                
                item2 = file.readline().split (':')
                
                total_atom = int( file.readline() )

                item3 = file.readline().split (':')

                boxx = [float(gama) for gama in file.readline().split ()]
                boyy = [float(gama) for gama in file.readline().split ()]
                bozz = [float(gama) for gama in file.readline().split ()]

                cell_x1, cell_x2 = boxx 
                cell_y1, cell_y2 = boyy
                cell_z1, cell_z2 = bozz 

                cellx = cell_x2 - cell_x1
                celly = cell_y2 - cell_y1
                cellz = cell_z2 - cell_z1

                box_size = [[cellx, 0., 0.], [0., celly, 0.], [0., 0., cellz]]

                item4 = file.readline().split ()

                Time.append(float(time))

                for i in range(0, int(total_atom)):
                    firstline = file.readline().split () 
                    long = len(firstline)

                    if (long == 5 and keytrj != 0) or (long == 8 and keytrj != 1) or (long == 11 and keytrj != 2):
                        if long == 5:
                            true_keytrj = 0
                        elif long == 8:
                            true_keytrj = 1
                        elif long == 11:
                            true_keytrj = 2
                        @decor
                        def print_error():
                            print('ValueError 😊')
                            print('Bad keytrj value')
                            print('keytrj is ', keytrj, 'instead', true_keytrj)
                            print('Put the good value and run again')
                            info = """ 
                - keytrj = 0 means only positions
                - keytrj = 1 means positions + velocities 
                - keytrj = 2 means positions + velocities + forces\n"""
                            print(info)
                        exit()

                    if keytrj == 0:
                        id_atom, type_atom, posx, posy, posz = firstline

                    elif keytrj == 1:
                        id_atom, type_atom, posx, posy, posz, vx, vy, vz = firstline
                    
                    elif keytrj == 2:
                        id_atom, type_atom, posx, posy, posz, vx, vy, vz, fx, fy, fz = firstline
                    
                    else:
                        @decor
                        def print_error():
                            print('ValueError 😊')
                            print(" Bad keytrj value")
                            info = """ 
                - keytrj = 0 means only positions
                - keytrj = 1 means positions + velocities 
                - keytrj = 2 means positions + velocities + forces\n"""
                            print(info)
                            print("Check your value and try again")
                        exit()

                    id_atom, type_atom = int( id_atom ), int( type_atom )
                    ntm = list(mass_atom.keys())[type_atom-1]

                    if type_atom == mass_atom[ntm][0] :
                        masses = float (mass_atom[ntm][1]) 
                    
                    else:
                        error.append([ ['id_lamps, type_lammps, atom', [id_atom, type_atom, ntm]], ['type_set, atom', [mass_atom[ntm][0], ntm]] ])
                        @decor1
                        def print_error():
                            print('ValueError 😊')
                            print('The problem comes from mass_atom')
                            print('The type_lammps is different from type_set, see the error below')
                            print('Change the bad value and run again\n')
                            print(error)
                        exit()

                    if keytrj == 0:
                        alloc1.append([str(ntm), float(posx), float(posy), float(posz), float(masses)])
                        columns = ['atom name', 'X', 'Y', 'Z', 'mass']
                    
                    elif keytrj == 1:
                        alloc1.append([str(ntm), float(posx), float(posy), float(posz), float(vx), float(vy), float(vz), float(masses)])
                        columns = ['atom name', 'X', 'Y', 'Z', 'VX', 'VY', 'VZ', 'mass']

                    elif keytrj == 2:
                        alloc1.append([str(ntm), float(posx), float(posy), float(posz), float(vx), float(vy), float(vz), float(fx), float(fy), float(fz), float(masses)])
                        columns = ['atom name', 'X', 'Y', 'Z', 'VX', 'VY', 'VZ', 'FX', 'FY', 'FZ','mass']

                    alloc2.append(masses)

                df = pd.DataFrame(alloc1, columns = columns)

                M_2D_array = df.values 
                M_2D_array = M_2D_array[MATRIX_MOL, ]
                
                for j in range(0, mol_type):
                    if mol_type > 1:
                        for val1 in M_2D_array[arr[j]:arr[j+1], :]:
                            coordinates[j].append(val1)
                    elif mol_type == 1:
                        for val1 in M_2D_array[0:arr[1], :]:
                            coordinates[j].append(val1)
                    else:
                        @decor
                        def print_error():
                            print('ErrorValue')
                            print('mol_type not in [1, ->[')
                            print("Put the correct value and try again")
                        exit()

                sleep(.001)
                bar() 

        for i in range(0,mol_type):
            if keytrj == 0: 
                columns = ['atom name', 'X', 'Y', 'Z', 'mass']
            elif keytrj == 1:
                columns = ['atom name', 'X', 'Y', 'Z', 'VX', 'VY', 'VZ', 'mass']
            elif keytrj == 2:
                columns = ['atom name', 'X', 'Y', 'Z', 'VX', 'VY', 'VZ', 'FX', 'FY', 'FZ','mass']

            data[i] = pd.DataFrame(coordinates[i], columns=columns)
            #data[i].set_index('atom name', inplace=True) #reset index for all data frame
        
        if CELL == None:
            cell = box_size 
        else:
            cell = CELL

        data_ = {'Molecule data' : data, 'box size' : cell, 'time simulation' : Time}

        xyz_, dataframe_, mass_ = params_gdr()
    
        vel_all, force_all = [],[]
        atom_name = []

        for i in range(0, len(xyz_)):
            dataframe_[i] = data[i]
            xyz_[i] = dataframe_[i].iloc[:, [1,2,3]].values 
            atom_name.append(dataframe_[i].iloc[:, 0])

            if keytrj == 0:
                mass_[i] = dataframe_[i].iloc[:, 4:5]

            if keytrj == 1:
                vel_all.append(np.array( dataframe_[i].iloc[:, 4:7], dtype = dtype ))
                mass_[i] = dataframe_[i].iloc[:, 7:8]
                
            if keytrj == 2:
                vel_all.append(np.array( dataframe_[i].iloc[:, 4:7], dtype = dtype ))
                force_all.append(np.array( dataframe_[i].iloc[:, 7:10], dtype = dtype ))
                mass_[i] = dataframe_[i].iloc[:, 11:12]
                
            
            mass_[i] = np.array(mass_[i], dtype = dtype)
        
        for i in range(0, len(xyz_)):
            atom_name[i] = np.array(atom_name[i])

        # returning the Final result as a data.frame for more clarity

        return data_
    
    def Info(self):
        return data_.keys()
    
    def Box_2DArray(self):
        return cell 
    
    def Data(self):
        return data 
    
    def XYZ_2DArray(self):
        return xyz_ 
    
    def Mass_2Darray(self):
        def decor(func):
            def wrap():
                print("==========================================")
                func()
                print("==========================================")
            return wrap()

        if name_init[-7:] in ['.lammps', '.LAMMPS'] or name_init[-5:] in ['.HIST', '.hist'] or name_init[-4:] in ['.XYZ', '.xyz']:     	
            return mass_
        
        else:
            @decor
            def print_error():
                print('ErrorName 😊')
                print('Impossible to show Mass_2Darray')
                print('It only works for the HISTORY or TRAJEC.xyz or LAMMPS Files')
                print('Have a look on your input, change the name and try again')
            exit()
    
    def Atom_Names_2Darray(slef, encoding : any  = False, n_type : dict = dict(),
    label_encoder : dict = None):
        
        """
        You can use this function to get the names of all atoms in yours molecular system. 
        It's very useful to make encoding by activating the keyword << encoding >> on True,
        then use the label_encoder to specify how would you like to do this. 
        
        >>> WARNING: if you want to compute the ElectronDensity or ElectronDensityNeutral the encoding 
        characters should be identical with the elements of the periodic table, else if the code could not run. 
     
        It means that, if in your molecular system the carbons are [CR, C1, CW] when you're doing the encoding, all these values become [C]
        because as i wrote before, [CR, C1, CW] should take the same value [C] as in the priodic table.

        Else if you can make it like you want.

        >>>>>>>>>>>>>>>>>>>>> INPUTS EXAMPLES AND DETAILS >>>>>>>>>>>>>>>>>>>>>>>>>>
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        >>> label_encoder = dict(C= ['CR','CW','CR','C1', 'CE'], H=['HCR','HCW','HC','H1'],Na=['NA'], B=['B'], F=['FB'], Mo=['Mo'],S=['S'])

        the keyword label_encoder is a dict see the example above we can convert all atoms in the lists by the items values 
        for example in our system the carbons are identified by 'CR' and 'CW' so, when you use label_encoder both values become 'C' 
        same for the Hydrogens and the others.

        """
        def decor(funct):
            def wrap():
                print("=====================================")
                funct()
                print("=====================================")
            return wrap()

        t1 = dict()
        t2 = bool()

        if encoding == False:
            return atom_name
        elif encoding == True:
            if label_encoder:
                if type(label_encoder) != type(t1):
                    @decor
                    def print_error():
                        print('TypeError 😊')
                        print('label_encoder should be a dictionary')
                        print('label_encoder :', (type(label_encoder)))
                    exit()

                encoding_list = list(label_encoder.keys())
                N = len(encoding_list)
                na = []

                if N == 1:
                    complet_list=label_encoder [encoding_list[0]]
                    for k in range(0, len(label_encoder [encoding_list[0]])):
                        na.append(encoding_list[0])

                elif N > 1:
                    complet_list=label_encoder [encoding_list[0]]
                    for k in range(0, len(label_encoder [encoding_list[0]])):
                        na.append(encoding_list[0])

                    for j in range(1, N):
                        complet_list = complet_list + label_encoder [encoding_list[j]]
                        for k in range(0, len(label_encoder [encoding_list[j]])):
                            na.append(encoding_list[j])

                bad_name = []
                with alive_bar(len(atom_name), title='Encoding Names') as bar:
                    for i in range(0, len(atom_name)):
                        for t in range(0, atom_name[i].shape[0]):
                            
                            if atom_name[i][t] in complet_list:
                                a = complet_list.index(atom_name[i][t])
                                atom_name[i][t] = na[a]
                            elif atom_name[i][t] not in complet_list:
                                bad_name.append(atom_name[i][t])
                                @decor
                                def print_error():
                                    print('ErrorName 😊')
                                    print('atom name', bad_name ,'not in the list below')
                                    print(complet_list)
                                    print('Change the bad value and try again')
                                exit()

                        sleep(0.001)
                        bar()

                return atom_name
            
            else:
                @decor
                def print_error():
                    print("InputError 😊")
                    print("label_encoder cannot be Empty")
                exit()
        else:
            @decor
            def print_error():
                print("TypeError 😊")
                print("encoding is a boolean type")
                print('encoding, ', type(t2))
                print('Correct your mistake and run again')
            exit()            

    def TimeSimulation(self, timestep : float = 1e-3, tri : any = False, step : int = None):
        """
        Get time simulation by using this function. 
        It takes three arguments as inputs 

        timestep: 
        Identical with the timestep used for your simulations 
        
        tri     : 
        Is a boolean type, generally use to make a selection of trajectories 
        
        step    : 
        Is an integer, it specifies the range between two timesteps when the keyword <<tri>> is defined on <True>>

        The default value of the timestep is :
        
        >>> timestep = 1e-3

        """
        global Time

        def decor(funct):
            def wrap():
                print("=================================")
                funct()
                print("=================================")
            return wrap()

        t1 = float()
        t2 = bool()
        t3 = int()

        if type(step) != type(t3):
            @decor
            def print_error():
                print('ErrorType')
                print('step is an integer not any other type')
                print('step, ', type(t3))
            exit()

        if type(timestep) != type(t1):
            @decor
            def print_error():
                print('ErrorType')
                print('timestep is a boolean not any other type')
                print('timestep, ', type(t3))
            exit()

        if tri == False:
            h = np.abs(Time[1] - Time[0]) * timestep
            x = 0
            new_time = []
            i = 0
            with alive_bar(len(Time), title='time Init') as bar:
                while i < len(Time):
                    x = x + h
                    new_time.append(x)
                    i +=1
                    sleep(0.001)
                    bar()

        elif tri == True:
            if step: 
                
                liste = [int(x) for x in range(0, len(Time), step)]
                liste = np.array(liste)
                
                Time = np.array(Time)

                time_n = Time[liste, ]

                h = np.abs(time_n[1] - time_n[0]) * timestep
                x = 0
                new_time = []
                i = 0

                with alive_bar(time_n.shape[0], title='time Init') as bar:
                    while i < time_n.shape[0]:
                        x = x + h
                        new_time.append(x)
                        i +=1

                        sleep(0.001)
                        bar()
            
            else:
                @decor
                def print_error():
                    print('InputError 😊')
                    print('tri is defined on True but step is empty')
                    print('Check your values and run again')
                exit()
        
        else:
            @decor
            def print_error():
                print('TypeError 😊')
                print('tri is a boolean type')
                print('tri, ', type(t2))
            exit()
  
        return np.array(new_time)

    def Charge_2Darray(self):
        def decor(func):
            def wrap():
                print("==========================================")
                func()
                print("==========================================")
            return wrap()

        if name_init[-5:] in  ['.HIST', '.hist']:
            return charge

        else:
            @decor
            def print_error():
                print('ErrorName 😊')
                print('Impossible to show charge_2Darray')
                print('It only works for the HISTORY Files')
                print('Have a look on your Input name and try again')
            exit()

    def Velocities_2Darray(self, keytrj : int = 1):
        def decor(func):
            def wrap():
                print("==========================================")
                func()
                print("==========================================")
            return wrap()

        t3 = int()

        if type(keytrj) != type(t3):
            @decor 
            def print_error():
                print('TypeError 😊')
                print('keytrj is an integer not any other type')
                print('keytrj, ', type(t3))
                print('Put an integer as an input and run again')
            exit()

        if name_init[-5:] in  ['.HIST', '.hist']:
            if keytrj in [1, 2]:
                return vel
            else:
                @decor
                def print_error():
                    print('InputError 😊')
                    print('Impossible to print volocities')
                    print('Check your keyword keytrj and try again')
                exit()
        elif name_init[-7:] in ['.LAMMPS', '.lammps']:
            if keytrj in [1, 2]:
                return vel_all
            else:
                @decor
                def print_error():
                    print('InputError 😊')
                    print('Impossible to print volocities')
                    print('Check your keyword keytrj and try again')
                exit()
        else:
            @decor
            def print_error():
                print('NameError 😊')
                print('It only works for HISTOTY or Lammps files')
            exit()
                    
    def Forces_2Darray(self, keytrj : int = 2):
        def decor(func):
            def wrap():
                print("==========================================")
                func()
                print("==========================================")
            return wrap()
        
        t3 = int()

        if type(keytrj) != type(t3):
            @decor 
            def print_error():
                print('TypeError 😊')
                print('keytrj is an integer not any other type')
                print('keytrj, ', type(t3))
                print('Put an integer as an input and run again')
            exit()

        if name_init[-5:] in  ['.HIST', '.hist']:
            if keytrj == 2:
                return forces
            else:
                @decor
                def print_error():
                    print('InputError  😊')
                    print('Impossible to print forces')
                    print('Check your keyword keytrj and try again')
                exit()
        elif name_init[-7:] in ['.LAMMPS', '.lammps']:
            if keytrj == 2:
                return force_all
            else:
                @decor
                def print_error():
                    print('InputError  😊')
                    print('Impossible to print forces')
                    print('Check your keyword keytrj and try again')
                exit()
        else:
            @decor
            def print_error():
                print('NameError 😊')
                print('It only works for HISTOTY or Lammps files')
            exit()