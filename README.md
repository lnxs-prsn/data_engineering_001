WeatherApp A

data engineering pipeline that fetches data from 

requests from fmi wfs endpoint Helsinki area weather forecast 
parses data, cleans and organizes data 
creates postgres table and stores data to two tables 
raw_forecast and current_forecast
current_forecast does not allow duplicate data and raw_forecast allows duplicate data
reason for this arrangement is to be able to recover from human or api errors 



PROJECT IS DIVIDED TO 3 SECTIONS 

1. preproject
   1. here I have stored 
      1. failures, discarded solutions paths, initial successes that were refined later
2. working project 
   1. here are stored the different files that the main.py turns to working project
   2. this is just mvp at the moment there is lots of hardcoding but due to time limit its left as it is.
3. post_project
   1. here is honest reflection about the project


