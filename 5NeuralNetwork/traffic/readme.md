History of training the model:

0) In all models, the training setup is:  
 optimizer="adam"; loss="categorical_crossentropy"; metrics="accuracy"

1) Directly adopting the neural network structure used in mnist example
 #1 Convolutional layer. Learn 32 filters using a 3x3 kernel
 #2 Max-pooling layer, using 2x2 pool size
 #3 Flatten units
 #4 Hidden dense layer with 128 nodes with 0.5 dropout
 #5 Output layer with output units for all 10 digits
 # Result: loss: 3.1691 - accuracy: 0.1456
 # Only correct for 15% of the time!!

2) Adding another layer of convolutional and max-pooling 
 #1 Convolutional layer. Learn 32 filters using a 3x3 kernel
 #2 Max-pooling layer, using 2x2 pool size
 #3 Convolutional layer. Learn 32 filters using a 3x3 kernel
 #4 Max-pooling layer, using 2x2 pool size
 #5 Flatten units
 #6 Hidden dense layer with 128 nodes with 0.5 dropout
 #7 Output layer with output units for all 10 digits
 # Result: loss: 0.2030 - accuracy: 0.9453
 # The accuracy is 95% - just two more layers and we see a huge improvement! 

3) Adding just one layer of convolutional to (1) (or deleting 1 max-pooling layer from (2))
 #1 Convolutional layer. Learn 32 filters using a 3x3 kernel
 #2 Convolutional layer. Learn 32 filters using a 3x3 kernel
 #3 Max-pooling layer, using 2x2 pool size
 #4 Flatten units
 #5 Hidden dense layer with 128 nodes with 0.5 dropout
 #6 Output layer with output units for all 10 digits
 # loss: 0.0979 - accuracy: 0.9765
 # Two convolutional layers stacked together is even better than the conv-max-conv-max sequence.

4) Modifying the kernel size of the convolutional layers in the hope of improving accuracy
Version1:
 #1 Convolutional layer. Learn 32 filters using a 3x3 kernel
 #2 Convolutional layer. Learn 32 filters using a 5x5 kernel
 #3 Max-pooling layer, using 2x2 pool size
 #4 Flatten units
 #5 Hidden dense layer with 128 nodes with 0.5 dropout
 #6 Output layer with output units for all 10 digits
 # loss: 0.1706 - accuracy: 0.9657
Version2:
 #1 Convolutional layer. Learn 32 filters using a 5x5 kernel
 #2 Convolutional layer. Learn 32 filters using a 3x3 kernel
 #3 Max-pooling layer, using 2x2 pool size
 #4 Flatten units
 #5 Hidden dense layer with 128 nodes with 0.5 dropout
 #6 Output layer with output units for all 10 digits
 # accuracy: 0.7XXXX
 # I changed this be closer to the model in best model: https://benchmark.ini.rub.de/gtsrb_results.html.
 # But the results are worse.
 
5) Adding one more convolutional layer and one more max-pooling layer
 #1 Convolutional layer. Learn 32 filters using a 3x3 kernel
 #2 Convolutional layer. Learn 32 filters using a 3x3 kernel
 #3 Max-pooling layer, using 2x2 pool size
 #4 Convolutional layer. Learn 32 filters using a 3x3 kernel
 #5 Max-pooling layer, using 2x2 pool size
 #6 Flatten units
 #7 Hidden dense layer with 128 nodes with 0.5 dropout
 #8 Output layer with output units for all 10 digits
 # loss: 0.1000 - accuracy: 0.9769
 # Best performance so far. But on second run this is worse than 3) 
 
# Final decision: model 3) - a balance between model complexity and performance 



