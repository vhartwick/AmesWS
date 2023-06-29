# =====================
# AmesWS
# Web Server Application for Ames FV3 Mars Climate Model Data Access & Visualization
# =====================
Download Instructions:
1. Download AmesWS Code from Github
```
        git clone git+https://github.com/vhartwick/AmesWS.git
```
2. Go into Program Directory & Create a Virtual Environment
``` 
        cd /PATH/TO/DIRECTORY/amesWS
        conda env create -f environment.yml --name amesWS-env
```

3. Activate Virtual Environment
```     
	conda activate amesWS-env
```
4. Add one thing to env
```	
	pip install importlib-metadata==4.13.0
```     
5. Change the File Paths to Your Data
```
	vi utils/common_functions.py 
        **change all file paths in def file_path (right now you only need to worry about the one copied below)
        I recommend adding a Data directory to amesWS (shown below)**      
	if vcords_input == "pstd" : # load atmos_average_pstd
       		f_path = '/PATH/TO/DATA/amesWS/Data/00668.atmos_average_pstd.nc'
```
6. Run App
```  	
	python app.py
```

7. Go to Web Server: When the app is running, it will return the following text. Copy the http web address and 
   go to that site address.

```	
	Dash is running on http://127.0.0.1:8050/

	 * Serving Flask app 'index'
	 * Debug mode: on
```
