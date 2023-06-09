Detail Design Presentation：
Pi_using_MapReduce
https://docs.google.com/presentation/d/1ghCmYWVxYW82MUV4BK1IQQ3wHP1cteWLUdHM0ROYvFE/edit#slide=id.g2504991d7a9_0_236

Design

![image](https://user-images.githubusercontent.com/93315926/194803849-7c4c723f-81a1-48ef-b068-12dd25496823.png)

Step 1: Generate an input file to the Pi MapReduce program

Step 1.1: Create a regular Java program which accepts two command line arguments.
R: The radius
N: The number of (x, y) pairs to create The Java program then randomly generates N pairs of (x, y) and displays them on the standard output. Step 1.2: Run the program created in Step 1.1 and save the result in a file. The file is the input to Step 2's Pi MapReduce program.
Step 2: Create a MapReduce program to calculate the numbers of inside darts and outside darts.

Step 3: Use the file generated in Step 1.2 as the input to execute the MapReduce program created in Step 2

Step 4: Calculate Pi in the driver program based on the numbers of inside darts and outside darts.

Implement

![image](https://user-images.githubusercontent.com/93315926/194799644-6b303972-e90e-4fc4-821b-0b26e2df9a6d.png)

Prepare input data
```
  $ mkdir PiCalculation
  $ cd PiCalculation
  $ vi GenerateRandomNumbers.java
  $ javac GenerateRandomNumbers.java
  $ java -cp . GenerateRandomNumbers
```
  
Input data will store in PiCalculationInput

Setup passphraseless ssh

Now check that you can ssh to the localhost without a passphrase:
```
  $ cd hadoop-3.3.4/
  $ ssh localhost
```
If you cannot ssh to localhost without a passphrase, execute the following commands:
```
  $ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
  $ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
  $ chmod 0600 ~/.ssh/authorized_keys
```
Make the HDFS directories required to execute MapReduce jobs(Copy input data to HDFS)
```
  $ cd ..
  $ cd hadoop-3.3.4/
  $ bin/hdfs namenode -format
  $ sbin/start-dfs.sh
  $ wget http://localhost:9870/
  $ bin/hdfs dfs -mkdir /user
  $ bin/hdfs dfs -mkdir /user/czhao322
  $ bin/hdfs dfs -mkdir /user/czhao322/picalculate
  $ bin/hdfs dfs -mkdir /user/czhao322/picalculate/input
  $ bin/hdfs dfs -put ../PiCalculation/PiCalculationInput /user/czhao322/picalculate/input
```  
Prepare code

Build PiCalculation java file
```
  $ cd /hadoop-3.3.4
  $ vi PiCalculation.java 
```
Compile PiCalculation.java and create a jar
```
  $ bin/hadoop com.sun.tools.javac.Main PiCalculation.java
  $ jar cf wc.jar PiCalculation*class  
```
Run

Execute
```
  $ bin/hadoop jar wc.jar PiCalculation /user/czhao322/picalculate/input /user/czhao322/picalculate/output7
```
Output
```
  $ bin/hdfs dfs -ls /user/czhao322/picalculate/output7
  $ bin/hdfs dfs -cat /user/czhao322/picalculate/output7/part-r-00000 
```
Stop
```
  $ sbin/stop-dfs.sh
```
Test Result

![image](https://github.com/ceciliazhao1/cloudcomputing/blob/main/pi/image.png)

Test Case:

How many random numbers to generate: 1000000 Radius = 200
  

