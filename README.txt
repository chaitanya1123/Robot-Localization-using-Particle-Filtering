README

---Files included---:
Code   : particleFilter.py
	 mapParser.py
	 logParser.py
	 gridFunctions.py
         measurementModel.py
	 motionModel.py
	 resample.py

Data   : log data,map data
Output : GIF file (showing localization), .txt files (output variables)
Readme file: README.txt 

---Implementation---:
We have implemented Robot Localization using Particle filtering in python using the provided data. Files 'wean.dat' and 'robotdata' are 
used to parse the map, odometry and laser readings. Particles are generated using random gaussian distribution. Odometry data is used for 
the motion model and log data for the sensor model. Resampling is carried out using low variance sampling. After implementing this particle 
filter algorithm, all the particles localize to a particular location, thus indicating the best estimate true pose of the robot.


---How to run--- :
Run the file particleFilter.py with default arguments.
To run the algorithm for different robot log data -  Open logParser.py
						     Choose the robotdata from the log data file and add to the filepath.
								 

