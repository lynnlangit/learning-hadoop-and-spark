# learning-hadoop
Companion Repository to Learning Hadoop course on Linked In Learning

Course is here - https://www.lynda.com/Hadoop-tutorials/Hadoop-Fundamentals/191942-2.html

Can use the following options:
- GCP Dataproc 
    - install Hadoop/Spark by default 
    - add Conda/Jupyter libraries (select `install components`)
- AWS EMR 
    - select Spark install from 4 available configurations
    - can create EMR Jupyter notebook
- Databricks Community Edition for AWS (also available for Azure)
    - select best fit Spark / Scala version
    - now Python3 only
    - includes Databricks notebooks
    - no GPUs in community edition
- Cloudera QuickStart VM (7 GB download) or Docker Image
    - not recommended, too large, install errors for many people

For production Hadoop/Spark clusters:
- Setup, pricing & monitoring for cloud
    - GCP Deployents or gcloud scripts
    - AWS Marketplace (uses AWS CloudFormation templates) or awscli scripts
    - Terraform Templates (multiple cloud vendors)
- Right-sizing in cloud and cost savings
    - GCP Preemptible Instances
    - AWS Spot or AWS Batch
