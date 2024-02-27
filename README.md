# ASE_Homeworks_Grp13
# Homeworks

# About
Homework repository for **CSC 591 021 Group-13**<br/>
- HW2 - Conversion of <a href="https://github.com/timm/lo/blob/main/docs/gatecode.pdf">script.lua</a> to Python, including the test cases.
- HW3 - Implementing Task 1, 2, 3 and 4 as per <a href="https://github.com/txt/aa24/blob/main/docs/hw03.md">script.lua</a>, including the test cases.
  
# Steps to run
- HW 2:
  1. Install Python 3.10.6
  2. cd into src folder of homework and run ```python -m gate -f .\auto93.csv -t stats```.
     
- HW 3:
  1. Install Python 3.10.6
  2. cd into hw03/src folder of homework and run - 
   <br /> ```python -m gate -f .\diabetes.csv -t csv_ascii```
   <br /> OR
   <br /> ```python -m gate -f .\soybean.csv -t csv_ascii``` -> For Task 1
   <br /> ```python .\gate.py -f .\diabetes.csv -t km_feature```
   <br /> OR
   <br /> ```python .\gate.py -f .\soybean.csv -t km_feature``` -> For remaining tasks
   <br /> To run all testcases
   <br /> ```python .\gate.py -f .\auto93.csv -t all```

- HW 4:
  1. Install Python 3.10.6
  2. cd into src folder of homework and run ```python -m gate -f .\auto93.csv -t gate```.
 
  Questions:
  1. Yes.
     One line from most: 3. most: [2160.0, 14.5, 40.0]
     One line from rand: 4: rand:[3387.54, 15.88, 20.0]
     Almost comparable accelerations but wins in Lbs and Mpg
  2. One per row, 398. "sort ROWS on "distance to heaven" ", sorts all rows
  3. It provides a good approximate value, and usually provides answers that maximize one value over others. Sometimes does provide a value that isn't great, but overall is much better than random selection.
  Examples:
    3. most: [3360.0, 16.6, 20.0]
    3. most: [3651.0, 17.7, 20.0]
    3. most: [3632.0, 18.0, 20.0]
    3. most: [2671.0, 13.5, 30.0]
    3. most: [2164.0, 22.1, 20.0]
    3. most: [2815.0, 14.5, 20.0]
    3. most: [2711.0, 15.5, 30.0]
    3. most: [3302.0, 15.5, 20.0]
    3. most: [3353.0, 14.5, 20.0]
    3. most: [2350.0, 16.8, 30.0]
   It tries to keep Mpg around 20-30, acceleration over/around 15 and then minimize Lbs, none above 4000 especially.
   
-HW5:
  1. Install Python 3.10.6
  2. cd into src folder of homework and run ```python -m gate -f .\auto93.csv -t far```.
  3. cd into src folder of homework and run ```python -m gate -f .\auto93.csv -t distance```.

-HW6:
  1. Install Python 3.10.6
  2. cd into src folder of homework and run ```$ python -m gate -f .\auto93.csv -t compare```.


# Team Members
 - Rhythm Jagota
 - Ankit Garg
 - Alex Taylor
    
