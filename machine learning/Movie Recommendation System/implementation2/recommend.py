from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

if __name__ == "__main__":
    sc = SparkContext(appName="PythonCollaborativeFilteringExample")

    # Load and parse the data
    data = sc.textFile("formatted_u.data")

    # Each line is 
    ratings = data.map(lambda l: l.split(',')).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))

    # Build the recommendation model using ALS
    # - rank: number of features to use
    rank = 10

    # - iterattions: number of iterations of ALS (recommended: 10-20)
    numIterations = 10

    # The default ALS.train() method which assumes ratings are explicit.
    # - Train a matrix factorization model given an RDD of ratings given by 
    #   users to some products, in the form of (userID, productID, rating) pairs. 
    # - We approximate the ratings matrix as the product of two lower-rank 
    #   matrices of a given rank (number of features). 
    #   + To solve for these features, we run a given number of 
    #     iterations of ALS. 
    #   + The level of parallelism is determined automatically based 
    #     on the number of partitions in ratings.  
    model = ALS.train(ratings, rank, numIterations)

    #####################################################
    # Evaluate the model on training data
    # - Evaluate the recommendation model on rating training data
    ############################################################
    testdata = ratings.map(lambda p: (p[0], p[1]))
    predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))

    # Join input rating with predicted rating
    ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
    MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
    print("Mean Squared Error = " + str(MSE))

    # Persist the user and product factors in memory to avoid slow predictions
    model.userFeatures().persist()
    model.productFeatures().persist()

    # Save and load model
    model.save(sc, "myCollaborativeFilter")
    sameModel = MatrixFactorizationModel.load(sc, "myCollaborativeFilter")

    sc.stop()
