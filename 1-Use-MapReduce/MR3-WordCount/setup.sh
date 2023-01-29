#Example for Word Count 3.0 with stop words
#Improve the quality of your results by filtering out info that is unnecessary 
#Create a list of stop words and punctuation, and then have the application skip them at run time.

#To compile for package WordCount.java
rm -rf build word_count.jar
mkdir -p build
javac -cp /usr/lib/hadoop/*:/usr/lib/hadoop-mapreduce/* WordCount.java -d build -Xlint
jar -cvf wordcount.jar -C build/ .

#Create a list of stop words. Store them in a file named stop_words.text
echo -e "a\\nan\\nand\\nbut\\nis\\nor\\nthe\\nto\\n.\\n," > stop_words.text

#Put stop_words.text into the Hadoop file system
hadoop fs -put stop_words.text /user/<working_dir>/wordcount/

#Run the application with the -skip switch 
#and the name of the stop_words.text file.
hadoop jar wordcount.jar org.myorg.WordCount /user/<my_dire>/wordcount/input /
    /user/<my_dir>/wordcount/output -skip /user/<my_dir>/wordcount/stop_words.text

