
def lat_lon(f,var,lon_input,lat_input,areo_input,vcords_input,lev_input):

   # COLLAPSE VAR(S) BASED ON INPUTS: LEV,LAT,LON,AREO
   # FOR 4D VARIABLES
   if len(f[var].dims) == 4:   # find out if variable has a vertical axis

         # IF ALL LAT & LON
         if lon_input == 'ALL' and lat_input=="ALL":
            dim1 = f.lon
            dim2 = f.lat

            # IF ALL AREO
            if areo_input == "ALL":
               var = f[var].sel(**{vcords_input:int(lev_input)},method='nearest').mean('time')
            elif len(areo_input)<4:
               areo_input = areo_input
               var = f[var].sel(**{vcords_input:int(lev_input)},time=int(areo_input),method='nearest')
            elif len(areo_input)<4:
               var = f[var].sel(**{vcords_input:int(lev_input)},time=int(areo_input),method='nearest')
            else:
               areo_split = str(areo_input).split(",")
               var = f[var].sel(**{vcords_input:int(lev_input)},method='nearest').sel(time=slice(areo_input))

         # SPECIFIED LAT RANGE, ALL LON
         elif lon_input == "ALL" and lat_input != "ALL":
            lat_split = str(lat_input).split(",")
            dim1 = f.lon
            dim2 = f.lat.sel(lat=slice(lat_split[0],lat_split[1]))

            # IF ALL AREO
            if areo_input == 'ALL':
               var = f[var].sel(**{vcords_input:int(lev_input)},method='nearest').sel(lat=slice(lat_split[0],lat_split[1])).mean('time')
            elif len(areo_input)<4:
                var = f[var].sel(**{vcords_input:int(lev_input)},time=int(areo_input),method='nearest').sel(lat=slice(int(lat_split[0]),int(lat_split[1])))
            else:
               areo_input = areo_input
               var = f[var].sel(**{vcords_input:int(lev_input)},time=int(areo_input),method='nearest').sel(lat=slice(lat_split[0],lat_split[1]))

         # SPECIFIED LON RANGE, ALL LAT
         elif lat_input == "ALL" and lon_input != "ALL":
            lon_split = str(lon_input).split(",")
            dim1 = f.lon.sel(lon=slice(lon_split[0],lon_split[1]))
            dim2 = f.lat

            # IF ALL AREO
            if areo_input == 'ALL':
               var = f[var].sel(**{vcords_input:int(lev_input)},method='nearest').sel(lon=slice(lon_split[0],lon_split[1])).mean('time')
            elif len(areo_input)<4:
               var = f[var].sel(**{vcords_input:int(lev_inputt)},time=int(areo_input),method='nearest').sel(lon=slice(int(lon_split[0]),int(lon_split[1])))
            else:
               areo_input = areo_input
               var = f[var].sel(**{vcords_input:int(lev_input)},time=int(areo_input),method='nearest').sel(lon=slice(lon_split[0],lon_split[1]))
         
         # SPECIFIED LAT & LON RANGES
         else:
            lon_split = str(lon_input).split(",")
            lat_split = str(lat_input).split(",")
            dim1 = f.lon.sel(lon=slice(lon_split[0],lon_split[1]))
            dim2 = f.lat.sel(lat=slice(lat_split[0],lat_split[1]))

            # IF ALL AREO
            if areo_input == 'ALL':
               var = f[var].sel(**{vcords_input:int(lev_input)},method='nearest').sel(lon=slice(lon_split[0],lon_split[1]),lat=slice(lat_split[0],lat_split[1])).mean('time')
            elif len(areo_input)<4:
               var = f[var].sel(**{vcords_input:(lev_input)},time=int(areo_input),method='nearest').sel(lon=slice(int(lon_split[0]),int(lon_split[1])),lat=slice(int(lat_split[0]),int(lat_split[1])))

            else:
               areo_input = areo_input
               var = f[var].sel(**{vcords_input:int(lev_input)},time=int(areo_input),method='nearest').sel(lon=slice(lon_split[0],lon_split[1]),lat=slice(lat_split[0],lat_split[1]))

   # FOR 3D VARIABLES 
   else:

      # ALL LAT/LON 
      if lon_input == 'ALL' and lat_input=="ALL":
         dim1,dim2 = f.lon,f.lat

         # ALL AREO - WORKS
         if areo_input == 'ALL':
            var = f[var].mean('time')
         elif len(areo_input) < 4:
            var = f[var].sel(time=int(areo_input),method='nearest')
         else:
            areo_split = str(areo_input).split(",")
            var = f[var].sel(time=slice(int(areo_split[0]),int(areo_split[1]))).mean('time')

      # ALL LON, SPECIFIED LAT
      elif lon_input == "ALL" and lat_input != "ALL":
         lat_split = str(lat_input).split(",")
         dim1 = f.lon
         dim2 = f.lat.sel(lat=slice(int(lat_split[0]),int(lat_split[1])))

         # ALL AREO - WORKS
         if areo_input == 'ALL': 
            var = f[var].sel(lat=slice(int(lat_split[0]),int(lat_split[1]))).mean('time')
         elif len(areo_input)<4:
            var = f[var].sel(time=int(areo_input),method='nearest').sel(lat=slice(int(lat_split[0]),int(lat_split[1])))

         else:
            areo_split = str(areo_input).split(",")
            var = f[var].sel(time=slice(areo_split[0],areo_split[1]),lat=slice(int(lat_split[0]),int(lat_split[1]))).mean('time')

      # ALL LAT, SPECIFIED LON
      elif lon_input != "ALL" and lat_input == "ALL":
         lon_split = str(lon_input).split(",")
         dim1 = f.lon.sel(lon=slice(int(lon_split[0]),int(lon_split[1])))
         dim2 = f.lat

         # ALL AREO 
         if areo_input == 'ALL': 
            var1 = f[var].sel(lon=slice(int(lon_split[0]),int(lon_split[1]))).mean('time')
         elif len(areo_input)<4:
             var = f[var].sel(time=int(areo_input),method='nearest').sel(lon=slice(int(lon_split[0]),int(lon_split[1])))
         else:
             areo_split = str(areo_input).split(",")
             var = f[var].sel(time=slice(areo_split[0],areo_split[1]),lon=slice(int(lon_split[0]),int(lon_split[1]))).mean('time')

      # SPECIFIED LON & LAT
      else:  # lon_input, lat_input != "ALL"
         lat_split,lon_split = str(lat_input).split(","),str(lon_input).split(",")
         dim1 = f.lon.sel(lon=slice(int(lon_split[0]),int(lon_split[1])))
         dim2 = f.lat.sel(lat=slice(int(lat_split[0]),int(lat_split[1])))

         # ALL AREO 
         if areo_input == 'ALL':
            var = f[var].sel(lon=slice(int(lon_split[0]),int(lon_split[1])),lat=slice(int(lat_split[0]),int(lat_split[1]))).mean('time')
         elif len(areo_input)<4:
            var = f[var].sel(time=int(areo_input),method='nearest').sel(lon=slice(int(lon_split[0]),int(lon_split[1])),lat=slice(int(lat_split[0]),int(lat_split[1])))
         else:
            areo_split = str(areo_input).split(",")
            var = f[var].sel(time=slice(areo_split[0],areo_split[1]),lon=slice(int(lon_split[0]),int(lon_split[1])),lat=slice(int(lat_split[0]),int(lat_split[1]))).mean('time')

   return dim1, dim2, var
