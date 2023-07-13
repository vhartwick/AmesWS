# =====================
# AmesWS
# Web Server Application for Ames FV3 Mars Climate Model Data Access & Visualization
# =====================
Download Instructions:
1. Download AmesWS Code from Github
```
        git clone https://github.com/vhartwick/AmesWS.git
```
2. Go into Program Directory & Create a Virtual Environment
``` 
        cd /PATH/TO/DIRECTORY/amesWS
        conda env create -f environment.yml --name amesWS-env
         
          OR

        python -m venv amesWS-env
        source ameWS-env/bin/activate
        pip install -r requirements.txt

```

3. Activate Virtual Environment
```     
	conda activate amesWS-env
```
4. Create a Local Data Directory & Download Data from NAS 
```
        mkdir amesWS/Data/sim1
        Sample Data Files are located in a shared directory on NAS
        /u/mkahre/MCMC/tmp/4victoria/C48_L30_MY34/
```
4. Change the File Paths to Your Data
```
	vi utils/common_functions.py 
        **change all file paths in def file_path (right now you only need to worry about the one copied below)
	if vcords_input == "pstd" : # load atmos_average_pstd
       		f_path = f'/PATH/TO/DATA/amesWS/Data/{model_input}/00668.atmos_average_pstd.nc'
```
5. Run App
```  	
	python app.py
```

6. Go to Web Server: When the app is running, it will return the following text. Copy the http web address and 
   go to that site address.

```	
	Dash is running on http://127.0.0.1:8050/

	 * Serving Flask app 'index'
	 * Debug mode: on
```
