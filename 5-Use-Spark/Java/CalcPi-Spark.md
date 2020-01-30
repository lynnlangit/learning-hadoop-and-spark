## To run a sample Spark job on GCP Dataproc:

- Create a GCP Dataproc managed Hadoop/Spark cluster using the GCP WebUI
    - Select `install components`
    - Install `Spark Console`
- Wait for the cluster to be available (~ 2 minutes) --> green indicator
- Select `Jobs` in the left nav to switch to GCP Dataproc's jobs view.
- Click `Submit job` to open the GCP WebUI
- Select your new cluster `example-cluster` from the Cluster drop-down menu.
- Select `Spark` from the Job type drop-down menu.
- Enter `file:///usr/lib/spark/examples/jars/spark-examples.jar` in the Jar file field.
- Enter `org.apache.spark.examples.SparkPi` in the Main class or jar field.
- Enter `1000` in the Arguments field to set the number of tasks.
- Click `submit job` and wait for the job to complete
- Review the job run output in the WebUI and/or the Spark Job History Console