import numpy as np
from matrix_package.pbc import Periodic_BC, Volume
from matrix_package.bin import Bin
from matrix_package.params import gdr_c
from matrix_package.params import param_atom_atom 
from math import pi
import pandas as pd 

class Radial_Distribution_Function():

    def GDR_COM(self, mol_type = int, nmol = [int, int,...], trajec_num = int, XYZ_COM = None, CELL = None, 
    PBC = False, imcon = int, r_step = float,max_float = 5, mol_select=None, delta = 0, start = 0, end = int, 
    box_replicated = False, rep_num = int):
        
        bn = Bin()

        def decor(func):
            def wrap():
                print("==================================================")
                func()
                print("==================================================")
            return wrap()
        
        @decor
        def print_error():
            print("Starting computing g(r) of center-of-mass ...".upper())

        if not mol_select:
            index_gdr_com = [int(x) for x in range(0, mol_type)]
        
        else:
            index_gdr_com = mol_select

        if len(index_gdr_com) > 10:
            @decor
            def print_error():
                print('Error 😊')
                print('Lenght mol_select or mol_type is bigger 10 ')
            exit()
        
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
                print("start >=  end, and it cannot be impossible ")
                print('totl_trajec = end - start, will be negative')
                print('Put the good values and try egain')
            exit()

        if imcon not in [1, 2, 3, 4, 5, 6]:
            @decor
            def print_error():
                print('error 😊'.capitalize())
                print("imcon not in [1, 2, 3, 4, 5, 6]")
                more_info = """
                1 = cubic, 2 = quadratic, 3 = hexagonal, 4 = orthorhombic, 5 = trigonal prismic, 6 = monoclinic
                """
                print(more_info)
            exit()

        if box_replicated:
            if box_replicated not in [True, False]:
                @decor  
                def print_error():
                    print('Error')
                    print('The Keyword replicated not in [True, False]')
                    print('Check your value and try again')   
                exit()

        volume = Volume(CELL=CELL, imcon=imcon)
        total_trajec = end - start

        [h_bin, rmax] = bn.bin_size(dr = r_step, CELL = CELL, delta = delta)
        gdr = gdr_c()

        boxx, boxy, boxz = CELL

        XYZ_COM_REP = []
        if box_replicated == True :
            xyz_num = []    
            if rep_num % 2 == 0:
                for px in range(0, rep_num+1): 
                    for py in range(0, rep_num+1):
                        for pz in range(0, rep_num+1):
                            
                            numx = float(px - (rep_num-1)*0.5) * boxx[0]
                            numy = float(py - (rep_num-1)*0.5) * boxy[1]
                            numz = float(pz - (rep_num-1)*0.5) * boxz[2] 

                            xyz_num.append([numx, numy, numz])

            else:   
                for px in range(0, rep_num):
                    for py in range(0, rep_num):
                        for pz in range(0, rep_num):
                            
                            numx = float(px - (rep_num-1)*0.5) * boxx[0]
                            numy = float(py - (rep_num-1)*0.5) * boxy[1]
                            numz = float(pz - (rep_num-1)*0.5) * boxz[2]

                            xyz_num.append([numx, numy, numz])

            xyz_num = np.array(xyz_num, dtype=np.float128)
            max_xyz_num = xyz_num.shape[0]

            for i in  index_gdr_com:
                storage = []
                for t in range(start, end):
                    storage.append( [XYZ_COM[i][t, :, :] - xyz_num[l] for l in range(0, xyz_num.shape[0]) ] )
                XYZ_COM_REP.append(storage)

        if box_replicated == True:
            for i in index_gdr_com:
                XYZ_COM_REP[i] = np.array(XYZ_COM_REP[i], dtype=np.float128)

        if box_replicated == False:
            
            for t in range(start, end):
                for i1 in index_gdr_com: 
                    for j1 in range(0, nmol[i1]):
                        for i2 in index_gdr_com: 
                            for j2 in range(0, nmol[i2]):
                                if ( ((i1 == i2) and (j1 != j2)) or (i1 != i2) ):
                                    
                                    dx, dy, dz = XYZ_COM[i1][t, j1, 0:3] - XYZ_COM[i2][t, j2, 0:3]

                                    if PBC == True:
                                        dx, dy, dz = Periodic_BC(dx = dx, dy = dy, dz = dz, CELL = CELL, imcon = imcon)
                                    
                                    elif PBC == False:
                                    
                                        if (t==start and i1== index_gdr_com[0] and j1==0 and i2==index_gdr_com[0] and j2==1):                              
                                            @decor
                                            def print_error():                                      
                                                print('The PBC keyword is defined on False')
                                                print("Do you want to compute the g(r) without PBC's ? YES / NO")
                                                _int_ = str(input ())
                                                if _int_ in ['NO', 'No', 'no']:
                                                    print("exit ...  ☹️ ")
                                                    print("==================================================")
                                                    exit()
                                                
                                                elif _int_ in ['YES', 'Yes', 'yes']:
                                                    print('continue ... 😊')
                                                
                                                else:
                                                    print('Bad answer 😡')
                                                    print("Try ['NO', 'No', 'no'] or ['YES', 'Yes', 'yes'] respectively ")
                                                    print("==================================================")
                                                    exit()
                                    
                                    else:
                                        
                                        if (t==0 and i1== index_gdr_com[0] and j1==0 and i2==index_gdr_com[0] and j2==1):
                                            @decor
                                            def print_error():
                                                print('Error 😊')
                                                print('PBC only takes two values')
                                                print("PBC not in ['True', 'False']")
                                            exit()

                                    r = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2) 
                                    if r < rmax: 
                                        
                                        alpha = [1.0 if (r >= h_bin[h]) and (r < h_bin[h+1]) else 0.0 for h in range(0, len(h_bin)-1)]
                                        gdr[i1][i2].append(alpha)
        
        elif box_replicated == True:

            for t in range(start, end):
                for p1 in range(0, rep_num+1):
                    for p2 in range(0, rep_num+1):
                        for i1 in index_gdr_com: 
                            for j1 in range(0, nmol[i1]):
                                for i2 in index_gdr_com: 
                                    for j2 in range(0, nmol[i2]):
                                        if ( ((i1 == i2) and (j1 != j2)) or (i1 != i2) ):
                                            
                                            dx, dy, dz = XYZ_COM_REP[i1][t, p1, j1, 0:3] - XYZ_COM_REP[i2][t, p2, j2, 0:3]

                                            if PBC == True:
                                                dx, dy, dz = Periodic_BC(dx = dx, dy = dy, dz = dz, CELL = CELL, imcon = imcon)
                                            
                                            elif PBC == False:
                                            
                                                if (t==start and p1 == 0 and p2 ==0 and i1== index_gdr_com[0] and j1==0 and i2==index_gdr_com[0] and j2==1):                              
                                                    @decor
                                                    def print_error():                                      
                                                        print('The PBC keyword is defined on False')
                                                        print("Do you want to compute the g(r) without PBC's ? YES / NO")
                                                        _int_ = str(input ())
                                                        if _int_ in ['NO', 'No', 'no']:
                                                            print("exit ...  ☹️ ")
                                                            print("==================================================")
                                                            exit()
                                                        
                                                        elif _int_ in ['YES', 'Yes', 'yes']:
                                                            print('continue ... 😊')
                                                        
                                                        else:
                                                            print('Bad answer 😡')
                                                            print("Try ['NO', 'No', 'no'] or ['YES', 'Yes', 'yes'] respectively ")
                                                            print("==================================================")
                                                            exit()
                                            
                                            else:
                                                
                                                if (t==0 and i1== index_gdr_com[0] and j1==0 and i2==index_gdr_com[0] and j2==1):
                                                    @decor
                                                    def print_error():
                                                        print('Error 😊')
                                                        print('PBC only takes two values')
                                                        print("PBC not in ['True', 'False']")
                                                    exit()

                                            r = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2) 
                                            if r < rmax: 
                                                
                                                alpha = [1.0 if (r >= h_bin[h]) and (r < h_bin[h+1]) else 0.0 for h in range(0, len(h_bin)-1)]
                                                gdr[i1][i2].append(alpha)

        else:
            @decor  
            def print_error():
                print('Error')
                print('The Keyword replicated not in [True, False]')
                print('Check your value and try again')   
            exit()

        for i1 in index_gdr_com: 
            for i2 in index_gdr_com: 
                gdr[i1][i2] = np.array(gdr[i1][i2])
                if box_replicated == False:
                    gdr[i1][i2] = gdr[i1][i2].sum( axis = 0, dtype = np.float128)  / (nmol[i1] * nmol[i2] * total_trajec)
                elif box_replicated == True:
                    gdr[i1][i2] = gdr[i1][i2].sum( axis = 0, dtype = np.float128)  / (nmol[i1] * nmol[i2] * total_trajec * max_xyz_num)

                for h in range(0, len(h_bin)-1):
                    vol = (4.0 / 3.0) * pi * (h_bin[h+1] ** 3 - h_bin[h] ** 3)
                    gdr[i1][i2][h] = (gdr[i1][i2][h] / vol) * ( volume ) 
                
                gdr[i1][i2] = gdr[i1][i2].reshape((gdr[i1][i2].shape[0],1)).round(max_float)
        
        gdr_com_final = dict(r = h_bin[0:len(h_bin)-1], gdr_com = gdr)

        #return gdr_com_final

        @decor
        def print_error():
            print("endind computing g(r) of center-of-mass ...".upper())

        #return gdr_com_final

        #####################################################################################################################
        ########### true block
        position = dict(r = h_bin[0:len(h_bin)-1])
        _values_ = [np.round(gdr[i1][i2], max_float) for i1 in index_gdr_com for i2 in index_gdr_com]
        _values_ = np.array(_values_).round(max_float)
        df = pd.DataFrame(position)
        #df[list(['{}-{}'.format(i1, i2) for i1 in index_gdr_com for i2 in index_gdr_com])] = _values_.reshape(( _values_.shape[0] , _values_.shape[1] ))
        #df.set_index('r', inplace=True)
        
        #####################################################################################################################

        if mol_type == 1:
            gdr_com_final = np.column_stack(( h_bin[0:len(h_bin)-1], gdr[0][0]))
        
        elif mol_type == 2:
            gdr_com_final = np.column_stack(( h_bin[0:len(h_bin)-1], gdr[0][0], gdr[0][1], gdr[1][1]  ))
       
        elif mol_type == 3:
            gdr_com_final = np.column_stack(( h_bin[0:len(h_bin)-1], gdr[0][0], gdr[0][1], gdr[1][1], gdr[1][2], gdr[2][2] ))
        
        elif mol_type == 4:
            gdr_com_final = np.column_stack(( h_bin[0:len(h_bin)-1], gdr[0][0], gdr[0][1], gdr[0][1], gdr[0][2], gdr[0][3], gdr[1][1],
            gdr[1][2], gdr[1][3], gdr[2][2], gdr[2][3], gdr[3][3] ))
        
        elif mol_type == 5:
            gdr_com_final = np.column_stack(( h_bin[0:len(h_bin)-1], gdr[0][0], gdr[0][1], gdr[0][1], gdr[0][2], gdr[0][3], gdr[0][4],
            gdr[1][1], gdr[1][2], gdr[2][3], gdr[1][4], gdr[2][2], gdr[2][3], gdr[2][4], gdr[3][3], gdr[3][4], ))
        
        else:
            exit()

        return  gdr_com_final
           
    def GDR_Atom_Atom(self, PBC=False, nmol = [int, int, ...], nsit = [int, int, ...], trajec_num = int, 
    start = 0, end = int, atoms_select = [[0, 0, 1, 4], [1, 0, 0, 1], [1, 1, 6, 0], [1, 0, 5, 1]], mol_type = int,
    delta = 0, max_float = 5, imcon = int, r_step = float, CELL = None, XYZ = None):
        
        def decor(func):
            def wrap():
                print("==================================================")
                func()
                print("==================================================")
            return wrap()

        bn = Bin()

        @decor
        def print_error():
            print("Starting computing g(r) atoms-atoms ...".upper())

        for i in range(0, mol_type):
            if len(XYZ[i].shape) not in [3, 4, 5,6]:
                @decor
                def print_error():
                    print('Error 😊')
                    print('Impossible to read XYZ coordinates')
                    print('Use StandardScaler() before using XYZ file')
                exit()

        mol_select = []

        if not atoms_select:
            @decor
            def print_error():
                print('Error 😊')
                print("atoms_select can't be empty or NULL")
                print('Put its values and try again')
            exit()
        
        else:
            if not mol_type:
                @decor
                def print_error():
                    print('Error 😊')
                    print("mol_type is empty or NULL")
                    print('Put the good value and try again')
                exit()
            
            else:
                for vl1 in atoms_select:
                    w1, w2, w3, w4 = vl1

                    if w1 > mol_type:
                        @decor
                        def print_error():
                            print('Error 😊')
                            print('problem in ', [w1, w2, w3, w4], w1,' > mol_type')
                        exit()

                    elif w2 > mol_type:
                        @decor
                        def print_error():
                            print('error'.upper())
                            print('problem in ', [w1, w2, w3, w4], w2,' > mol_type')
                        exit()

                    mol_select.append([w1, w2])

            for i in range(0, len(atoms_select)):
                
                if (len(atoms_select) > 10)  or (len(atoms_select[i]) != 4):
                    @decor
                    def print_error():
                        print('Error 😊')
                        print(" length of atoms_select is >", 10)
                        print("or length  atoms_select[i] are differents of 4")
                    exit()

            for varr  in atoms_select:
                varr1, varr2, varr3, varr4 = varr
                
                if varr3 > nsit[varr1]:
                    
                    @decor
                    def print_error():
                        print('Error 😊')
                        print(varr3,' > ', nsit[varr1])
                    exit()
                
                elif varr4 > nsit[varr2]:
                    @decor
                    def print_error():
                        print('Error 😊'.capitalize())
                        print(varr3,' > ', nsit[varr1])
                    exit()

        if not trajec_num:
            @decor
            def print_error():
                print('error 😊'.capitalize())
                print("trajec_num is empty or NULL")
                print('Put the Good value and Try again')
            exit()

        if start < 0 or end > trajec_num:
            @decor 
            def print_error():
                print('error 😊'.capitalize())
                print('start < 0 or end > ', trajec_num) 
            exit()

        if start >= end :
            @decor 
            def print_error():
                print('error')
                print('start >=  end')
                print('total_trajec = end - start, will be negative')
            exit()

        if imcon not in [1, 2, 3, 4, 5, 6]:
            @decor
            def print_error():
                print('error 😊'.capitalize())
                print("imcon not in [1, 2, 3, 4]")
                more_info = """
                1 = cubic, 2 = quadratic, 3 = hexagonal, 4 = orthorhombic, 5 = trigonal prismic, 6 = monoclinic
                """
                print(more_info)
            exit()
        
        volume = Volume(CELL=CELL, imcon=imcon)
        total_trajec = end - start

        _val_ = []
        [h_bin, rmax] = bn.bin_size(dr = r_step, CELL = CELL, delta = delta)
        gdr = gdr_c()
        gdr_aa = param_atom_atom (gamma = len(atoms_select))

        for t in range(start, end):
            for k in range(0, len(atoms_select)):
                if t == start:
                    if k < mol_type:
                        i1, i2 = 0, k
                    else:
                        if k % mol_type == 0:
                            i1 = int(k / mol_type)
                            i2 = (k % mol_type)
                        elif k % mol_type == 1:
                            i1 = int((k-1) / mol_type)
                            i2 = (k % mol_type)
                        elif k % mol_type == 2:
                            i1 = int((k-2) / mol_type)
                            i2 = (k % mol_type)
                for j1 in range(0, nmol[mol_select[k][0]]):    
                    for j2 in range(0, nmol[mol_select[k][1]]):
                        if ( (atoms_select[k][2] == atoms_select[k][3] and j1 != j2) or (atoms_select[k][2] != atoms_select[k][3]) ):
                            
                            if XYZ[mol_select[k][0]].shape[0] == 3:
                                dx, dy, dz = XYZ[mol_select[k][0]][t, j1, atoms_select[k][2], 0:3] - XYZ[mol_select[k][1]][t, j2, atoms_select[k][3], 0:3]
                            
                            elif XYZ[mol_select[k][0]].shape[0] == 4:
                                dx, dy, dz = XYZ[mol_select[k][0]][t, j1, atoms_select[k][2], 1:4] - XYZ[mol_select[k][1]][t, j2, atoms_select[k][3], 1:4]
                            
                            elif XYZ[mol_select[k][0]].shape[0] == 5:
                                dx, dy, dz = XYZ[mol_select[k][0]][t, j1, atoms_select[k][2], 1:4] - XYZ[mol_select[k][1]][t, j2, atoms_select[k][3], 1:4]
                            
                            elif XYZ[mol_select[k][0]].shape[0] == 6:
                                dx, dy, dz = XYZ[mol_select[k][0]][t, j1, atoms_select[k][2], 1:4] - XYZ[mol_select[k][1]][t, j2, atoms_select[k][3], 1:4]

                            if PBC == True:
                                dx, dy, dz = Periodic_BC(dx = dx, dy = dy, dz = dz, CELL = CELL, imcon = imcon)
                                
                            elif PBC == False:
                                if (t==start and k == 0 and j1==0 and j2 in [1 if atoms_select[k][2] == atoms_select[k][3] else 0] ):                              
                                    @decor
                                    def print_error():                                      
                                        print('The PBC keyword is defined on False')
                                        print('Do you want to continue ? YES / NO')
                                        _int_ = str(input ())
                                        if _int_ in ['NO', 'No', 'no']:
                                            print("Exit() ...")
                                            print("==================================================")
                                            exit()
                                        elif _int_ in ['YES', 'Yes', 'yes']:
                                            print('continue ...😊')
                                        else:
                                            print('Bad ansswer 😡')
                                            print("Try ['NO', 'No', 'no'] or ['YES', 'Yes', 'yes'] respectively ")
                                            print('Exit() ...')
                                            print("==================================================")
                                            exit()
                            else:
                                if (t==start and k == 0 and j1==0 and j2 in [1 if atoms_select[k][2] == atoms_select[k][3] else 0] ):
                                    @decor
                                    def print_error():
                                        print('Error 😊')
                                        print('PBC value only takes two values')
                                        print("PBC value not in ['True', 'False']")
                                    exit()

                            r = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2) 
                            if r < rmax: 
                                    
                                alpha = [1.0 if (r >= h_bin[h]) and (r <= h_bin[h+1]) else 0.0 for h in range(0, len(h_bin)-1)]
                                gdr[i1][i2].append(alpha)
                                gdr_aa[k].append(alpha)

                _val_.append([i1, i2])

        ####################################################################################################
        # after test i will delate this block
        for i1 in range(0, mol_type):
            for i2 in range(0, mol_type):       
                gdr[i1][i2] = np.array(gdr[i1][i2])
                gdr[i1][i2] = gdr[i1][i2].sum( axis = 0)  / ( nmol[i1] * nmol[i2] * total_trajec )
                for h in range(0, len(h_bin)-1):
                    vol = (4.0 / 3.0) * pi * (h_bin[h+1] ** 3 - h_bin[h] ** 3)
                    gdr[i1][i2][h] = gdr[i1][i2][h] * (volume / vol)
                    
                gdr[i1][i2] = gdr[i1][i2].reshape((gdr[i1][i2].shape[0],1)).round(max_float)
        ####################################################################################################


        for k in range(0, len(atoms_select)):
            gdr_aa[k] = np.array(gdr_aa[k])
            gdr_aa[k] = gdr_aa[k].sum( axis = 0) / ( nmol[mol_select[k][0]] * nmol[mol_select[k][1]] * total_trajec )
            
            for h in range(0, len(h_bin)-1):
                vol = (4.0 / 3.0) * pi * (h_bin[h+1] ** 3 - h_bin[h] ** 3)
              
                gdr_aa[k][h] = ( gdr_aa[k][h] / vol ) * ( volume )
            
            gdr_aa[k] =  gdr_aa[k].reshape(( gdr_aa[k].shape[0], 1)).round(max_float)
        
        position = dict(r = h_bin[0:len(h_bin)-1])

        @decor
        def print_error():
            print("ending computing g(r) atoms-atoms...".upper())

        length = len(h_bin)-1
        _values_ = [np.round(gdr_aa[i],max_float) for i in range(0, len(atoms_select))]
        _values_ = np.array(_values_).round(max_float)
        
        df = pd.DataFrame(position)
        df[list([str(atoms_select[i]) for i in range(0, len(atoms_select))])] = _values_.reshape(( length, _values_.shape[1] ))
        df.set_index('r', inplace=True)

        return df 
