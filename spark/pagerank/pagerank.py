import sys
from pyspark import SparkConf, SparkContext

def show_warning():
    print("""
    WARN: This is a naive implementation of PageRank
    and is given as an example!
    Please use the PageRank implementation found in
    org.apache.spark.graphx.lib.PageRank
    for more conventional use.
    """)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: PageRank <file> <iter> <output_path>")
        sys.exit(1)

    show_warning()

    sparkConf = SparkConf().setAppName("PageRank")
    sc = SparkContext(conf=sparkConf)

    lines = sc.textFile(sys.argv[1])

    links = lines.map(lambda s: s.split()).map(lambda parts: 
               (parts[0], parts[1])).distinct().groupByKey().cache()

    ranks = links.mapValues(lambda v: 1.0)

    iters = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    for _ in range(iters):
        
        contribs = links.join(ranks).flatMap(lambda urls_rank: 
           [(url, urls_rank[1][1] / len(urls_rank[1][0])) for url in urls_rank[1][0]])

        ranks = contribs.reduceByKey(lambda x, y: x + y).mapValues(lambda rank: 
           0.15 + 0.85 * rank)

    output = ranks.collect()
    output_rdd = sc.parallelize(output)
    output_rdd.saveAsTextFile(sys.argv[3])
    for tup in output:
        print(tup[0] + " has rank: " + str(tup[1]) + ".")

    sc.stop()
