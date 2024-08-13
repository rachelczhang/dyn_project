import numpy as np
import matplotlib.pyplot as plt
import cmc_parser as cp

rvnum = 20
rv20mod_conv = cp.conversion_file('dynamics/rv20_modified/king.conv.sh')

dyn_dat = np.genfromtxt('dynamics/rv20_modified/king.dyn.dat')
additional = False #flag to determine whether or not to read kingres1 too
#dyn_dat1 = np.genfromtxt('dynamics/rv2.0_modified/kingres1.dyn.dat')
#print(dyn_dat)
#print(dyn_dat1)
bin_dat = np.genfromtxt('dynamics/rv20_modified/king.bin.dat')
#bin_dat1 = np.genfromtxt('dynamics/rv2.0_modified/kingres1.bin.dat')

def per_section(it, is_delimiter=lambda x: x.isspace()):
        ret = []
        for line in it:
            if is_delimiter(line):
                if ret:
                    yield ret  # OR  ''.join(ret)
                    ret = []
            else:
                ret.append(line.rstrip())  # OR  ret.append(line)
        if ret:
            yield ret

def read_output_file(path, model):
    
        import numpy as np
        with open(path + model + 'king.log') as f:
        #with open(path + model + 'output.out') as f:
            sections = list(per_section(f, lambda line: line.startswith('*'))) # comment
        print('sections', len(sections))
        plot_times = []
        plot_max_r = []
        plot_rho_core = []
        plot_N_core = []
        
        for j in range(1,len(sections)):
        
            if 'TotalTime=' in sections[j][0]:
                times = sections[j][0]
                t = times.split(' ')
                t     = t[1]
                t     = t.split('=')
                t     = float(t[1])*rv20mod_conv.time_myr
                plot_times.append(t)
                line = sections[j][1]
                max_r     = line.split('max_r')
                max_r     = max_r[1].split(' ')
                max_r     = max_r[0].split('=')
                max_r     = float(max_r[1])*rv20mod_conv.length_parsec
                plot_max_r.append(max_r)
                line = sections[j][4]
                rho_core     = line.split('rho_core')
                rho_core     = rho_core[1].split(' ')
                rho_core     = rho_core[0].split('=')
                rho_core     = float(rho_core[1])*rv20mod_conv.mass_msun/(rv20mod_conv.length_parsec)**3
                plot_rho_core.append(rho_core)
                line = sections[j][4]
                N_core     = line.split('N_core')
                N_core     = N_core[1].split(' ')
                N_core     = N_core[0].split('=')
                N_core     = float(N_core[1])
                plot_N_core.append(N_core)       
        with open(path + model + 'output.out') as f: 
                sections = list(per_section(f, lambda line: line.startswith('*')))
        for j in range(1,len(sections)):
            if 'TotalTime=' in sections[j][0]:
                times = sections[j][0]
                t = times.split(' ')
                t     = t[1]
                t     = t.split('=')
                t     = float(t[1])*rv20mod_conv.time_myr
                plot_times.append(t)
                line = sections[j][1]
                max_r     = line.split('max_r')
                max_r     = max_r[1].split(' ')
                max_r     = max_r[0].split('=')
                max_r     = float(max_r[1])*rv20mod_conv.length_parsec
                plot_max_r.append(max_r)
                line = sections[j][4]
                rho_core     = line.split('rho_core')
                rho_core     = rho_core[1].split(' ')
                rho_core     = rho_core[0].split('=')
                rho_core     = float(rho_core[1])*rv20mod_conv.mass_msun/(rv20mod_conv.length_parsec)**3
                plot_rho_core.append(rho_core)
                line = sections[j][4]
                N_core     = line.split('N_core')
                N_core     = N_core[1].split(' ')
                N_core     = N_core[0].split('=')
                N_core     = float(N_core[1])
                plot_N_core.append(N_core)       
         
#        for j in range(1,len(sections)):
#
#            if len(sections[j])>1 and 'max_r' in sections[j][1]:
#                line = sections[j][1]
#                max_r     = line.split('max_r')
#                max_r     = max_r[1].split(' ')
#                max_r     = max_r[0].split('=')
#                max_r     = np.float(max_r[1])
#                plot_max_r.append(max_r)
   
#        for j in range(1,len(sections),2):
#            if  len(sections[j])>4 and 'rho_core' in sections[j][4]:
#                line = sections[j][4]
#                rho_core     = line.split('rho_core')
#                rho_core     = rho_core[1].split(' ')
#                rho_core     = rho_core[0].split('=')
#                rho_core     = float(rho_core[1])
#                plot_rho_core.append(rho_core)
#            
#        for j in range(1,len(sections),2):
#            if len(sections[j])>4 and 'N_core' in sections[j][4]:
#                line = sections[j][4]
#                N_core     = line.split('N_core')
#                N_core     = N_core[1].split(' ')
#                N_core     = N_core[0].split('=')
#                N_core     = float(N_core[1])
#                plot_N_core.append(N_core)
#        
        fig, axs = plt.subplots(3,1,figsize = (10,10))

        (ax1),(ax2),(ax3) = axs
        print('rho core', plot_rho_core)
        ax1.plot(plot_times , plot_max_r, color = 'royalblue')
        ax2.plot(plot_times , plot_rho_core, color = 'orchid')
        ax3.plot(plot_times , plot_N_core, color = 'orange')
        
        ax1.set_xlabel('Time [Myr]', fontsize = 15)
        ax2.set_xlabel('Time [Myr]', fontsize = 15)
        ax3.set_xlabel('Time [Myr]', fontsize = 15)
        
        ax1.set_ylabel(r'$ \rm max \, r $ [pc]', fontsize  = 15)
        ax2.set_ylabel(r'$ \rm Core density \, $ [msun/pc^3]', fontsize  = 15)  
        ax3.set_ylabel(r'$ \rm N_{core}$', fontsize  = 15)  
        
        ax2.set_yscale('log')
        ax3.set_yscale('log')
        
        fig.suptitle('rv'+str(rvnum))
        fig.tight_layout()
        fig.subplots_adjust(hspace=0.55, wspace=0.35)
        fig.savefig('coredetails.png')
        fig.clf()
        return fig

