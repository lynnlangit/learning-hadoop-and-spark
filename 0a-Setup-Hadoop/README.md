# Setup Hadoop and Libraries

This is a companion Repo to my `Learning Hadoop` (and other Spark) courses on Linked In Learning.  
My Course is here - https://www.lynda.com/Hadoop-tutorials/Learning-Hadoop-2020-Revision/2817067-2.html

### Hadoop/Spark Learning Cloud Cluster Setup Info:

General cloud Hadoop cluster setup considerations include at which level you'd like to interact with your cluster resources.  Most modern cloud vendors include three options:

- IaaS - use **managed VMs**, i.e. Dataproc on GCE for GCP, EMR on EC2 for AWS...
- PaaS - use **Kubernetes**, i.e. Dataproc on GKE for GCP, EMR on EKS for AWS...
- SaaS - use **Serverless**, i.e. [Serverless Sessions](https://cloud.google.com/vertex-ai/docs/workbench/managed/serverless-spark) for GCP, [Job Runs](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html) for AWS...

---

More detail for each cloud vendor setup listed below.   
Even more detail on my 'advanced setup notes page' - [link](https://github.com/lynnlangit/learning-hadoop-and-spark/blob/master/0a-Setup-Hadoop/adv-setup.md)

- **GCP Dataproc** - "partially-managed"
    - install Hadoop and/or Spark by default
        - other libraries optional (Hive, etc...)
        - add Conda/Jupyter libraries (select `install components`)
        - includes Spark History WebUI
    - can use GCE (VMs) for Hadoop/Spark workloads
        - w/ included tooling (web ui for YARN, etc...)
    - use GKE (K8) for rapidly scaling Spark workloads
        - w/ K8 tooling
        - requires 'standard-cluster w/workload identity enabled' 
        - NOT 'auto-pilot-cluster'
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


