# Script to run the photometry for IMACS data
# Note that it is important to change the infile for the separate nights 
# in the  zpt_determination.

python3 zpt_determination.py
python3 plot_depth.py
