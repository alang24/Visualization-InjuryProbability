# Injury-Visualization
While at the Center for Applied Biomechanics, I had written a MATLAB script that produced injury visualizations on the human body for various FEA crash simulations. The script was slow and felt hard-coded, and I wanted to adapt the script using Python. The result was that I was able to familiarize myself with Pandas, numpy, and Pillow while creating a faster and easier to use alternative. 

**Performance comparison:**
- MATLAB runtime: 1.0625 seconds per image
- Python runtime: 0.1708 seconds per image

**Projects**
- HMC 2019
- HMC 2020


**Dependencies:**
- PANDAS library: https://pypi.org/project/pandas/
- Pillow: https://pypi.org/project/Pillow/

**Updates:**
- 7/12: Uploaded base code. Script combines coord/simulationdata and recognizes the four cases.
- 7/18: Script now uses Pillow to draw circles/ellipses onto image based on coordinates. Verification of the linkTable.py method (still need to check case 3 and 4)
- 7/26: Completed exceptions and verified cases 3 and 4. Script now adds list of five highest probabilities and a title to image. Partially complete on automation through entire spreadsheet and fixed bug involving RGB tuples
- 7/31: processes the different cases (guardrail,medstrip,etc.). for each case, able to loop through all the sheets and create an image, verified correctness <br />
- 8/1: Verified correctness of entire script. Added function documentation. Added helper functions to clean up the main.py file.
- 10/2: New simulations (task 5) that are similar to RoadsideTree
- 10/16: Added car models to image names, restructured directories, cleaned code, fixed an error regarding OverCenterline
- 10/23: Separated head metrics into two (BrIC MPS and HIC36), added documentation, ran on 2020 results that finished so far
- 11/4: adjusted head metrics shape, re-ran on all

Things to do: wait for more of those results, potentially add more information on bottom left of image?
