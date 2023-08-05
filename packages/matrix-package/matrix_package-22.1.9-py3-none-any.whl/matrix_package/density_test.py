import numpy as np
import pandas as pd 
from matrix_package.bin import Bin
from matrix_package.pbc import Periodic_BC, Volume
from time import sleep 
from alive_progress import alive_bar 
import multiprocessing as mp


class Density:

    def Density_profile(self, mol_type = None, nmol = None, trajec_num = None, XYZ = None, 
    max_float = 5, atom_index = list, mol_select = None, start = 0, end = None,  _dir_ = 'Z', imcon = None, nsit = None,
    z_first_layer = None, delta = 0.0, CELL = None, r_step = 0.1, replicated_layer = False, limit_box = 0., charge = None,
    scaler = None, Normalize = False, Name_cal = 'AtomicDensity', atoms_name = None, rho_0 = 1.2803):
        
        global density_final, index_density_com
        
        bn = Bin()

        t1 = list([])
        t2 = float()
        t3 = int()
        t4 = bool()
        t5 = str()

        def decor(func):
            def wrap():
                print("=======================================================")
                func()
                print("=======================================================")
            return wrap()

        if not trajec_num:
            @decor 
            def print_error():
                print('ErrorInput 😊')
                print('trajec_num connot be Empty')
            exit()
        else:
            if type(trajec_num) != type(t3):
                @decor 
                def print_error():
                    print('ErrorType 😊')
                    print('trajec_num is an integer not any other type')
                exit()

        if not mol_type:
            @decor 
            def print_error():
                print('ErrorInput 😊')
                print("mol_type is Empty")
            exit() 
        else:
            if type(mol_type) != type(t3):
                @decor 
                def print_error():
                    print('ErrorType 😊')
                    print("mol_type is an integer not any other type")
                    print("Put mol_type as an integer and try again")
                exit()

        if not nmol:
            @decor 
            def print_error():
                print('ErrorInput 😊')
                print('nmol cannot be Empty')
            exit()
        else:
            if type(nmol) != type(t1):
                @decor 
                def print_error():
                    print('ErrorType 😊')
                    print("nmol is a list not any other type")
                    print("Put nmol as list and try again")
                exit()   
            else:
                for i, val in enumerate(nmol):
                    if type(val) != type(3):
                        @decor 
                        def print_error():
                            print('ErrorType 😊')
                            print("The values in nmol should be the integers")
                            print("Check your values and correct the bad values")
                            print('The bad found is :', val, 'index = ', i, 'from', nmol)
                        exit()
                    else:
                        if val == 0:
                            @decor 
                            def print_error():
                                print('ErrorValue 😊')
                                print("The values in nmol should be bigger than 0")
                                print("Check your values and correct the bad values")
                                print('The bad found is :', val, 'index = ', i, 'from', nmol)
                            exit()  

        if not nsit:
            @decor 
            def print_error():
                print('ErrorInput 😊')
                print('nsit cannot be Empty')
            exit()
        else:
            if type(nsit) != type(t1):
                @decor 
                def print_error():
                    print('ErrorType 😊')
                    print("nsit is a list not any other type")
                    print("Put nmol as list and try again")
                exit()   
            else:
                for i, val in enumerate(nsit):
                    if type(val) != type(3):
                        @decor 
                        def print_error():
                            print('ErrorType 😊')
                            print("The values in nsit should be the integers")
                            print("Check your values and correct the bad values")
                            print('The bad found is :', val, 'index = ', i, 'from', nsit)
                        exit()
                    else:
                        if val == 0:
                            @decor 
                            def print_error():
                                print('ErrorValue 😊')
                                print("The values in nsit should be bigger than 0")
                                print("Check your values and correct the bad values")
                                print('The bad found is :', val, 'index = ', i, 'from', nmol)
                            exit()

        if start:
            if start < 0 :
                @decor 
                def print_error():
                    print('ErrorValue 😊')
                    print('start cannot be lower than 0 ')
                exit()
            else: 
                if type(start) != type(t3):
                    @decor 
                    def print_error():
                        print('ErrorType 😊')
                        print('start is an integer not any other type')
                    exit()
                else:
                    begin = start
        else:
            begin = int(0.)
        
        if end:
            if end > trajec_num:
                @decor 
                def print_error():
                    print('ErrorValue 😊')
                    print('end cannot be bigger than trajec_num') 
                    print('Put another value')
                exit()
            else: 
                if type(end) != type(t3):
                    @decor 
                    def print_error():
                        print('ErrorType 😊')
                        print('end is an integer not any other type')
                    exit()
                else:
                    endding = end
        else:
            endding = int(trajec_num)

        if end and start:    
            if start >= end :
                @decor 
                def print_error():
                    print('ErrorValue 😊')
                    print('start should be lower than end')
                    print('Check your input and try again')
                exit()
        
        end = endding 
        start = begin

        if not mol_select:
            index_density_com = [int(x) for x in range(0, mol_type)]      
        else:
            if type(mol_select) != type(t1):
                @decor 
                def print_error():
                    print('ErrorType 😊')
                    print('mol_select is a list not any other type')
                    print('Change your input and try again')
                exit() 
            else:
                for i, val in enumerate(mol_select):
                    if type(val) != type(t3):
                        @decor 
                        def print_error():
                            print('ErrorType 😊')
                            print('The values in mol_select should be the integers')
                            print("Check your values and correct the bad values")
                            print('The bad found is :', val, 'index = ', i, 'from', mol_select)
                        exit()
                    else:
                        index_density_com = mol_select

        if not z_first_layer :
            @decor
            def print_error():
                print('ErrorInput 😊')
                print("z_first_layer cannot be Empty or NULL")
        else:
            if type(z_first_layer) == type(t1):
                if len(z_first_layer) != 2:
                    @decor
                    def print_error():
                        print('ErrorValue 😊')
                        print("z_first_layer is a list with a length 2")
                        print('[a, b]')
                        info = """ where 'a' is first or second layer and 'b' the number of atoms 
                        does the layer 'a' has """
                        print(info)
                        print('check your inputs and try again')
                    exit()
            elif type(z_first_layer) == type(t2):
                if z_first_layer < 0.: 
                    @decor
                    def print_error():
                        print('ErrorValue 😊')
                        print("z_first_layer cannot be negative")
                    exit()
            elif type(z_first_layer) not in [type(t1), type(t2)]:
                @decor
                def print_error():
                    print('ErrorType 😊')
                    print("z_first_layer type not in", [type(t1), type(t2)])
                exit()

        if not XYZ:
            @decor
            def print_error():
                print('ErrorInput 😊')
                print("XYZ cannot be Empty")
            exit()          
        else:
            if type(XYZ) != type(t1):
                @decor 
                def print_error():
                    print('ErrorType 😊')
                    print("XYZ is a list not any other type")
                    print("Put a list as an input and try again")
                exit() 

        if  CELL == None:
            @decor
            def print_error():
                print('ErrorInput 😊')
                print("CELL cannot be Empty")
            exit()    
        else:
            if type(CELL) != type(t1):
                @decor 
                def print_error():
                    print('ErrorType 😊')
                    print("CELL is a list not any other type")
                    print("Put a list as an input and try again")
                exit()

        if not charge:
            @decor
            def print_error():
                print('ErrorInput 😊')
                print("charge cannot be Empty")
            exit()       
        else:
            if type(charge) != type(t1):
                @decor 
                def print_error():
                    print('ErrorType 😊')
                    print("charge is a list not any other type")
                    print("Put a list as an input and try again")
                exit()
        
        if not imcon:
            imcon = 1
            @decor 
            def print_error():
                print('imcon is Empty the default value is 1 ')
                print('for cubic sytems')
        else:
            if type(imcon) != type(t3):
                @decor 
                def print_error():
                    print('ErrorType 😊')
                    print('imcon is an integer not any other type')
                    print('Put imcon as an integer and run again')
                exit()

            imcon_list = [int(x) for x in range(1, 7)]
            if imcon not in  imcon_list:
                @decor 
                def print_error():
                    print('ErrorValue 😊')
                    print('imcon not in the list below')
                    print(imcon_list) 
                    print('change your input and run again')
                exit()

        if rho_0:
            if type(rho_0) != type(t2):
                @decor 
                def print_error():
                    print('ErrorType 😊')
                    print('rho_0 if a float not any other type')
                    print('Put rho_0 as a float and run again')
                exit()
            else:
                if rho_0 < 0.0:
                    @decor 
                    def print_error():
                        print('ErrorValue 😊')
                        print('rho_0 cannot be negative')
                    exit()

        Z_atom = dict(

            H=1,He=2,Li=3,Be=4,B=5,C=6,N=7,O=8,F=9,Ne=10,Na=11,Mg=12,Al=13,Si=14,P=15,S=16,Cl=17,Ar=18,
            K=19,Ca=20,Sc=21,Ti=22,V=23,Cr=24,Mn=25,Fe=26,Co=27,Ni=28,Cu=29,Zn=30,Ga=31,Ge=32,As=33,Se=34,Br=35,Kr=36,
            Rb=37,Sr=38,Y=39,Zr=40,Nb=41,Mo=42,Tc=43,Ru=44,Rh=45,Pd=46,Ag=47,Cd=48,In=49,Sn=50,Sb=51,Te=52,I=53,Xe=54,
            Cs=55,Ba=56,Lu=71,Hf=72,Ta=73,W=74,Re=75,Os=76,Ir=77,Pt=78,Au=79,Hg=80,Tl=81,Pb=82,Bi=83,Po=84,At=85,Rn=86,
            Fr=87,Ra=88,Lr=103,Rf=104,Db=105,Sg=106,Bh=107,Hs=108,Mt=109,Ds=110,Rg=111,Cn=112,Nh=113,Fl=114,Mc=115,Lv=116,Ts=117,Og=118,
            La=57,Ce=58,Pr=59,Nd=60,Pm=61,Sm=62,Eu=63,Gd=64,Tb=65,Dy=66,Ho=67,Er=68,Tm=69,Yb=70,
            Ac=89,Th=90,Pa=91,U=92,Np=93,Pu=94,Am=95,Cm=96,Bk=97,Cf=98,Es=99,Fm=100,Md=101,No=102
        )

        periodic_tab = list ( Z_atom.keys() )
        
        [h_bin, rmax] = bn.bin_interface(ind = z_first_layer, dr = r_step, CELL = CELL, delta = delta, 
        _dir_ = _dir_, double=replicated_layer, h_max=limit_box, XYZ = XYZ, trajec_num = trajec_num)

        charge_density = [[],[]]
        total_trajec = end - start
        boxx, boxy, boxz = CELL

        volume = Volume(CELL=CELL, imcon=imcon)

        with alive_bar(total_trajec * len(index_density_com), title=Name_cal) as bar:
            def lolo(i):
                for t in range(start, end):
                    for i in index_density_com:  
                        for j in range(0, nmol[i]):
                            data = []
                            for k in range(0, nsit[i]):
                                x, y, z = XYZ[i][t, j, k, 0:3]

                                if _dir_ == 'Z':
                                    cm_xyz = z 
                                
                                elif _dir_ == 'Y':
                                    cm_xyz = y 
                                
                                elif _dir_ == 'X':
                                    cm_xyz = x
                                
                                else:
                                    @decor
                                    def print_error():
                                        print('error 😊')
                                        print("_dir_ takes three values : ['X', 'Y', 'Z']")
                                        print('change the value and try again')
                                    exit()
                                
                                if type(z_first_layer) == type(t1):
                                    dis = []
                                    
                                    for p in range(0, z_first_layer[1]):
                                        x_l, y_l, z_l = XYZ[z_first_layer[0]][t, 0, p, 0:3]
                                        dis_z =  cm_xyz - z_l #z_first_layer
                                        dis.append(dis_z)
                                    dz = np.mean(dis)

                                elif type(z_first_layer) == type(t2):
                                    dz = cm_xyz - z_first_layer

                                if dz < rmax[t]:
                                    if Name_cal in ['AtomicDensity', 'MolecularDensity', 'ChargeDensity']:
                                        alpha = [ charge[i][t, j, k] if (dz >= h_bin[h]) and (dz < h_bin[h+1]) else 0.0 for h in range(0, len(h_bin)-1)]
                                        data.append( alpha )
                                    
                                    elif Name_cal == 'ElectronDensity':
                                        if atoms_name == None:
                                            @decor
                                            def print_error():
                                                print('Error')
                                                print('atoms_name cannot be empty or NULL')
                                                print("Put the correct values and try again")
                                            exit()

                                        if atoms_name[i][t, j, k] in periodic_tab:

                                            alpha = [ (Z_atom[atoms_name[i][t, j, k]] - charge[i][t, j, k]) if (dz >= h_bin[h]) and (dz < h_bin[h+1]) else 0.0 for h in range(0, len(h_bin)-1)]
                                            data.append( alpha)

                                        elif atoms_name[i][t, j, k] not in periodic_tab:
                                            @decor
                                            def print_error():
                                                print('NameError')
                                                print(atoms_name[i][t, j, k], 'not in the list below')
                                                print(periodic_tab)
                                            exit()
                                    
                                    elif Name_cal == 'ElectronDensityNeutral':
                                        if atoms_name == None:
                                            @decor
                                            def print_error():
                                                print('Error')
                                                print('atoms_name cannot be empty or NULL')
                                                print("Put the correct values and try again")
                                            exit()

                                        if atoms_name[i][t, j, k] in periodic_tab:
                                            alpha = [ Z_atom[atoms_name[i][t, j, k]] if (dz >= h_bin[h]) and (dz < h_bin[h+1]) else 0.0 for h in range(0, len(h_bin)-1)]
                                            data.append( alpha)

                                        elif atoms_name[i][t, j, k] not in periodic_tab:
                                            @decor
                                            def print_error():
                                                print('NameError')
                                                print(atoms_name[i][t, j, k], 'not in the list below')
                                                print(periodic_tab)
                                            exit()
                                    
                                    else:
                                        @decor
                                        def print_error():
                                            print('Error 😊')
                                            print('Name_cal not in the list below')
                                            print('[ElectronDensity, ChargeDensity, AtomicDensity, MolecularDensity, ElectronDensityNeutral]')
                                            print('Change your value and try again')
                                            info = """
                                            * ChargeDensity = Q / Volume
                                            * AtomiqueDensity = Ma / Volume
                                            * MolecularDensity = N / Volume
                                            * ElectronDensity = (Z - Q) / Volume
                                            * ElectronDensityNeutral = Z / Volume
                                            
                                            where 

                                            * Q is the partial charge
                                            * N the Number 
                                            * Ma is the atomic mass 
                                            * Z is the atomic number 

                                            """
                                            print(info)
                                        exit()
                                    
                                    charge_density[i].append(np.array(alpha, dtype=np.float32))

                        sleep(0.001)
                        bar()

            pool = mp.Pool(mp.cpu_count())
            pool.map(lolo, [i for i in index_density_com])
            pool.close()

            allocate = []

            for i in  index_density_com:
                summ = 0.
                
                for k in range(0, nsit[i]):
                    if Name_cal in ['AtomicDensity', 'MolecularDensity', 'ChargeDensity']:
                        summ = summ + charge[i][0, 0, k]
                    
                    elif Name_cal == 'ElectronDensity':
                        summ = summ + (Z_atom[atoms_name[i][0, 0, k]] - charge[i][0, 0, k])
                    
                    elif Name_cal == 'ElectronDensityNeutral':
                        summ = summ + Z_atom[atoms_name[i][0, 0, k]] 

                allocate.append(summ)

            summ = 0.
            for i in index_density_com:
                charge_density[i] = np.array(charge_density[i], dtype=np.float32)

                charge_density[i] = charge_density[i].sum( axis = 0)
                
                for h in range(0, len(h_bin)-1):
                    if imcon in [1, 2, 3, 4, 5, 6]:
                        if _dir_ == 'X':    
                            vol = (h_bin[h+1] - h_bin[h]) * boxy[1] * boxz[2]
                            r_z = boxx[0]

                        elif _dir_ == 'Y':
                            vol = (h_bin[h+1] - h_bin[h]) * boxx[0] * boxz[2]
                            r_z = boxy[1]

                        elif _dir_ == 'Z':
                            vol = (h_bin[h+1] - h_bin[h]) * boxx[0] * boxy[1]
                            r_z = boxz[2]
                    
                    else:
                        @decor
                        def print_error():
                            print('error 😊')
                            print('imcon not in [1,2,3,4]')
                            print('change the value and try again')
                            print("===========================================")
                        exit()

                    if Name_cal == 'ChargeDensity':
                        charge_density[i][h] = (charge_density[i][h] * 1000. ) / (vol * total_trajec) 
                        
                    elif Name_cal == 'AtomicDensity':
                        charge_density[i][h] = charge_density[i][h] / (vol * total_trajec )
                        charge_density[i][h] = charge_density[i][h] * (10. / 6.023)

                    elif Name_cal == 'MolecularDensity' :
                        charge_density[i][h] = charge_density[i][h] / (vol * total_trajec )
                        charge_density[i][h] = charge_density[i][h] * (10. / 6.023)
                        
                        charge_density[i][h] = charge_density[i][h] * ((6.023 * 1e+2) /  allocate[i])

                    elif Name_cal == 'ElectronDensity':
                        charge_density[i][h] = (charge_density[i][h] * 1000. ) / (vol * total_trajec)

                    elif Name_cal == 'ElectronDensityNeutral':
                        charge_density[i][h] = (charge_density[i][h] * 1000. ) / (vol * total_trajec)
                    
                charge_density[i].round(max_float)

            if Name_cal in ['AtomicDensity', 'MolecularDensity']:
                
                total_m = np.sum(allocate)

                for i in  index_density_com:
                
                    rho = rho_0 * ((allocate[i]) / (total_m))
                    rho_d_0 = rho * ((6.023 * 1e+2 ) / allocate[i])

                    if Normalize == True:

                        if Name_cal == 'MolecularDensity':
                            charge_density[i] = charge_density[i] / rho_d_0
                        
                        elif Name_cal == 'AtomicDensity':
                            charge_density[i] = charge_density[i] / rho
                    
                    else:
                        charge_density[i] = charge_density[i]

            elif Name_cal == 'ChargeDensity':
                for i in  index_density_com:

                    chg = ( np.abs(allocate[i]) * nmol[i] * 1000. ) / volume
                    
                    if Normalize == True:
                        charge_density[i] = charge_density[i]  / chg 
                    
                    else:
                        charge_density[i] = charge_density[i]
            
            elif Name_cal == 'ElectronDensity':
                for i in  index_density_com:
                
                    electron = (allocate[i] * nmol[i] * 1000.) / volume
                    
                    if Normalize == True:
                        charge_density[i] = charge_density[i] / electron
                    
                    else:
                        charge_density[i] = charge_density[i]
            
            elif Name_cal == 'ElectronDensityNeutral':
                for i in  index_density_com:
                
                    electron = (allocate[i] * nmol[i] * 1000.) / volume
                    
                    if Normalize == True:
                        charge_density[i] = charge_density[i] / electron
                    
                    else:
                        charge_density[i] = charge_density[i]
            
            summ = 0.

            for h in range(0, len(h_bin)-1):
                
                if scaler == 'StdScaler':
                    h_bin[h] = ( h_bin[h] - np.mean(h_bin[h]) ) / ( np.std(h_bin) )
                
                elif scaler == 'MinMaxScaler':
                    h_bin[h] = ( h_bin[h] - np.max(h_bin) ) / ( np.max(h_bin) - np.min(h_bin) ) 
                
                elif scaler == 'OrdinalScaler':
                    h_bin[h] = ( h_bin[h] - ( np.max(h_bin) + np.min(h_bin) ) * 0.5 ) / ( np.max(h_bin) - np.min(h_bin) )
                
                elif scaler == 'MedianScaler':
                    h_bin[h] = ( h_bin[h] - ( r_z * 0.5) ) 
                    
                elif scaler in ['IdentityScaler', None]:
                    h_bin[h] = h_bin[h]
                
                else:
                    @decor
                    def print_error():
                        print('error 😊')
                        print('Bad scaler value')
                        print("scaler not in the list below ")
                        print("[StdScaler, MinMaxScaler, OrdinalScaler, MedianScaler, IndentityScaler, None]" )
                        info = """

                        * StdScaler = ( zi - mean(z) ) / std(z)
                        * MinMaxScaler = ( zi - max(z) ) / ( max(z) - min(z) ) 
                        * OrdinalScaler = ( zi - ( max(z) + min(z) ) * 0.5 ) / ( max(z) - min(z) )
                        * MedianScaler = ( zi - boax_z * 0.5 )
                        * IdentityScaler = None = any change here, the box conserve his initial properties

                        Where zi are the values of the positions along z-axis, inversely (yi for y-axiz  and xi for x-axis )

                        """

                        print(info)
                    exit()
                
                if Name_cal in ['AtomicDensity', 'MolecularDensity', 'ChargeDensity','ElectronDensity','ElectronDensityNeutral']:
                    h_bin[h] = h_bin[h] / float(10.) 

            np.round(h_bin, max_float)

            density_final = dict( distance =  np.array(h_bin[0:len(h_bin)-1]), density1 =  charge_density[0], density2 = charge_density[1])
            
        return density_final

    def Integral_Density(self, data = 'EMIMBF_50d', defects = True):

        global density_final 

        if not data:
            names =  list(density_final.keys())

            data_f = pd.DataFrame(density_final) 
            data_f['total'] = (data_f.iloc[:, 1] + data_f.iloc[:, 2]) / 2.0

            z_value = data_f.iloc[:, 0]
            values = data_f.iloc[:, 3] 
            density1 = data_f.iloc[:, 1]
            density2 = data_f.iloc[:, 2]

        if data:
            file = open(data, 'r')
            lines = []
            for line in file.readlines():
                lines.append(line)
            file.close
            num = len(lines) 
            
            file = open(data, 'r')
            matrix = []
            for i in range(0, num-10):
                r1, d1, d2 = [np.round(float(x),5) for x in file.readline().split()]
                matrix.append([r1, d1, d2])

            matrix = np.array(matrix).round(5)
            data_f = pd.DataFrame(matrix, columns=['distance', 'density1', 'density2'])
            data_f['total'] = (data_f['density1'] + data_f['density2'])/2.0

            z_value = np.round(data_f.iloc[:, 0],5)
            values = np.round(data_f.iloc[:, 3],5)
            density1 = np.round(data_f.iloc[:, 1],5)
            density2 = np.round(data_f.iloc[:, 2],5)

            file.close()

        max_value1 = np.round(np.max(values),5) 
        for i, val in enumerate(values):
            if val == max_value1:
                index_max1 = i

        l1 = int(len(lines) / 3.)
        data1 = []
        for val in values[index_max1:l1]:
            if val != 0.:
                data1.append(val)

       
        max_value2 = np.round(np.min(data1), 5) 

        for i, val in enumerate(values):
            if val == max_value2:
                index_max2 = i

        z_max = z_value[index_max2]
        z_min = z_value[0]

        if defects == False:
            min = np.min(values[:index_max1])
            for i, val in enumerate(values[:index_max1]):
                if val == min:
                    min_index = i

            den1, den2 = 0., 0.
            for i in range(min_index, index_max2):
                den1 = den1 + density1[i]
                den2 = den2 + density2[i]

            tot = den1 + den2
            return [den1, den2, '{}%, {}%'.format((den1 / tot)*100, (den2 / tot)*100)]
        if defects == True: 
            max2 = np.max(values[:index_max1]) 
            for i, val in enumerate(values[:index_max1]):
                if val == max2:
                    index_max3 = i 
            
            min1 = np.min(values[index_max3:index_max1])
            for i, val in enumerate(values[index_max3:index_max1]):
                if val == min1:
                    min1_index = i

            min2 = np.min(values[:index_max3])
            for i, val in enumerate(values[:index_max3]):
                if val == min2:
                    min2_index = i

            den1, den2 = 0., 0.
            den3, den4 = 0., 0.

            for i in range(min1_index, index_max2):
                den1 = den1 + density1[i]
                den2 = den2 + density2[i]

            for i in range(min2_index, index_max3):
                den3 = den3 + density1[i]
                den4 = den4 + density2[i]

            tot1 = den1 + den2
            tot2 = den3 + den4

            return [den1, den2, den3, den4, '{}%, {}%, {}%, {}%'.format((den1 / tot1)*100, (den2 / tot1)*100,(den3 / tot2)*100, (den4 / tot2)*100)]
            
     
