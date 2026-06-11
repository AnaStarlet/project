# Container With Most Water

You are given an integer array height of length n.  
There are n vertical lines drawn such that the two endpoints of the i-th line are (i, 0) and (i, height[i]).  
Find two lines that together with the x-axis form a container, such that the container contains the most water.  
Return the maximum amount of water a container can store.  
Notice that you may not slant the container.

## Example

**Input:** height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

**Calculation:**

- Choose index 1 (height 8) and index 8 (height 7)
- Minimum height = min(8, 7) = 7
- Width = 8 - 1 = 7
- Area = 7 × 7 = 49

**Output:** 49

**Explanation:** The vertical lines are represented by array [1, 8, 6, 2, 5, 4, 8, 3, 7].  
In this case, the maximum area the container can contain is 49.
