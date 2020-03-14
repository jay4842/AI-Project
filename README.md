# AI-Project
[GitHub](https://github.com/jay4842/AI-Project)  
Code is under *genetic_boy*.  
  
[Paper Link](https://www.overleaf.com/read/pcgwmrpzyqjd)    
- Please see this for detailed information about the project.
  
## N Queens Problem
The N Queens Problem is a classical intractable problem, which is often used in case of discussing about various types of searching problems. The objective is to place N number of queens on an N by N sized chess board in a way that none of the queens can capture one another. Therefore three constraints arise in this problem which are the following; the queens cannot be in the same, row, column, or diagonal. Random boards, or states, are generated with the queens randomly placed on the board. With this, the algorithm will perform calculations that will determine when a board has reached its goal state, and keep track of the number of goal states that have been reached.

## A genetic Approach
The requirement for this research is first to apply a modified genetic algoritm. The genetic algorithm is based on parent states producing child states. The original method consists of, selecting two parents at random from a population. Then preforming a crossover operation or having the two states reproduce a child state. This is done by taking half of the first parent and another half of the second parent and combining the two. Then there is a chance that the child can be mutated. Once the child is created then the child is added to the rest of the population. This loop continues until a solution is found.
  
A type of N queens problem implementation where we have modified how child states are added to the population. Along with what mutation operations are preformed as well as when they are preformed.

## Conclusion
The genetic algorithm is an algorithm that can be used to solve constraint problems. The N queens problem does fall under the number of problems that can be solved with this algorithm. This being said the random component is a major area of the genetic algorithm that can hinder the success of it. The way that we combated that issue was using the fitness function to reduce the complete randomness. Additionally keeping the population at a constant rate also proved a good approach to reducing the amount of memory that is consumed while the algorithm is running.