More details:
-----------------------------------------------------------------------------------------
Model 1
-------------------------------------------------------------------------------------------
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d_35 (Conv2D)           (None, 28, 28, 32)        896       
_________________________________________________________________
max_pooling2d_10 (MaxPooling (None, 14, 14, 32)        0         
_________________________________________________________________
flatten_6 (Flatten)          (None, 6272)              0         
_________________________________________________________________
dense_9 (Dense)              (None, 128)               802944    
_________________________________________________________________
dropout_5 (Dropout)          (None, 128)               0         
_________________________________________________________________
dense_10 (Dense)             (None, 43)                5547      
=================================================================
Total params: 809,387
Trainable params: 809,387
Non-trainable params: 0
_________________________________________________________________

Model 2
-------------------------------------------------------------------------------------------
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d_40 (Conv2D)           (None, 28, 28, 32)        896       
_________________________________________________________________
max_pooling2d_15 (MaxPooling (None, 14, 14, 32)        0         
_________________________________________________________________
conv2d_41 (Conv2D)           (None, 12, 12, 32)        9248      
_________________________________________________________________
max_pooling2d_16 (MaxPooling (None, 6, 6, 32)          0         
_________________________________________________________________
flatten_9 (Flatten)          (None, 1152)              0         
_________________________________________________________________
dense_15 (Dense)             (None, 128)               147584    
_________________________________________________________________
dropout_8 (Dropout)          (None, 128)               0         
_________________________________________________________________
dense_16 (Dense)             (None, 43)                5547      
=================================================================
Total params: 163,275
Trainable params: 163,275
Non-trainable params: 0
_________________________________________________________________

Model 3
-------------------------------------------------------------------------------------------
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d_42 (Conv2D)           (None, 28, 28, 32)        896       
_________________________________________________________________
conv2d_43 (Conv2D)           (None, 26, 26, 32)        9248      
_________________________________________________________________
max_pooling2d_17 (MaxPooling (None, 13, 13, 32)        0         
_________________________________________________________________
flatten_10 (Flatten)         (None, 5408)              0         
_________________________________________________________________
dense_17 (Dense)             (None, 128)               692352    
_________________________________________________________________
dropout_9 (Dropout)          (None, 128)               0         
_________________________________________________________________
dense_18 (Dense)             (None, 43)                5547      
=================================================================
Total params: 708,043
Trainable params: 708,043
Non-trainable params: 0
_________________________________________________________________

Model 4
-------------------------------------------------------------------------------------------
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d_48 (Conv2D)           (None, 28, 28, 32)        896       
_________________________________________________________________
conv2d_49 (Conv2D)           (None, 24, 24, 32)        25632     
_________________________________________________________________
max_pooling2d_20 (MaxPooling (None, 12, 12, 32)        0         
_________________________________________________________________
flatten_13 (Flatten)         (None, 4608)              0         
_________________________________________________________________
dense_23 (Dense)             (None, 128)               589952    
_________________________________________________________________
dropout_12 (Dropout)         (None, 128)               0         
_________________________________________________________________
dense_24 (Dense)             (None, 43)                5547      
=================================================================
Total params: 622,027
Trainable params: 622,027
Non-trainable params: 0
_________________________________________________________________

Model 5
-------------------------------------------------------------------------------------------
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d_50 (Conv2D)           (None, 28, 28, 32)        896       
_________________________________________________________________
conv2d_51 (Conv2D)           (None, 26, 26, 32)        9248      
_________________________________________________________________
max_pooling2d_21 (MaxPooling (None, 13, 13, 32)        0         
_________________________________________________________________
conv2d_52 (Conv2D)           (None, 11, 11, 32)        9248      
_________________________________________________________________
max_pooling2d_22 (MaxPooling (None, 5, 5, 32)          0         
_________________________________________________________________
flatten_14 (Flatten)         (None, 800)               0         
_________________________________________________________________
dense_25 (Dense)             (None, 128)               102528    
_________________________________________________________________
dropout_13 (Dropout)         (None, 128)               0         
_________________________________________________________________
dense_26 (Dense)             (None, 43)                5547      
=================================================================
Total params: 127,467
Trainable params: 127,467
Non-trainable params: 0
_________________________________________________________________