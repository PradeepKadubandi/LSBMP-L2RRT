# LSBMP-L2RRT
Reproducing the paper 'Robot Motion Planning In Learned Latest Spaces'

## TODO (in no particular order)
- Need to implement train/test data generation code for visual planning problem
- Need to implement spatial softmax in pytorch
- Need to fix the loss function for collision network
- For now copied the code for RRT almost as is from the source except for calling the pytorch network implementation. Need to perhaps modularize this code later.
- Sanity checks on the entire code (like making sure it runs without errors and perhaps also making sure the structure does not have bugs)
- Training the networks
- Testing the networks and plots