class VDW():

    def Distance(self, mol_type = int, nmol = [int, int,...], trajec_num = int, XYZ = list, nsit = [int, int, ...],
    start = 0, end = int, z_vwd_max = float, r_step = 0.1, layer_frozen_index = int,mol_select = None, time = None):

        def decor(funct):
            def wrap():
                print('=========================================')
                funct()
                print('=========================================')
            return wrap()

        if start < 0 or end > trajec_num:
            @decor 
            def print_error():
                print('Error 😊')
                print('start < 0 or end >  trajec_num') 
            exit()
        
        if start >= end :
            @decor 
            def print_error():
                print('Error 😊')
                print('start >=  end')
            exit()

        if not XYZ:
            @decor
            def print_error():
                print('error 😊')
                print("XYZ_COM cannot be empty")
            exit()

        if not mol_select:
            index_selc = [int(x) for x in range(0, mol_type)]
        
        else:
            index_selc = mol_select

        
        total_trajec = end - start 

        h_bin = []
        bin_in = int(z_vwd_max / r_step) + 1
        for i in range(0, bin_in):
            h_bin.append(float(i) * float(z_vwd_max / bin_in))

        storage = [[]]

        with alive_bar(len(index_selc) * total_trajec, title='Computing VdW D') as bar:
            for i in range(0, len(index_selc)):
                #storage1 = []
                for t in range(start, end):
                    #for j in range(0, nmol[mol_select[i]]):
                    storage2 = []
                    for k in range(0, nsit[mol_select[i]]):
                        if i != int(layer_frozen_index):
                            x, y, z = XYZ[mol_select[i]][t, 0, k, 0:3]
                            x_f, y_f, z_f = XYZ[layer_frozen_index][t, 0, 0, 0:3]
                            d_vdw = z - z_f
                            storage2.append(abs(d_vdw))
                        else:
                            @decor
                            def print_error():
                                print('Error')
                                print('layer_frozen_index should not be in', index_selc)
                                print('Put the correct value and try again')
                            exit()
                    sleep(0.001)
                    bar()   

                    storage[i].append(np.mean(storage2))

            for i in range(0, len(index_selc)):
                storage[i] = np.array(storage[i]) 
                #storage[i] = storage[i].sum(axis = 0) / total_trajec

        return [np.array(h_bin[0:len(h_bin)-1]), storage[0] ]