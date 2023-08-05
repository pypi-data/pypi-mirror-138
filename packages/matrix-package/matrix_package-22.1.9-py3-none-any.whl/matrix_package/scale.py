from matrix_package.params import * 
import numpy as np
from alive_progress import alive_bar 
from time import sleep
import os , sys

class Scale():
    def StandardScaler(self, trajec_num : int = None, mol_type : int = None, nmol : list = None, nsit : list = None, 
    XYZ : list = None, select_index : any = False, index : list = None, tri : any = False, step : int = None):

        def decor(func):
            def wrap():
                print("=======================================================")
                func()
                print("=======================================================")
            return wrap()

        t1 = list()
        t2 = float()
        t3 = int()
        t4 = bool()
        t5 = str()
        t6 = dict()
        t7 = np.ndarray([])

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
                print(os.getcwd()+'/scale.py')
            exit()
        else:
            if type(trajec_num) != type(t3):
                @decor 
                def print_error():
                    print('TypeError 😊')
                    print('trajec_num is an integer not any other type')
                    print('trajec_num, ', type(t3))
                    print('Put an integer as an input and run again')
                    print(os.getcwd()+'/scale.py')
                exit()
            else:
                if trajec_num < 0:
                    @decor 
                    def print_error():
                        print('ValueError 😊')
                        print('trajec_num cannot be negative')
                        print(os.getcwd()+'/scale.py')
                        print(os.path.basename(__file__))
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

        if select_index == True:
            if not index:
                @decor
                def print_error():
                    print('InputError 😊')
                    print('select_index is defined on <True> but index is Empty')
                    print('When select_index is defined on <True> index cannot be Empty or NULL')
                    print('Check your input and correct it')
                exit()
            else:
                if type(index) != type(t1):
                    @decor 
                    def print_error():
                        print('TypeError 😊')
                        print('index is a list not any other type')
                        print('index, ', type(t1))
                        print('Put a list as an input and run again')
                    exit()
                else:
                    for i, val in enumerate(index):
                        if type(index[i]) != type(t3):
                            @decor 
                            def print_error():
                                print('TypeError 😊')
                                print("The values in index should be integers")
                                print(type(t3))
                                print("Check your values and correct the bad values")
                                print('The bad found is :', val, 'index = ', i, 'from', index)
                            exit()
                        else:
                            if index[i] < 0:
                                @decor 
                                def print_error():
                                    print('ValueError 😊')
                                    print("The values in nsit cannot be negatives")
                                    print("Check your values and correct the bad values")
                                    print('The bad found is :', val, 'index = ', i, 'from', index)
                                exit()
                            else:
                                index = index 
        elif select_index == False:
            index = [int(x) for x in range(0, mol_type)]       
        else:
            @decor 
            def print_error():
                print('TyppeError 😊')
                print('select_index is a boolean type')
                print('select_index', type(t4))
                print('Have a look on your value and correct it')
            exit()

        if tri == False:
            total_trajec = trajec_num
        elif tri == True:

            if step:
                if type(step) != type(t3):
                    @decor 
                    def print_error():
                        print('TypeError 😊')
                        print('step is an integer not any other type')
                        print('step, ', type(t3))
                        print('Put an integer as an input and run again')
                    exit()
                else:
                    if step >= trajec_num:
                        @decor
                        def print_error():
                            print('ValueError 😊')
                            print('step value cannot be egal or bigger than trajec_num')
                            print('Check your value and run again')
                        exit()
            else:
                @decor
                def print_error():
                    print('InputError 😊')
                    print('tri is defined on True but step is empty or NULL')
                    print('when tri is defined on <True> step step cannot be NULL or Empty')
                    print('Check your input and run again')
                exit()      
        else:
            @decor
            def print_error():
                print('TypeError 😊')
                print('tri should is a boolean type')
                print('tri ', type(t4))
                print('Have a look on your input and coorect it')
            exit()

        if len(index) == 1:
           scale1, scale2, scale3 = [[[]],[[]],[[]]] 
        elif len(index) == 2:
            scale1, scale2, scale3= [[[],[]],[[],[]], [[],[]]] 
        elif len(index) == 3:
            scale1, scale2, scale3 = [[[],[],[]],[[],[],[]], [[],[],[]]] 
        elif len(index) == 4:
            scale1, scale2, scale3 = [[[],[],[],[]],[[],[],[],[]], [[],[],[],[]]] 
        elif len(index) == 5:
            scale1, scale2, scale3= [[[],[],[],[],[]],[[],[],[],[],[]], [[],[],[],[],[]]]
        elif len(index) == 6:
            scale1, scale2, scale3 = [[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]]]
        elif len(index) == 7:
            scale1, scale2, scale3 = [[[],[],[],[],[],[],[]],[[],[],[],[],[],[],[]],[[],[],[],[],[],[]]]
        elif len(index) == 8:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]] ]
        elif len(index) == 9:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 10:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 11:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 12:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[]]]
        elif len(index) == 13:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[]]]
        elif len(index) == 14:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 15:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 16:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 17:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 18:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 19:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 20:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 21:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 22:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 23:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 24:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 25:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 26:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 27:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 28:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 29:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 30:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 31:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        elif len(index) == 32:
            scale1, scale2, scale3 = [ [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] ]
        

        if len(nmol) != len(nsit):
            @decor
            def print_error():
                print('ValueError 😊')
                print('nmol and nsit should have the same length')
                print('Check your value and run again')
            exit()

        with alive_bar(len(index), title='StandardScaler') as bar:
            for i in index:
                allocate = []  
                for t in range(0, trajec_num):
                    for j in range(0, nmol[index.index(i)]):
                        allocate.append(nsit[index.index(i)] * j + (nsit[index.index(i)] * nmol[index.index(i)] * t))
                allocate2 = [nmol[index.index(i)] * t for t in range(0, trajec_num+1)]
                allocate.append(nsit[index.index(i)] * nmol[index.index(i)] * trajec_num)
                

                for w in range(0, len(allocate)-1):
                    scal = []
                    for k in range(0, nsit[index.index(i)]):
                        valx = XYZ[i][allocate[w]:allocate[w+1]][k, ]        
                        scal.append( np.array(valx) )
                    scale1[index.index(i)].append(scal)

                scale1[index.index(i)] = np.array(scale1[index.index(i)])
                for w in range(0, len(allocate2)-1):
                    scal = []
                    for j in range(0, nmol[index.index(i)]):
                        value_xyz = scale1[index.index(i)][allocate2[w]:allocate2[w+1]][j, 0:nsit[index.index(i)], ]
                        scal.append(value_xyz)
                    scale2[index.index(i)].append(scal)
                scale2[index.index(i)] = np.array(scale2[index.index(i)])

                if tri == True: 
                    for t in range(0, trajec_num, step):
                        scale3[index.index(i)].append(scale2[index.index(i)][t, ])
                
                else:
                    for t in range(0, trajec_num):
                        scale3[index.index(i)] = scale2[index.index(i)]      

                scale3[index.index(i)] = np.array(scale3[index.index(i)])

                sleep(.001)
                bar()

        return scale3