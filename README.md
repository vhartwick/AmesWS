# =====================
# AmesWS
# Web Server Application for Ames FV3 Mars Climate Model Data Access & Visualization
# V2 - depracated functionalities : download additional variables
#      			            plot same variable at multiple atm levels
#				    time series hover plot
#      new features : NASA logo
#		      title & various style features (including plot color)
#		      vertical profile title
# 		      png figure title
#		      tested downloads, new folders (download/images, download/data	
#		      link to database in download data abar
#      bug fixes: tooltips
#		  figure title (for zonal, global average, etc)
#		
# =====================
Download Instructions:
1. Download AmesWS Code from Github
        pip install git+https://github.com/vhartwick/AmesWS.git
        # ignore this for now, just download everything in the google drive

2. Go into Program Directory & Create a Virtual Environment
  
        cd /PATH/TO/DIRECTORY/amesWS
        conda env create -f environment.yml --name amesWS-env

3. Add one thing to env
	
	pip install importlib-metadata==4.13.0

4. Change the File Paths to Your Data

	vi utils/common_functions.py
        
        #change all file paths in def file_path (right now you only need to worry about the one copied below)
        # I recommend adding a Data directory to amesWS (shown below)      
	if vcords_input == "pstd" : # load atmos_average_pstd
       		f_path = '/PATH/TO/DATA/amesWS/Data/00668.atmos_average_pstd.nc'

5. Activate Virtual Environment
     
	conda activate amesWS-env

5. Run App
	
	python app.py

6. Go to Web Server: When the app is running, it will return the following text. Copy the http web address and 
   go to that site address.
	
	Dash is running on http://127.0.0.1:8050/

	 * Serving Flask app 'index'
	 * Debug mode: on
