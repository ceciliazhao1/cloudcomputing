# Movie Recommendation system


**[Movie Recommendation system Google Slides](https://docs.google.com/presentation/d/1EK3W5Z6-JsIT54kWeN4PkH5EE4x0bGdsXbtAG0JlYpo/edit#slide=id.p)**


## Introduction

Recommender System is an information filtering tool that seeks to predict which product a user will like, and based on that, recommends a few products to the users. 

The two widely used approaches for building a recommender System are:

* content-based filtering (CBF)
* collaborative filtering (CF)

![My Image](./image/Recommendation_System.png)


## Design

Recommendation using Alternating Least Squares (ALS)
The general approach is iterative. During each iteration, one of the factor matrices is held constant, while the other is solved for using least squares. 

* Modify the provided code and implement on Google Colab 
* Download the file from Google Colab and test on Google Cloud Platform

## Implementation

### Google Colab

**[Detailed steps of execute on Google Colab](https://github.com/ceciliazhao1/cloudcomputing/blob/main/machine%20learning/Movie%20Recommendation%20System/implementation3/Recommendation_Engine_MovieLens.ipynb)**

## Test

### Google Cloud Platform

* Download .py file from Colab

* Create instance on GCP and open VM through SSH

* Upload .txt data files and .py source file to GCP

![My Image](./image/upload.png)

* 


* Install pyspark:
```
sudo apt install python3-pip
sudo pip3 install pyspark
pyspark --version
```

* Install java
```
java -version
sudo apt install openjdk-8-jre-headless  
sudo update-alternatives 
export JAVA_HOME=/path/to/java/installation/directory
source ~/.bashrc 
echo $JAVA_HOME
```
![My Image](./image/pandas.png)

* Install pandas
```
sudo -H pip3 install pandas
```

*  Execute .py source code

```
$ python3 movie_recommendation_GCP.py
```

![My Image](./image/1.png)
![My Image](./image/2.png)
![My Image](./image/3.png)
![My Image](./image/4.png)



## Enhancement

How to make the result more reliable and the training speed faster?

## Conclusion

The result run in Google Colab is verified in GCP with no problem. However, the training time on both platforms are really long. With this project there are only less than 20,000 data in dataset. Training data will be heavier with heavier datasets. 


## References

Nair, S. (2020, August 10). PySpark Recommender System with ALS. Towards Data Science. Retrieved November 16, 2022, from https://towardsdatascience.com/build-recommendation-system-with-pyspark-using-alternating-least-squares-als-matrix-factorisation-ebe1ad2e7679 
