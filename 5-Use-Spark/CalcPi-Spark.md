## To run a sample Spark job:

- Select Jobs in the left nav to switch to Dataproc's jobs view.
- Click `Submit job`
- Select your new cluster example-cluster from the Cluster drop-down menu.
- Select `Spark` from the Job type drop-down menu.
- Enter `file:///usr/lib/spark/examples/jars/spark-examples.jar` in the Jar file field.
- Enter `org.apache.spark.examples.SparkPi` in the Main class or jar field.
- Enter `1000` in the Arguments field to set the number of tasks.