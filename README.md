# LSBMP-L2RRT
Reproducing the paper 'Robot Motion Planning In Learned Latest Spaces'

## TODO (in no particular order)
- Training Follow ups:
  - <s>Data Sanity checks</s>
    - I noticed that the difference between the data for empty image and image with the robot is only one cell (one value in the entire array) in our data set whereas it's about 15-16 in their data set. So I increased the robot half length and generated a new data set.
  - <s>Check the latent dimension values</s>
    - The latent dimension turns out to be of a very low magnitude (of the order 10^-5) whereas theirs is in between 0 and 1. This is also the reason for almost negligible L2 loss and Grammian loss after training a few epochs.
  - <s>Check their reconstruction quality</s>
    - Thier reconstruction is relatively better looking than ours. Also their MSE on a test sample is below 25 whereas the best we got so far is above 150.
  - Run my network with their sample data.
  - Cross check the spatial arg max implementations on both sides.