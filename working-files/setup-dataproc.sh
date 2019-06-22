gcloud beta dataproc clusters create cluster-e8db \
 --enable-component-gateway --region us-west1 --subnet default --zone "" \
 --master-machine-type n1-standard-2 --master-boot-disk-size 500 \
 --num-workers 2 --worker-machine-type n1-standard-2 \
 --worker-boot-disk-size 500 --image-version 1.3-debian9 \
 --optional-components ANACONDA,JUPYTER --project root-cortex-244002
