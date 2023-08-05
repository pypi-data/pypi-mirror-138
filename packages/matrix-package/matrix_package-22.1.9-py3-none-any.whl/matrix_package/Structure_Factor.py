import numpy as np
import pandas as pd 
from math import pi 

class SFT:
    def Structure_Factor(self, input_gdr = str, output = str, sep = None, type = str, Mass = None, density = None, solver = str, atomic_unity = str,
    wavelength = float, max_iter = int, max_float = 5, multi_solver = False, return_SF_as = 'XYZ', 
    box = list, q_max = 16.0, atm_d = False, atm_density = float):

        global molecular_density
        def decor(func):
            def wrap():
                print("==================================================")
                func()
                print("==================================================")
            return wrap()

        if type == 'CSV':
            gdr = pd.read_csv(input_gdr, sep = sep, header = False)
            data_r_gdr = gdr.values
        elif type == 'XYZ':
            file = open(input_gdr, 'r')
            max_config = int(file.readline())
            character = file.readline().split()
            data_r_gdr = []
            for line in range(0, max_config):
                data_r_gdr.append([float(line) for line in file.readline().split()] )     
            file.close()
            data_r_gdr = np.array(data_r_gdr) 
            

            true_solver = ['simpson', 'runge-kutta2', 'runge-kutta4', 'rk-f45', 'euler', 
            'adams-bashforth2', 'adams-bashforth3', 'adams-bashforth4','adams-bashforth5', 'adams-moulton2', 'adams-moulton3']

        if len(density) != len(Mass):
            @decor
            def print_error():
                print('error')
                print('Mass and density should have the same length')
            exit()

        if not density or not Mass:
            @decor
            def print_error():
                print('error')
                print('Mass or density cant not be empty')
            exit()
        if solver not in true_solver:
            @decor
            def print_error():
                print('error')
                print('solver not in list >>>', true_solver)
            exit()

        if atomic_unity == 'angstrom':
            data_r_gdr[:, 0] = data_r_gdr[:, 0] 
            wavelength = wavelength
        elif atomic_unity == 'bohr':
            coef_conv = 0.529177 
            wavelength = wavelength * coef_conv
            data_r_gdr[:, 0] = data_r_gdr[:, 0] * coef_conv
        else:
            @decor
            def print_error():
                print('error')
                print('atomic_unity not in [angstrom, bohr]')
            exit()

        L  = 16.20
        dq = (2.0 * pi) / ( L * int(max_iter))

        max_iter_final = int(q_max / dq)
        summ = 0.5
        wave_vector = []
        for i in range(0, max_iter_final):
            summ = summ + dq
            wave_vector.append(summ)
        if atm_d == False:
            density = np.array(density)
            Mass = np.array(Mass) 
            delta, n_avogadro = 1e-24, 6.023e+23
            atomic_density = ((density * n_avogadro) / Mass) * delta 
            molecular_density =  atomic_density * 4.0 * pi
        else:
            molecular_density = np.array([atm_density]) * 4.0 * pi
        
        print(molecular_density)

        if solver == 'euler':
            s_factor = SFT().euler(data_r_gdr, max_iter_final, wave_vector)
        elif solver == 'simpson':
            s_factor = SFT().simpson(data_r_gdr, max_iter_final, wave_vector)
        elif solver == 'runge-kutta2':
            s_factor = SFT().runge_ktta2(data_r_gdr, max_iter_final, wave_vector)
        elif solver == 'adams-bashforth5':
            s_factor = SFT().adams_bashforth5(data_r_gdr, max_iter_final, wave_vector)
        elif solver == 'adams-moulton3':
             s_factor = SFT().adams_moulton3(data_r_gdr, max_iter_final, wave_vector)

        return [wave_vector, s_factor]

    def simpson(self, matrix, max_iter, wave_vector):
        loop_v = matrix.shape[1]
        loop_h = matrix.shape[0]
        dr = matrix[1,0] - matrix[0,0]

        if matrix[0, 0] != 0.0:
            max_emp = int(matrix[0, 0] / dr) 
            new_arr = np.arange(0.0, matrix[0,0], dr)
            new_arr = new_arr.reshape((new_arr.shape[0],1))
            
            gdr_new_arr = []

            matrix_ = []

            for v in range(0, new_arr.shape[0]):
                gdr_new_arr.append([0.0])
            gdr_new_arr = np.array(gdr_new_arr) 
            arr = np.hstack((new_arr, gdr_new_arr))

            for (r, gdr) in arr:
                matrix_.append([r, gdr])
            for (r, gdr) in matrix:
                matrix_.append([r, gdr])
            matrix_ = np.array(matrix_)
        
        matrix = matrix_ 
        loop_h = matrix.shape[0]

        if matrix[0, 0] != 0.0:
            max_emp = int(matrix[0, 0] / dr) 
            new_arr = np.arrange(0.0, matrix[0,0], dr)
            print(new_arr)

        for j in range(1, loop_v):
            structure_factor = []
            val1 = []
            for i in range(0, max_iter):
                final = 0.0
                for h in range(0, loop_h-1):
                    c1 =  molecular_density[j-1] * dr * np.sin( matrix[h, 0] * wave_vector[i] ) * ( matrix[h, 0] ) * (matrix[h, j] - 1.0)
                    c2 =  molecular_density[j-1] * dr * np.sin( (matrix[h, 0] +  (dr/ 2.0) ) * wave_vector[i] ) * ( (matrix[h, 0] + (dr / 2.0)) ) * (matrix[h, j] - 1.0)
                    c3 =  molecular_density[j-1] * dr * np.sin( (matrix[h+1, 0] ) * wave_vector[i] ) * ( (matrix[h+1, 0]) ) * (matrix[h+1, j] - 1.0)
                    total = (c1 + 4.0 * c2 + c3) / 6.0
                    final = final + total / wave_vector[i] 
                val1.append(1.0 + final )
            structure_factor.append(val1)

        structure_factor = np.array(structure_factor) 
        structure_factor = structure_factor 
        return structure_factor
    
    def runge_ktta2(self, matrix, max_iter, wave_vector):
        loop_v = matrix.shape[1]
        loop_h = matrix.shape[0]
        dr = matrix[1,0] - matrix[0,0]

        if matrix[0, 0] != 0.0:
            max_emp = int(matrix[0, 0] / dr) 
            new_arr = np.arange(0.0, matrix[0,0], dr)
            new_arr = new_arr.reshape((new_arr.shape[0],1))
            
            gdr_new_arr = []

            matrix_ = []

            for v in range(0, new_arr.shape[0]):
                gdr_new_arr.append([0.0])
            gdr_new_arr = np.array(gdr_new_arr) 
            arr = np.hstack((new_arr, gdr_new_arr))

            for (r, gdr) in arr:
                matrix_.append([r, gdr])
            for (r, gdr) in matrix:
                matrix_.append([r, gdr])
            matrix_ = np.array(matrix_)
        
        matrix = matrix_ 
        loop_h = matrix.shape[0]
        for j in range(1, loop_v):
            structure_factor = []
            val1 = []
            for i in range(0, max_iter):
                final = 0.0
                for h in range(0, loop_h-1):
                    c1 = molecular_density[j-1]  * dr * np.sin( matrix[h, 0] * wave_vector[i] ) * ( matrix[h, 0] ) * (matrix[h, j] - 1.0)
                    c2 = molecular_density[j-1]  * dr * np.sin( (matrix[h+1, 0]) * wave_vector[i] ) *  ( matrix[h+1, 0] ) * (matrix[h+1, j] - 1.0)
                    total = (c1 + c2) / 2.0
                    final = final + total / wave_vector[i]
                val1.append(1.0 + final )
            structure_factor.append(val1)

        structure_factor = np.array(structure_factor) 
        structure_factor = structure_factor
        return structure_factor

    def runge_ktta4(self, matrix, max_iter, wave_vector):
        loop_v = matrix.shape[1]
        loop_h = matrix.shape[0]
        dr = matrix[1,0] - matrix[0,0]

        for j in range(1, loop_v):
            structure_factor = []
            val1 = []
            for i in range(0, max_iter):
                
                for h in range(0, loop_h-1):
                    final = 0.0
                    c1 = molecular_density[j] * dr * np.sinc( matrix[h, 0] * wave_vector[i] ) * np.square(matrix[h, 0] ) * (matrix[h, j] - 1.0)
                    c2 = molecular_density[j] * dr * np.sinc( (matrix[h, 0] + (dr / 2.0)) * wave_vector[i] ) * np.square( matrix[h+1, 0] + (dr / 2.0) ) * (matrix[h, j] - 1.0)
                    c3 = molecular_density[j] * dr * np.sinc( (matrix[h, 0] + (dr / 2.0)) * wave_vector[i] ) * np.square( matrix[h+1, 0] + (dr / 2.0) ) * (matrix[h, j] - 1.0)
                    c4 = molecular_density[j] * dr * np.sinc( (matrix[h, 0] + dr)* wave_vector[i] ) * np.square( (matrix[h, 0] + dr) ) * (matrix[h+1, j] - 1.0)
                    final = final +  ( c1 + 2.0 * c2 + 2.0 * c3 + c4 ) / 6.0
                
                val1.append(1.0 + final)
            structure_factor.append(val1)
            
        structure_factor = np.array(structure_factor) 
        structure_factor = structure_factor
        return structure_factor

    def euler(self, matrix, max_iter, wave_vector):
        loop_v = matrix.shape[1]
        loop_h = matrix.shape[0]
        
        dr = matrix[1,0] - matrix[0,0]

        for j in range(1, loop_v):
            structure_factor = []
            val1 = []
            for i in range(0, max_iter):
                for h in range(0, loop_h-1):
                    final = 0.0
                    c1 = molecular_density[j-1] * dr * np.sinc( matrix[h, 0] * wave_vector[i] ) * np.square(matrix[h, 0] ) * (matrix[h, j] - 1.0)
                    final = final + c1
                val1.append(1.0 + final)
            structure_factor.append(val1)

        structure_factor = np.array(structure_factor) 
        structure_factor = structure_factor 
        return structure_factor

    def adams_bashforth2(self, matrix, max_iter, wave_vector):
        loop_v = matrix.shape[1]
        loop_h = matrix.shape[0]
        dr = matrix[1,0] - matrix[0,0]

        for j in range(1, loop_v):
            structure_factor = []
            val1 = []
            for i in range(0, max_iter):
                
                for h in range(0, loop_h-1):
                    val2 = [] 
                    c1 = molecular_density[j-1] * dr * np.sinc( matrix[h, 0] * wave_vector[i] ) * np.square(matrix[h, 0] ) * (matrix[h, j] - 1.0)
                    c2 = molecular_density[j-1] * dr * np.sinc( (matrix[h, 0] + dr) * wave_vector[i] ) * np.square( (matrix[h, 0] + dr) ) * (matrix[h+1, j] - 1.0) 
                    final = ( 3.0 * c2 - c1) / 2.0
                    val2.append(final)
                val1.append(np.sum(val2))
            structure_factor.append(val1)

        structure_factor = np.array(structure_factor) 
        structure_factor = structure_factor + 1.0
        return structure_factor

    def adams_bashforth3(self, matrix, max_iter, wave_vector):
        loop_v = matrix.shape[1]
        loop_h = matrix.shape[0]
        dr = matrix[1,0] - matrix[0,0]

        for j in range(1, loop_v):
            structure_factor = []
            val1 = []
            for i in range(0, max_iter):
                
                for h in range(0, loop_h-2):
                    val2 = [] 
                    c1 = molecular_density[j-1] * dr * np.sinc( matrix[h, 0] * wave_vector[i] ) * np.square(matrix[h, 0] ) * (matrix[h, j] - 1.0)
                    c2 = molecular_density[j-1] * dr * np.sinc( (matrix[h, 0] + dr) * wave_vector[i] ) * np.square( (matrix[h, 0] + dr) ) * (matrix[h+1, j] - 1.0)
                    c3 = molecular_density[j-1] * dr * np.sinc( (matrix[h, 0] + 2.0 * dr) * wave_vector[i] ) * np.square( (matrix[h, 0] + 2.0 * dr) ) * (matrix[h+2, j] - 1.0)
                    
                    final = ( 23.0 * c3 - 16.0 * c2 + 5.0 * c1) / 12.0
                    val2.append(final)
                val1.append(np.sum(val2))
            structure_factor.append(val1)

        structure_factor = np.array(structure_factor) 
        structure_factor = structure_factor + 1.0
        return structure_factor

    def adams_bashforth4(self, matrix, max_iter, wave_vector):
        loop_v = matrix.shape[1]
        loop_h = matrix.shape[0]
        dr = matrix[1,0] - matrix[0,0]

        for j in range(1, loop_v):
            structure_factor = []
            val1 = []
            for i in range(0, max_iter):
                
                for h in range(0, loop_h-3):
                    val2 = [] 
                    c1 = molecular_density[j-1] * dr * np.sinc( matrix[h, 0] * wave_vector[i] ) * np.square(matrix[h, 0] ) * (matrix[h, j] - 1.0)
                    c2 = molecular_density[j-1] * dr * np.sinc( (matrix[h, 0] + dr) * wave_vector[i] ) * np.square( (matrix[h, 0] + dr) ) * (matrix[h+1, j] - 1.0)
                    c3 = molecular_density[j-1] * dr * np.sinc( (matrix[h, 0] + 2.0 * dr) * wave_vector[i] ) * np.square( (matrix[h, 0] + 2.0 * dr) ) * (matrix[h+2, j] - 1.0)
                    c4 = molecular_density[j-1] * dr * np.sinc( (matrix[h, 0] + 3.0 * dr) * wave_vector[i] ) * np.square( (matrix[h, 0] + 3.0 * dr) ) * (matrix[h+3, j] - 1.0)
                    
                    final = ( 55.0 * c4 - 59.0 * c3 + 37.0 * c2 - 9.0 * c1) / 24.0
                    val2.append(final)
                val1.append(np.sum(val2))
            structure_factor.append(val1)

        structure_factor = np.array(structure_factor) 
        structure_factor = structure_factor + 1.0
        return structure_factor

    def adams_bashforth5(self, matrix, max_iter, wave_vector):
        loop_v = matrix.shape[1]
        loop_h = matrix.shape[0]
        dr = matrix[1,0] - matrix[0,0]

        if matrix[0, 0] != 0.0:
            max_emp = int(matrix[0, 0] / dr) 
            new_arr = np.arange(0.0, matrix[0,0], dr)
            new_arr = new_arr.reshape((new_arr.shape[0],1))
            
            gdr_new_arr = []

            matrix_ = []

            for v in range(0, new_arr.shape[0]):
                gdr_new_arr.append([0.0])
            gdr_new_arr = np.array(gdr_new_arr) 
            arr = np.hstack((new_arr, gdr_new_arr))

            for (r, gdr) in arr:
                matrix_.append([r, gdr])
            for (r, gdr) in matrix:
                matrix_.append([r, gdr])
            matrix_ = np.array(matrix_)
        
        matrix = matrix_ 
        loop_h = matrix.shape[0]

        for j in range(1, loop_v):
            structure_factor = []
            val1 = []
            for i in range(0, max_iter):
                final = 0.0
                for h in range(0, loop_h-4):
                    
                    c1 = molecular_density[j-1] * dr * np.sin( matrix[h, 0] * wave_vector[i] ) * (matrix[h, 0] ) * (matrix[h, j] - 1.0)
                    c2 = molecular_density[j-1] * dr * np.sin( (matrix[h, 0] + dr) * wave_vector[i] ) * ( (matrix[h, 0] + dr) ) * (matrix[h+1, j] - 1.0)
                    c3 = molecular_density[j-1] * dr * np.sin( (matrix[h, 0] + 2.0 * dr) * wave_vector[i] ) * ( (matrix[h, 0] + 2.0 * dr) ) * (matrix[h+2, j] - 1.0)
                    c4 = molecular_density[j-1] * dr * np.sin( (matrix[h, 0] + 3.0 * dr) * wave_vector[i] ) * ( (matrix[h, 0] + 3.0 * dr) ) * (matrix[h+3, j] - 1.0)
                    c5 = molecular_density[j-1] * dr * np.sin( (matrix[h, 0] + 4.0 * dr) * wave_vector[i] ) * ( (matrix[h, 0] + 4.0 * dr) ) * (matrix[h+4, j] - 1.0)
                    
                    total = ( 1901 * c5 - 2774.0 * c4 + 2616.0 * c3 - 1274.0 * c2 + 251.0 * c1) / 720.0
                    final = final +  total / wave_vector[i]
                val1.append(1.0 + final)
            structure_factor.append(val1)

        structure_factor = np.array(structure_factor) 
        structure_factor = structure_factor 
        return structure_factor

    def adams_moulton2(self, matrix, max_iter, wave_vector):
        loop_v = matrix.shape[1]
        loop_h = matrix.shape[0]
        dr = matrix[1,0] - matrix[0,0]

        for j in range(1, loop_v):
            structure_factor = []
            val1 = []
            for i in range(0, max_iter):
                
                for h in range(0, loop_h-2):
                    val2 = [] 
                    c1 = molecular_density[j-1] * dr * np.sinc( matrix[h, 0] * wave_vector[i] ) * np.square(matrix[h, 0] ) * (matrix[h, j] - 1.0)
                    c2 = molecular_density[j-1] * dr * np.sinc( (matrix[h, 0] + dr) * wave_vector[i] ) * np.square( (matrix[h, 0] + dr) ) * (matrix[h+1, j] - 1.0) 
                    c3 = molecular_density[j-1] * dr * np.sinc( (matrix[h, 0] + 2.0*dr) * wave_vector[i] ) * np.square( (matrix[h, 0] + 2.0*dr) ) * (matrix[h+2, j] - 1.0)
                    final = ( (5.0 / 12.0) * c3 + (2.0 / 3.0) * c2 - (1.0 / 12.0) * c1 ) 
                    val2.append(final)
                val1.append(np.sum(val2))
            structure_factor.append(val1)

        structure_factor = np.array(structure_factor) 
        structure_factor = structure_factor + 1.0
        return structure_factor

    def adams_moulton3(self, matrix, max_iter, wave_vector):
        loop_v = matrix.shape[1]
        loop_h = matrix.shape[0]
        dr = matrix[1,0] - matrix[0,0]

        if matrix[0, 0] != 0.0:
            max_emp = int(matrix[0, 0] / dr) 
            new_arr = np.arange(0.0, matrix[0,0], dr)
            new_arr = new_arr.reshape((new_arr.shape[0],1))
            
            gdr_new_arr = []

            matrix_ = []

            for v in range(0, new_arr.shape[0]):
                gdr_new_arr.append([0.0])
            gdr_new_arr = np.array(gdr_new_arr) 
            arr = np.hstack((new_arr, gdr_new_arr))

            for (r, gdr) in arr:
                matrix_.append([r, gdr])
            for (r, gdr) in matrix:
                matrix_.append([r, gdr])
            matrix_ = np.array(matrix_)
        
        matrix = matrix_ 
        loop_h = matrix.shape[0]

        for j in range(1, loop_v):
            structure_factor = []
            val1 = []
            for i in range(0, max_iter):
                final = 0.0
                for h in range(0, loop_h-3):
                    c1 = molecular_density[j-1] * dr * np.sin( matrix[h, 0] * wave_vector[i] ) * (matrix[h, 0] ) * (matrix[h, j] - 1.0)
                    c2 = molecular_density[j-1] * dr * np.sin( (matrix[h, 0] + dr) * wave_vector[i] ) * ( (matrix[h, 0] + dr) ) * (matrix[h+1, j] - 1.0) 
                    c3 = molecular_density[j-1] * dr * np.sin( (matrix[h, 0] + 2.0 * dr) * wave_vector[i] ) * ( (matrix[h, 0] + 2.0 * dr) ) * (matrix[h+2, j] - 1.0)
                    c4 = molecular_density[j-1] * dr * np.sin( (matrix[h, 0] + 3.0 * dr) * wave_vector[i] ) * ( (matrix[h, 0] + 3.0 * dr) ) * (matrix[h+3, j] - 1.0)
                    total = ( 9.0 * c4 + 19.0 * c3 - 5.0 * c2 + 1.0 * c1 ) / 24.0 
                    final = final + total / wave_vector[i]
                val1.append(1.0 + final)
            structure_factor.append(val1)

        structure_factor = np.array(structure_factor) 
        structure_factor = structure_factor
        return structure_factor
        
