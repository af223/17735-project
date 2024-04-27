# Anomaly Detection & Employee Privacy

As part of a project for 17-735: Engineering Privacy in Software, this repo creates three different versions of an isolation forest ML model trained to detect anomalies on employee data. 

### Contributors
Aimee Feng [(af223)](https://github.com/af223), Bhavesh Dhake [(wickywanka)](https://github.com/wickywanka), Prachi Doshi [(PrachiDoshi2170)](https://github.com/PrachiDoshi2170)

## Details

Our goal is to investigate different approaches towards creating a model for detecting insider threats based on employee data while preserving employee privacy through epsilon-differential privacy. We use the Insider Threat Test Dataset released by CMU [here](https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247?file=24857825). For the purpose of carrying out exploration of privacy-preserving methods in anomaly detection, we decided to use the version 1 (r1) dataset as this was sufficiently enough data to train and test our models on. In addition, we acknowledge that there are known issues with this dataset, such as the dataset not accounting for holidays, however later versions of the dataset that address these issues contain too much data to reasonably work with for the scope of our project. The layout of the later dataset versions are similar, if not the same, format as r1, so we can easily extend our project to train and test our ML models on these later-versioned large dataset.

Current research shows that ML models built using isolation forests are one of the most commonly used anomaly detection algorithms. Running the model on a datapoint will produce an anomaly score, which is then interpreted to represent whether the datapoint is considered an outlier or anomaly. In addition, two common methods to introduce differential privacy into the process is either to train the model on an epsilon-DP dataset or to train the model in a differential privacy preserving way. 

Thus, this project contains three implementations of an ML model trained to detect anomalies in employee activity through logs:

### 1. Isolation Forest ML model implemented with sci-kit learn

1. This model doesn't preserve employee privacy in any way. We chose to use sklearn as it's an open-source library that's one of the most commonly used Python libraries containing ML model implementations.

2. Of note, sklearn implements isolation model anomaly score differently than in the [paper](https://ieeexplore.ieee.org/document/4781136) that first presented the isolation forest. Specifically, sklearn computes the anomaly score to be the equivalent of 0.5 minus the anomaly score calculated by the original paper's presentation.

3. A negative anomaly score is classified as potentially an anomly. After analyzing the distribution of anomaly scores for the dataset, we was observed that a threshold of -0.04 provides a reasonable separation between normal instances and true anomalies.

### 2. Isolation Forest ML model implemented with diffprivlib

1. This model preserves epsilon-DP by training the model in such a way that preserves epsilon-DP on the underlying dataset by accounting for differential privacy when sampling the data to build the model. Notably, the data on which the model is being trained is still the raw data itself that hasn't been processed or obscured in any way.

2. We chose diffprivlib as we found that this was a relatively well-supported open-source Python library that implements differentially private ML models. However, diffprivlib does not yet support isolation forests. To address this, we viewed the sklearn implementation of the isolation forest and diffprivlib's implementation of other ML model types that preserve differential privacy to draw inspiration on how to implement the isolation forest model such that training it on raw data would still preserve differential privacy of the employee data.

### 3. Isolation Forest ML model trained over differentially private dataset

1. This model preserves epsilon-DP by training the model on a dataset that is epsilon-DP.

2. As we deal primarily with non-numerical data in the dataset, we derived a differentially-private dataset from r1 using the Laplace function. We then trained the isolation forest model from sklearn on this new dataset. Due to the different format of this data input than in methods 1 and 2, we analyzed the results from this model differently. Specifically, our testing datapoints also had to transformed into this new format so we could only retrieve the anomaly count and score for users, but could not retrieve any specific detail such as logon/logoff activity as in methods 1 and 2 above since this data has been obscured.

## Setup & Usage

Download and unzip the r1 CMU Insider Threat Test Dataset from (here)[https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247?file=24857825] in the same directory as where this repo has been cloned.

To generate the preprocessed data from methods (1) and (2) from above, execute the following command:

```
python3 preprocess.py
```

To train and test the isolation forest ML model implemented with sci-kit learn, inside of the file ``detection_v1.ipynb`` select Python3.7 as the kernel and run all cells.

To train and test the isolation forest ML model implemented with diffprivlib, inside of the file ``detection_v2.ipynb`` select Python3.7 as the kernel and run all cells.

To train and test the isolation forest ML model trained over differentially private dataset, inside of the file ``epsilon_datasset.ipynb`` select Python3.7 as the kernel and run all cells.

These notebooks will produce graphs within the output that visulaize the results of the testing the model. 


### Challenges & Next Steps

We would like to add the disclaimer that our implementation of the isolation forest using diffprivlib has minimal functionality. This was difficult as we had very little time to dive deeply into all parts of the diffprivlib library. However, we accept its correctness based on preliminary results, as running with higher values of epsilon (e.g. 50, 60, ...) roughly matches the results from the sklearn isolation forest model.

The next steps from here include:
* Training and testing on much larger datasets (e.g. r3 or r4 from the CMU Insider Threat Test Dataset)
* Expanding and further testing on the isolation forest implementation using diffprivlib
* Work towards making our models compliant with industry privacy standards and other requirements

## References

The CMU Insider Threat Test Dataset can be found here: [https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247?file=24857825]

Sci-kit learn:

diffprivlib:

isolation forest paper:
