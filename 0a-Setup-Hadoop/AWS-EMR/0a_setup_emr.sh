# Instructions to set up AWS EMR for testing

# 1. Create EC2 SSH key
# 2. Create EMR cluster - Spark configuration (#4)
# 3a. If SSH, set up Security Group rule for yourIP port:22 (inbound)
# 3b0. If Notebook, create EMR Notebook, connect, set kernel to `PySpark`
# 3b1. Use script `CalcPi` to test setup 
# 4. Can Use Spark History Server WebUI to eval job run

# 5. Remeber to DELETE - notebook and cluster when done!