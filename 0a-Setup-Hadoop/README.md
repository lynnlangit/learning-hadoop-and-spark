# learning-hadoop-and-spark
Companion Repository to `Learning Hadoop` course on Linked In Learning

Course is here - https://www.lynda.com/Hadoop-tutorials/Learning-Hadoop-2020-Revision/2817067-2.html

### Hadoop/Spark Learning Cloud Cluster Setup Info:

General cloud Hadoop cluster setup considerations include at which level you'd like to interact with your cluster resources.  Most modern cloud vendors include three options:
- IaaS - use **managed VMs**, i.e. GCE for GCP, EC2 for AWS...
- PaaS - use **Kubernetes**, i.e. GKE for GCP, EKS for AWS...
- SaaS - use **Serverless** endpoints, i.e. Serverless Sessions for GCP, Job Runs for AWS...

More detail for each cloud vendor setup listed below.  

- **GCP Dataproc** - "partially-managed"
    - install Hadoop/Spark by default 
    - add Conda/Jupyter libraries (select `install components`)
    - includes Spark History WebUI
- **AWS EMR** - "partially-managed"
    - select Spark install from 4 available EMR configurations
    - can create/use EMR Jupyter notebook (alternative to SSH client)
    - includes Spark History WebUI
    - can use EMR Studio (includes Jupyter) - [link](https://aws.amazon.com/blogs/big-data/amazon-emr-studio-preview-a-new-notebook-first-ide-experience-with-amazon-emr/)
- **Databricks Community Edition for AWS** (also available for Azure) - "fully-managed"
    - select best fit Spark / Scala version
    - now Python3 only
    - includes Databricks notebooks
    - no GPUs in community edition
- **Cloudera QuickStart VM** (7 GB download) or Docker Image
    - not recommended, too large, install errors for many people
---

### For production Hadoop/Spark clusters:

- Setup, pricing & monitoring for cloud
    - GCP Deployents or gcloud scripts
    - AWS Marketplace (uses AWS CloudFormation templates) or awscli scripts
    - Terraform Templates (multiple cloud vendors)
- Right-sizing in cloud and cost savings
    - GCP Preemptible (or Spot) Instances
    - AWS Spot or AWS Batch
