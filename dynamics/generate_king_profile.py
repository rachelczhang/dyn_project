# Creates a King profile with N=10^5 stars/binaries and a central concentration (W_0) of 6,
# using COSMIC's initial condition generators
# This imports the version of COSMIC that was downloaded and installed with CMC
# See https://clustermontecarlo.github.io/CMC-COSMIC/initialconditions/index.html for more details
import constants
from cosmic.sample import InitialCMCTable

# Generate the Singles and Binaries Pandas tables.  Here we sample stellar masses from a Kroupa 2001
# IMF, and assign 10% of the stars binary companions.  Radii are set in COSMIC.
# See (https://cosmic-popsynth.github.io/COSMIC/runpop/index.html) for more details on the options here
Singles, Binaries = InitialCMCTable.sampler('cmc', binfrac_model=1.0, primary_model='kroupa01',
                                            ecc_model='thermal', porb_model='log_uniform', qmin=0.1, m2_min=0.08,
                                            cluster_profile='king', met=0.00017, zsun=0.017, size=1000000,w_0=6,
                                            seed=12345, virial_radius=1.0, tidal_radius = 30)

print(Singles.mass_of_cluster)

vg = 220 #km/s
rg = 8000 #pc
rv = 1.0 #pc
m_c = Singles.mass_of_cluster
r_tidal = (constants.G * m_c * constants.Msun / 2. / (vg*constants.km)**2.)**(1./3.) * (rg*constants.PC)**(2./3.) / constants.PC
print(r_tidal)
r_tidal_code = r_tidal/rv

Singles, Binaries = InitialCMCTable.sampler('cmc', binfrac_model=1.0, primary_model='kroupa01',
                                            ecc_model='thermal', porb_model='log_uniform', qmin=0.1, m2_min=0.08,
                                            cluster_profile='king', met=0.00017, zsun=0.017, size=1000000,w_0=6,
                                            seed=12345, virial_radius=1.0, tidal_radius = r_tidal_code)

# Save them to an hdf5 file for CMC with a virial radius of 1pc 
# and an initial tidal radius of 10^6 virial radii
InitialCMCTable.write(Singles, Binaries, filename="king.hdf5")
