# =======================================================================
# Python Script to Modify var_data Dictionary in data_function.py
# Core Functionalities : Add & Remove Variables Based on User Input
# Author : Victoria Hartwick
# Last Modified : August 7, 2023
# =======================================================================

# Import Modules
import argparse
import ast
import re
import pandas as pd
import data_function as df

# Reference Dictionary
dref = {'plot-type':['2D_lon_lat', '2D_lat_lev', '2D_lon_lev', '2D_time_lat', '2D_time_lon', '2D_time_lev', '1D_time', '1D_lat', '1D_lon', '1D_lev','1D_diurn','1D_daily'],
    'dimx':['lon','lat','lon','time','time','time','time','lat','lon','lev','time_of_day_12','time'],
    'dimy': ['lat','lev','lev','lat','lon','lev','NaN','NaN','NaN','NaN','NaN','NaN'],

    'xaxis-name':['Longitude','Latitude','Longitude','Ls','Ls','Ls','Ls','Latitude','Longitude','Pressure','Local Time','Ls'],

    'yaxis-name':['Latitude','Pressure','Pressure','Latitude','Longitude','Pressure','NaN','NaN','NaN','NaN','NaN','NaN']}

# Load var_data
d = df.var_data()
d = d.to_dict(orient='list')

def main():

   # Argument Parser Setup
   parser = argparse.ArgumentParser(description='Add or remove variables from data_var dictionary in data_function.py\ndata_var is the main dictionary driver for the webserver and specifies the variables that can be accessed with each plot type and additional basic information, including the dimensions, variable name & unit, etc.\n',formatter_class=argparse.RawTextHelpFormatter)
   parser.add_argument("-r", "--remove",metavar="variable_name", help="Remove variable from data_var in data_function.py\n"
        "> USAGE: python database_gen.py -r ts\n") 
   parser.add_argument("-a", "--add", metavar="variable_name", help="Add variable from data_var in data_function.py\n"
        "> USAGE: python database_gen.py -a ts\n")           
    
   args = parser.parse_args()

   if args.remove:
      function_r(args.remove)
   elif args.add:
      function_a(args.add)
   else:
      print("No function specified")

# function to remove variable
def function_r(remove_var):
 
   # User Input
   #remove_var = input("What is the name (in FV3) of the variable you want to remove (e.g. ts): ")

   # Find the index positions of 'ts' in the 'variable' key
   indices_to_remove = [i for i, x in enumerate(d['variable']) if x == remove_var]

   # Create a new dictionary without 'ts' and its associated values in other keys
   new_dict = {}
   for key, values in d.items():
      new_dict[key] = [value for i, value in enumerate(values) if i not in indices_to_remove]

   # Replace var_data dictionary with new dictionary & save old version
   
   # Open and read the data_function.py file
   file_path = 'data_function.py'
   with open(file_path, 'r') as file:
      content = file.read()

   # Save a Copy
   copy_filename = 'data_function.sav'
   with open(copy_filename, 'w') as copy_file:
      copy_file.write(content)

   # Find the dictionary definition in the file using regular expressions
   pattern = r'def var_data\(\):(?:\n|.)*?d\s*=\s*\{(?:[^}]|\n)*\}'
   match = re.search(pattern, content, re.DOTALL)

   if match:
      # Replace the dictionary definition in the content with the new dictionary
      new_content = content[:match.start()] + f"def var_data():\n   d = {new_dict}" + content[match.end():]
   
   # Write the updated content back to the file
   with open(file_path, 'w') as file:
      file.write(new_content) 


