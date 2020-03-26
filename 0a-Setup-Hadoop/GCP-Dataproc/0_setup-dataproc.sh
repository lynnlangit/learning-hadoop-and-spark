# this script uses 8 CPUs for your cluster

# change the following to your settings

region=us-central1
zone=us-central1-a
project=nosql-langit

gcloud beta dataproc clusters create demo \
    --enable-component-gateway \
    --region $region \
    --subnet default \
    --zone $zone \
    --master-machine-type n1-standard-4 \
    --master-boot-disk-size 500 \
    --num-workers 2 \
    --worker-machine-type n1-standard-2 \
    --worker-boot-disk-size 500 \
    --image-version 1.3-deb9 \
    --optional-components ANACONDA,HIVE_WEBHCAT,JUPYTER,DRUID,PRESTO,ZOOKEEPER \
    --project $project
    
