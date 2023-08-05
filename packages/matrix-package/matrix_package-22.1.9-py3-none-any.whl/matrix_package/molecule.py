import numpy as np 
import pandas as pd 

from matrix_package.params import param_atom_atom 

class Orientation():
    def Corr(self, mol_type = int, nmol = [int, int,...], trajec_num = int, XYZ_COM = None, max_float = 5, XYZ_A = None, atom_index = list,
    mol_select=None,  start = int, end = int, z_first_layer = float, z_sep = float, max_iter = int, 
    ring_atom_selec = [0, 1, 2, 3, 4], CELL = None, c_start_end = [7, 25], median = [2, 7], mol_chc = dict):
        
        def decor(func):
            def wrap():
                print("==================================================")
                func()
                print("==================================================")
            return wrap()
        
        @decor
        def print_error():
            print("Computing molecule orientation is starting ...".upper())

        if not mol_select:
            index_gdr_com = [int(x) for x in range(0, mol_type)]
        else:
            index_gdr_com = mol_select

        if len(index_gdr_com) > 10:
            @decor
            def print_error():
                print('error')
                print('lenght of mol_select or mol_type is bigger than 10')
            exit()
        
        if start < 0 or end > trajec_num:
            @decor 
            def print_error():
                print('error')
                print('start < 0 or end > ', trajec_num) 
            exit()
        if start >= end :
            @decor 
            def print_error():
                print('error')
                print('start >=  end')
            exit()
     
        storage = param_atom_atom(gamma=mol_type)
        suface_mean1, suface_mean2 = [[],[]], [[],[]]
        boxx, boxy, boxz = CELL

        for i in index_gdr_com: 
            for j in range(0, nmol[i]):
                for t in range(start, end):
                    location, surface1, surface2 = [],[], []     
                    
                    origin_comx,  origin_comy,  origin_comz  = XYZ_COM[i][t, j, 0:3]
                    dis_suf_com = origin_comz - z_first_layer

                    [u1, u2, u3] = Orientation().Surface(XYZ_A, atom_index, i, t, j, median, z_first_layer)
                    normal_vector1 = np.array([u1, u2, u3])

                    if i == 0 :
                        vector = Orientation().Ring(origin_comx, origin_comy, origin_comz, XYZ_A, atom_index, i, t, j, ring_atom_selec)
                        lis = [int(g) for g in range(0, len(vector))] 
                        p = np.random.choice(lis)
                        [v1, v2, v3] = vector[p]
                        
                        normal_vector2 = np.array([v1, v2, v3])
                        
                    if i == 1:
                        [v1, v2, v3] = Orientation().Alkyl_Chain(XYZ_A, atom_index, i, t, j,origin_comx,origin_comy, origin_comz, c_start_end )
                        normal_vector2 = np.array([v1, v2, v3])

                    d1 = np.sqrt(np.square(normal_vector1).sum( ))
                    d2 = np.sqrt(np.square(normal_vector2).sum( ))
                    
                    d1_d2_product = d1 * d2
			
                    d1_d2 = (normal_vector1 * normal_vector2).sum()
                    
                    if d1_d2_product != 0:
                    	cos_theta_s = (3.0 / 2.0) * np.square(d1_d2 / (d1 * d2)) 

                    if dis_suf_com >= z_sep:
                        bulk = cos_theta_s
                        interface = 0.0
                    else:
                        interface = cos_theta_s
                        bulk = 0.0

                    location.append(cos_theta_s)
                    surface1.append(bulk)
                    surface2.append(interface)

                storage[i].append(location)
                suface_mean1[i].append(surface1)
                suface_mean2[i].append(surface2)

        data1, data2, data3 = [[],[]], [[],[]], [[],[]]
        bin_ = [[],[]]
	
        for i in index_gdr_com:      
            storage[i] = np.array(storage[i])
            suface_mean1[i] = np.array(suface_mean1[i]) 
            suface_mean2[i] = np.array(suface_mean2[i])

            storage[i] = storage[i].mean(axis = 1, dtype = np.float64).round(max_float) - 0.5
            suface_mean1[i] = suface_mean1[i].mean(axis = 1, dtype = np.float64).round(max_float) - 0.5
            suface_mean2[i] = suface_mean2[i].mean(axis = 1, dtype = np.float64).round(max_float) - 0.5
            
            min_val, max_val = np.min(storage[i]), np.max(storage[i])
            h = (max_val - min_val) / float(max_iter)
            delta = min_val
            for j in range(0, max_iter+1):
                delta = delta + h
                bin_[i].append(delta)
            summ1 = 0.
            for value in suface_mean1[i]:
                n = [1.0 if (value >= bin_[i][w]) and (value <= bin_[i][w+1]) else 0.0 for w in range(0, len(bin_[i])-1)]
                data1[i].append(n)

            for value in suface_mean2[i]:
                n = [1.0 if (value >= bin_[i][w]) and (value <= bin_[i][w+1]) else 0.0 for w in range(0, len(bin_[i])-1)]
                data2[i].append(n)

            data1[i] = np.array(data1[i])
            data1[i] = data1[i].mean(axis = 0) #/ a1[i][0] #suface_mean1[i].shape[0] #storage[i].shape[0]

            data2[i] = np.array(data2[i])
            data2[i] = data2[i].mean( axis = 0) #/ a2[i][0] #suface_mean2[i].shape[0]
            bin_[i] = np.array(bin_[i][0:max_iter])

        @decor
        def print_error():
            print("end computing  molecule orientation ...".upper())

        return [bin_, data1, data2] 
    
    def Surface(self, XYZ_A, atom_index, i, t, j,median, z_first_layer):
       
        origin_x, origin_y, origin_z = XYZ_A[atom_index[i]][t, j, median[0], 0:3] + XYZ_A[atom_index[i]][t, j, median[1], 0:3]
        origin_z = z_first_layer - origin_z
      
        u1 = 0. #origin_z * origin_y + origin_z * (vec_by - origin_y) 
        u2 = 0. #(vec_ax * 0.5 + origin_x) * origin_z + origin_z * (vec_ax - origin_x)
        u3 = origin_z #origin_x * origin_y # (vec_ax - origin_x) * (vec_by - origin_y)  - (vec_ax * 0.5 + origin_x ) * origin_y
        
        return [u1, u2, u3]

    def Alkyl_Chain(self, XYZ_A, atom_index, i, t, j, origin_comx, origin_comy, origin_comz, c_start_end):
        start_x, start_y, start_z = XYZ_A[atom_index[i]][t, j, c_start_end[0], 0:3] 
        end_x, end_y, end_z = XYZ_A[atom_index[i]][t, j, c_start_end[1], 0:3]
        matrix = XYZ_A[atom_index[i]]
        
        if  matrix.shape[2] >= 25:
        	#a1, a2, a3 = (origin_comx - start_x),(origin_comy - start_y), (origin_comz - start_z)
        	#b1, b2, b3 = (end_x - origin_comx),(end_y - origin_comy), (end_z - origin_comz)
        	#v1, v2, v3 = (a1 + b1) / 2.0, (a2 + b2) / 2.0, (a3 + b3) / 2.0
            v1, v2, v3 = end_x - start_x, end_y - start_y, end_z - start_z
        elif matrix.shape[2] > 16 and matrix.shape[2] <= 19: 
            v1, v2, v3 = end_x - start_x, end_y - start_y, end_z - start_z
        	#v1, v2, v3 = (origin_comx - start_x),(origin_comy - start_y), (origin_comz - start_z)

        return [v1, v2, v3]

    def Ring(self, origin_comx, origin_comy, origin_comz, XYZ_A, atom_index, i, t, j, ring_atom_selec):
        global numerical_vector

        normal_vec, numerical_vector, normal_vec1 = [], [], []
        for l in ring_atom_selec:
            for k in ring_atom_selec:
                if l != k: 
                    numerical_vector.append([k,l])
                    xa, ya, za =  XYZ_A[atom_index[i]][t, j, l, 0:3]
                    xb, yb, zb =  XYZ_A[atom_index[i]][t, j, k, 0:3]

                    vec_ax, vec_ay, vec_az = xa - origin_comx, ya - origin_comy, za - origin_comz
                    vec_bx, vec_by, vec_bz = xb - origin_comx, yb - origin_comy, zb - origin_comz

                    v1 = (vec_ay * vec_bz - vec_az * vec_by)
                    v2 = (vec_az * vec_bx - vec_ax * vec_bz)
                    v3 = (vec_ax * vec_by - vec_ay * vec_bx)
                    normal_vec.append([v1, v2, v3])

                for w in ring_atom_selec:
                    if w != l and w != k and l != k:
                        xg, yg, zg =  XYZ_A[atom_index[i]][t, j, w, 0:3]

                        vec_gax, vec_gay, vec_gaz = xa-xg, ya-yg, za-zg
                        vec_gbx, vec_gby, vec_gbz = xb-xg, yb-yg, zb-zg

                        v_g1 = (vec_gay * vec_gbz - vec_gaz * vec_gby)
                        v_g2 = (vec_gaz * vec_gbx - vec_gax * vec_gbz)
                        v_g3 = (vec_gax * vec_gby - vec_gay * vec_gbx)
                        normal_vec1.append([v_g1, v_g2, v_g3])
    				 
        vec = Orientation().Evaluation(origin_comx, origin_comy, origin_comz, XYZ_A, atom_index, i, t, j, ring_atom_selec, numerical_vector, normal_vec)
        
        new_vec = []
        for i in range(0, len(vec)):
            if vec[i]:
                new_vec.append(vec[i])
        
        return normal_vec			
    	
    def Evaluation(self, origin_comx, origin_comy, origin_comz, XYZ_A, atom_index, i, t, j, ring_atom_selec, ring_plan, normal_vec):
        new_ring_vector = []
        for r_val in ring_plan:
            ring_act = ring_atom_selec[:]
            for w in r_val:
                num = ring_act.index(w)
                del(ring_act[num])
            new_ring_vector.append(ring_act)

        storage = []		
        for k1 in range(0, len(new_ring_vector)):
            r_val_selc = new_ring_vector[k1]
            vec_storage = []
            for w in r_val_selc:
    		
                x, y, z = XYZ_A[atom_index[i]][t, j, w, 0:3]
                dx, dy, dz = (x - origin_comx), (y - origin_comy), (z - origin_comz)
                ring_plan_vec = np.array([dx, dy, dz]) 
                product = (normal_vec * ring_plan_vec).sum()
                vec_storage.append(product)
            storage.append(vec_storage)

        true_ring_vector = []
        for k2 in range(0, len(storage)):
            w1, w2, w3 = storage[k2]
            if (w1 == 0.0 and w2 == 0.0 and w3 == 0.0):
                true_ring_vector.append(normal_vec[k2])

        accuracy = len(true_ring_vector) / len(storage)
        
        return true_ring_vector

    def TFSI(self, XYZ_A, atom_index, i, t, j, carbon):
        x1, y1, z1 =  XYZ_A[atom_index[i]][t, j, carbon[1], 0:3]
        x2, y2, z2 =  XYZ_A[atom_index[i]][t, j, carbon[2], 0:3]

        vec_x, vec_y, vec_z = x1 - x2, y1 - y2, z1 - z2 
        vector = [vec_x, vec_y, vec_z]

        dis = np.sqrt(np.square(vector).sum())   

        return dis	
    	
	
	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