read_output_file('dynamics/', 'rv2.0_modified/')

t = []
N_c = []
r_c = []
r_h = []
rho_0 = []
rhoc_s = []
rhoc_b = []
t1 = []
for i in dyn_dat:
        t.append(i[0]*rv20mod_conv.time_myr)
        N_c.append(i[6])
        r_c.append(i[7]*rv20mod_conv.length_parsec)
        r_h.append(i[20]*rv20mod_conv.length_parsec)
        #rho_0.append(i[21])
        rho_0.append(i[21]*rv20mod_conv.mass_msun/(rv20mod_conv.length_parsec)**3)
if additional:
        for j in dyn_dat1:
                t.append(j[0]*rv20mod_conv.time_myr)
                N_c.append(j[6])
                r_c.append(j[7]*rv20mod_conv.length_parsec)
                r_h.append(j[20]*rv20mod_conv.length_parsec)
                rho_0.append(j[21]*rv20mod_conv.mass_msun/(rv20mod_conv.length_parsec)**3)

for g in bin_dat:
        t1.append(g[0]*rv20mod_conv.time_myr)
        rhoc_s.append(g[6]*rv20mod_conv.mass_msun/(rv20mod_conv.length_parsec)**3)
        rhoc_b.append(g[7]*rv20mod_conv.mass_msun/(rv20mod_conv.length_parsec)**3)

if additional:
        for h in bin_dat1:
                t1.append(h[0]*rv20mod_conv.time_myr)
                rhoc_s.append(h[6]*rv20mod_conv.mass_msun/(rv20mod_conv.length_parsec)**3)
                rhoc_b.append(h[7]*rv20mod_conv.mass_msun/(rv20mod_conv.length_parsec)**3)

plt.title('rv'+str(rvnum))
plt.scatter(t, r_c, s=1)
plt.yscale('log')
plt.xlabel('Time [Myr]')
plt.ylabel('Core radius [pc]')
plt.grid()
#plt.xscale('log')
plt.savefig('corerad.png')
plt.clf()

late_rc = []
for i in range(len(t)):
        if t[i] > 10000:
                late_rc.append(r_c[i])
print('Core radius at t=0: ', r_c[0])
print('Average core radius at t=present: ', sum(late_rc)/len(late_rc))

late_rh = []
for i in range(len(t)):
        if t[i] > 10000:
                late_rh.append(r_h[i])
print('Half mass radius at t=0: ', r_h[0])
print('Average half mass radius at t=present: ', sum(late_rh)/len(late_rh))

plt.title('rv'+str(rvnum))
plt.scatter(t, r_h, s=1)
plt.xlabel('Time [Myr]')
plt.ylabel('Half mass radius [pc]')
#plt.xscale('log')
plt.grid()
plt.savefig('halfmassrad.png')
plt.clf()

plt.title('rv'+str(rvnum))
print('min N', np.min(N_c))
plt.scatter(t, N_c, s=1)
plt.xlabel('Time [Myr]')
plt.yscale('log')
plt.ylabel('Number of stars within core')
plt.savefig('numstarsincore.png')
plt.clf()

plt.title('rv'+str(rvnum))
rc_rh = []
for i in range(len(r_c)):
        rc_rh.append(r_c[i]/r_h[i])
plt.scatter(t, rc_rh, s=1)
plt.xlabel('Time [Myr]')
plt.ylabel('Core radius/half mass radius')
plt.xscale('log')
plt.savefig('coredivhalfm.png')
plt.clf()

plt.title('rv'+str(rvnum))
plt.scatter(t, rho_0, s = 1)
plt.xlabel('Time [Myr]')
plt.ylabel('Central density [M_sol/pc^3]')
plt.yscale('log')
plt.savefig('centraldensity.png')
plt.clf()

plt.title('rv'+str(rvnum))
plt.scatter(t1, rhoc_s, s = 1)
plt.xlabel('Time [Myr]')
plt.ylabel('Core density of singles [M_sol/pc^3]')
plt.yscale('log')
plt.savefig('coredensitysing.png')
plt.clf()

plt.title('rv'+str(rvnum))
plt.scatter(t1, rhoc_b, s = 1)
plt.xlabel('Time [Myr]')
plt.ylabel('Core density of binaries [M_sol/pc^3]')
plt.yscale('log')
plt.savefig('coredensitybin.png')
plt.clf()

