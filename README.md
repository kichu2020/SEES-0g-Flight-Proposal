# SEES-0g-Flight-Proposal
Python Simulation code for SEES 0g Project: Acoustic Field Control of Suspended Particles in Microgravity Fluid Chambers
There are three scripts for the simulation: 

1. Particle band formation generator script: particle_band_simulator.py
This script creates the simulated particle images used in the analysis. It generates synthetic bead patterns with adjustable band strength, dispersion, bead size, and number of bands, and includes sliders so these parameters can be changed interactively. The final images can then be saved and used as input for the FFT analysis, making this the script that creates the band formations themselves.

2. FFT metric extraction script: particle_banding_fft_metrics.py
This script loads each particle image, converts it to a binary bead mask, and computes a vertical bead-density profile by summing beads across each row. It then applies a 1D Fast Fourier Transform (FFT) to that profile to measure periodic banding. From the FFT, it extracts the dominant band spacing, dominant peak bin, FFT peak SNR, and a contrast metric, giving quantitative measures of ordering strength for the strong, medium, and weak cases.

3. FFT spectrum comparison script: fft_spectrum_comparison.py
This script loads the strong, medium, and weak particle images, computes the FFT magnitude spectrum for each one, and overlays all three spectra on a single graph. Its purpose is to visually compare how the dominant spectral peak changes across different banding strengths while keeping the spatial wavelength constant. This shows that stronger ordering produces a larger FFT peak.