# function to add variable
def function_a(variable_name):

   # User Inputs
   #variable_name = input("What is the name (in FV3) of the new variable (e.g. ts): ")


   # First Check if Variable Is Already in Dictionary
   if variable_name in d['variable']:
      print(f"The variable '{variable_name}' is already in the dictionary.")
      exit()  # Exit the program


   # If variable doesn't exist ask some more questions
   variable_unit = input("What is the unit of the new variable (e.g. K): ")
   variable_label = input("What is the long name of the new variable (e.g. Surface Temperature): ")
   hvar_name = input("What variable would you like to use for the vertical profile plot (e.g. temp): ")
   variable_cmap = input("For a contour map, what is your preferred color map (e.g. Oryel): ")
   new_plot_type = input("List all Plot Types that Can use this new variable: (e.g. FOR VARIABLES WITH VERTICAL DIMENSION - '2D_lon_lat', '2D_lat_lev', '2D_lon_lev', '2D_time_lat', '2D_time_lon', '2D_time_lev', '1D_time', '1D_lat', '1D_lon', '1D_lev' , or FOR VARIABLES WITH NO VERICAL DIMENSION - '2D_lon_lat','2D_time_lat','2D_time_lon','1D_time','1D_lat','1D_lon', ADDITIONAL PLOT TYPES - '1D_diurn', '1D_daily'):  ")

   # Define Elements of Each dictionary Key
   # ast.literal_eval takes user input (str) and breaks apart into array of elements
   # size/length depends on number of plots that variable can be used in, based on this
   # generate variable name, unit, label, hover, cmap, dimx, dimy, xasix_name, yaxis_name
   new_plot_type_test =  ast.literal_eval(f"[{new_plot_type}]")
   new_variable =  ast.literal_eval(f"'{variable_name}', " * len(new_plot_type_test))
   new_unit  =  ast.literal_eval(f"'[{variable_unit}]', " * len(new_plot_type_test))
   new_label = ast.literal_eval(f"'{variable_label} [{variable_unit}]', " * len(new_plot_type_test))
   new_hover2 = ast.literal_eval(f"['lev','{hvar_name}'], " * len(new_plot_type_test))
   new_cmap = ast.literal_eval(f"'{variable_cmap}', " * len(new_plot_type_test))

   # Using reference dictionary (dref) find dimx, dimy for each plot type
   new_dimx =  [dref['dimx'][dref['plot-type'].index(ptype)] for ptype in new_plot_type_test]
   new_dimy =  [dref['dimy'][dref['plot-type'].index(ptype)] for ptype in new_plot_type_test]
   new_xaxis_name =  [dref['xaxis-name'][dref['plot-type'].index(ptype)] for ptype in new_plot_type_test]
   new_yaxis_name =  [dref['yaxis-name'][dref['plot-type'].index(ptype)] for ptype in new_plot_type_test]

   # Add New Elements to Old Data Array
   # Append the d dictionary with the new lists
   d['variable'] += new_variable
   d['unit'] += new_unit
   d['plot-type'] += new_plot_type_test 
   d['label'] += new_label
   d['dimx']+= new_dimx
   d['dimy']+= new_dimy
   d['xaxis_name']+= new_xaxis_name
   d['yaxis_name']+= new_yaxis_name
   d['hover2'] += new_hover2
   d['cmap'] += new_cmap
 
   # Replace var_data dictionary with new dictionary & save old version
   # Open and read the data_function.py file
   file_path = 'data_function.py'
   with open(file_path, 'r') as file:
      content = file.read()

   # Save a Copy
   copy_filename = 'data_function.sav'
   with open(copy_filename, 'w') as copy_file:
      copy_file.write(content)

   # Find the dictionary definition in the file using regular expressions
   pattern = r'def var_data\(\):(?:\n|.)*?d\s*=\s*\{(?:[^}]|\n)*\}'
   match = re.search(pattern, content, re.DOTALL)

   if match:
      # Replace the dictionary definition in the content with the new dictionary
      new_content = content[:match.start()] + f"def var_data():\n   d = {d}" + content[match.end():]

   # Write the updated content back to the file
   with open(file_path, 'w') as file:
      file.write(new_content)

if __name__ == "__main__":
    main()



