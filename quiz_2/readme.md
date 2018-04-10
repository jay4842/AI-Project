# Quiz 2
Currently working on setting up the problem, and understanding the problem as well.  

## Cryptarithmetic Problem 
Given a mathematical equation among unknown numbers, whose  
digits are represented by letters. The goal is to identify the value of  
each letter.  

### Forward checking algorithm
- Whenever a variable X is assigned, check all variables Y  
connected to X by a constraint.  
- Delete from Y’s domain any value that is inconsistent with the  
value chosen for X.  
- Backtrack if the domain of any variable becomes empty.  

### MRV and LCV
##### MRV or *Minimum Remaining Values*
- Choose a variable with the fewest possible values.   
  -   Assign most constrained variable first.  
  
##### LCV or *Least Constraining Values*
- Choose a value that rules out the fewest values in the remaining
variables.  
  - Assign values that leave maximal flexibility for the remaining
variables.  


## The Problem! 
DORALD + GERALD = ROBERT  

