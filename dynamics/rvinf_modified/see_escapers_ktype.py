import cmc_parser as cp

rv20mod_conv = cp.conversion_file('king.conv.sh')

def a_to_p(a, m1, m2):
        mtot = m1+m2 # in solar masses
        period=(a**3/mtot)**(1/2) ##in years
        period=period*365 ##in days
        return period

def read_single_escapers():
        m = []
        kstar = []
        t = []
        with open('king.esc.dat', 'r') as g:
                next(g)
                for line in g:
                        x = line.split(' ')
                        if int(x[14]) == 0:
                                m.append(float(x[2]))
                                kstar.append(float(x[21]))
                                t_pre = float(x[1])
                                t_pre = t_pre*rv20mod_conv.time_myr
                                t.append(5100.4359-t_pre)
        #with open('kingres1.esc.dat', 'r') as f:
        #       for line in f:
        #               x = line.split(' ')
        #               if int(x[14]) == 0:
        #                       m.append(float(x[2]))
        #                       kstar.append(float(x[21]))
        #                       t_pre = float(x[1])
        #                       t_pre = t_pre*rv20mod_conv.time_myr
        #                       t.append(13800.0-t_pre) 
        return m, kstar, t

def read_binary_escapers():
        m0 = []
        m1 = []
        p = []
        e = []
        kstar1 = []
        kstar2 = []
        t = []
        with open('king.esc.dat', 'r') as g:
                next(g)
                for line in g:
                        x = line.split(' ')
                        if int(x[14]) == 1:
                                m0.append(float(x[15]))
                                m1.append(float(x[16]))
                                a = float(x[19])
                                p.append(a_to_p(a, float(x[15]), float(x[16])))
                                e.append(float(x[20]))
                                kstar1.append(float(x[22]))
                                kstar2.append(float(x[23]))
                                t_pre = float(x[1])
                                t_pre = t_pre*rv20mod_conv.time_myr
                                t.append(5100.4359-t_pre)
        return m0, m1, p, e, kstar1, kstar2, t
m, kstar, t = read_single_escapers()
m0, m1, p, e, kstar1, kstar2, t = read_binary_escapers()

print('single kstars', kstar)
print('binary kstars', kstar1, kstar2)
