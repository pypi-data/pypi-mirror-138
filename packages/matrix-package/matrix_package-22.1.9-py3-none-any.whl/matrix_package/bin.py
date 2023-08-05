import numpy as np

class Bin():

    def bin_size(self, dr = float, CELL = None, delta = float):
        def decor(func):
            def wrap():
                print("==========================================")
                func()
                print("==========================================")
            return wrap()

        if delta < 0 or delta > 1:
            @decor 
            def print_error():
                print("dalta not in [0., 1.]")
            exit()

        if dr < 0:
            @decor
            def print_error():
                print('error'.upper())
                print("r_step cannot be negative but positive ")
            exit()

        boxx, boxy, boxz = CELL
        r = [boxx[0], boxy[1], boxz[2]]
        
        if not delta:
            rmax = np.min(r) / 2.0
        else:
            rmax = ((1. + delta) * np.min(r)) / 2.0

        bin_max = int(rmax / dr) + 1

        h_bin = []

        for i in range(0, bin_max):
            h_bin.append(float( i * (rmax / bin_max)))

        return [h_bin, rmax]

    def bin_interface(self, ind = None, CELL = None, dr = float, delta = None, _dir_ = 'X', double = False,
    h_max = 0., trajec_num = int, XYZ = None):

        def decor(func):
            def wrap():
                print("==========================================")
                func()
                print("==========================================")
            return wrap()

        boxx, boxy, boxz = CELL
        r = [boxx[0], boxy[1], boxz[2]]

        if delta < 0 or delta > 1 :
            @decor 
            def print_error():
                print("dalta not in [0., 1.]")
            exit()
        
        if dr < 0:
            @decor
            def print_error():
                print('error'.upper())
                print("r_step cannot be negative but positive ")
            exit()
        
        t1 = list([])
        t2 = float()

        if type(ind) == type(t1):
            r_maximum = []
            for t in range(0, trajec_num):
                dis = []
                for p in range(0, ind[1]):
                    x, y, z = XYZ[ind[0]][t, 0, p, 0:3]
                    dis.append(z)
                z_max = np.mean(dis)

                if double == False:
                    if not delta:
                        if _dir_ == 'X':
                            rmax = float(r[0] - z_max)
                        elif _dir_ == 'Y':
                            rmax = float(r[1] - z_max)
                        elif _dir_ == 'Z':
                            rmax = float(r[2] - z_max)
                    else:
                        if _dir_ == 'X':
                            rmax = float(r[0] - z_max) * (1. + delta)
                        elif _dir_ == 'Y':
                            rmax = float(r[1] - z_max) * (1. + delta)
                        elif _dir_ == 'Z':
                            rmax = float(r[2] - z_max) * (1. + delta)

                elif double == True:       
                    if _dir_ == 'X':
                        rmax = float(r[0] - 2. * z_max)
                    elif _dir_ == 'Y':
                        rmax = float(r[1] - 2. * z_max)
                    elif _dir_ == 'Z':
                        rmax = float(r[2] - 2. * z_max)
                
                else:
                    @decor
                    def print_error():
                        print('Error')
                        print('doule only takes two values: True or False')
                    exit()

                r_maximum.append(rmax)

        elif type(ind) == type(t2):
            r_maximum = []
            for t in range(0, trajec_num):
                z_max = float(ind)
                if double == False:
                    if not delta:
                        if _dir_ == 'X':
                            rmax = float(r[0] - z_max)
                        elif _dir_ == 'Y':
                            rmax = float(r[1] - z_max)
                        elif _dir_ == 'Z':
                            rmax = float(r[2] - z_max)
                    else:
                        if _dir_ == 'X':
                            rmax = float(r[0] - z_max) * (1. + delta)
                        elif _dir_ == 'Y':
                            rmax = float(r[1] - z_max) * (1. + delta)
                        elif _dir_ == 'Z':
                            rmax = float(r[2] - z_max) * (1. + delta)

                elif double == True:       
                    if _dir_ == 'X':
                        rmax = float(r[0] - 2. * z_max)
                    elif _dir_ == 'Y':
                        rmax = float(r[1] - 2. * z_max)
                    elif _dir_ == 'Z':
                        rmax = float(r[2] - 2. * z_max)
                
                else:
                    @decor
                    def print_error():
                        print('Error')
                        print('doule only takes two values: True or False')
                    exit()
                r_maximum.append(rmax)

        if h_max != 0.:
            rmax = h_max
            bin_max = int(rmax / dr) + 1
        
        else:
            rmax = rmax
            bin_max = int(rmax / dr) + 1

        h_bin = []

        for i in range(0, bin_max):
            h_bin.append(float( i * (rmax / bin_max)))

        return [h_bin, r_maximum]