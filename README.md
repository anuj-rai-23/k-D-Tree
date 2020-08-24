# k-Dimensional Tree
An implementation of k-dimensional tree for storage, management (insert/search/delete) and range query for multi-dimensional numerical data.</br>
Project done under supervision of [Dr. Vishwanath Gunturi](http://cse.iitrpr.ac.in/~gunturi/)

## Supported Operations
<ul>
  <li>Bulk loading from a text file</li>
  <li>Visualization of current tree</li>
  <li>Insertion</li>
  <li>Deleton</li>
  <li>Range Query</li>
  </ul>
Initially, data is bulk-loaded from "Dataset.txt" that has ID, col1, col2 . . . . coln.</br>
Then, insertion/deletion/visualization can be performed.</br>
At each level, existing points are split into two parts along the dimension with maximum difference in two extreme points.</br>
Each node stores the location of its split axis/ parent/ children along with data point.</br>
Range Query involves finding points that lie inside rectangle whose two extreme ends are given as input.

*Results of range query are as given in [Observation Report](/KDTreeObservatiponReport.pdf)*
