//https://docs.cloudera.com/documentation/other/tutorial/CDH5/topics/ht_wordcount3.html
//WordCount v3.0 - IMPORTANT - this is work in progress

import java.io.IOException;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.util.HashSet;
import java.util.Set;
import java.util.*;

import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.StringUtils;

import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class WordCount {
        
 public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> {
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();
        
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        StringTokenizer tokenizer = new StringTokenizer(line);
        while (tokenizer.hasMoreTokens()) {
            word.set(tokenizer.nextToken());
            context.write(word, one);
        }
    }
 } 
        
 public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable> {

    public void reduce(Text key, Iterator<IntWritable> values, Context context) 
      throws IOException, InterruptedException {
        int sum = 0;
        while (values.hasNext()) {
            sum += values.next().get();
        }
        context.write(key, new IntWritable(sum));
    }
 }
        
 public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = new Job(conf, "wordcount");

    for (int i = 0; i < args.length; i += 1) {
        if ("-skip".equals(args[i])) {
          job.getConfiguration().setBoolean("wordcount.skip.patterns", true);
          i += 1;
          job.addCacheFile(new Path(args[i]).toUri());
          LOG.info("Added file to the distributed cache: " + args[i]);
        }
      }
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    job.setMapperClass(Map.class);

    job.setCombinerClass(Reduce.class);
    job.setReducerClass(Reduce.class);
         
    private String input;
    private Set<String> patternsToSkip = new HashSet<String>();
    if (context.getInputSplit() instanceof FileSplit) {
        this.input = ((FileSplit) context.getInputSplit()).getPath().toString();
      } else {
        this.input = context.getInputSplit().toString();
      }
    if (config.getBoolean("wordcount.skip.patterns", false)) {
    URI[] localPaths = context.getCacheFiles();
    parseSkipFile(localPaths[0]);
    }
    if (word.isEmpty() || patternsToSkip.contains(word)) {
        continue;
      }

    job.setInputFormatClass(TextInputFormat.class);
    job.setOutputFormatClass(TextOutputFormat.class);
        
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    job.waitForCompletion(true);
 }

 private void parseSkipFile(URI patternsURI) {
    LOG.info("Added file to the distributed cache: " + patternsURI);
    try {
      BufferedReader fis = new BufferedReader(new FileReader(new File(patternsURI.getPath()).getName()));
      String pattern;
      while ((pattern = fis.readLine()) != null) {
        patternsToSkip.add(pattern);
      }
    } catch (IOException ioe) {
      System.err.println("Caught exception while parsing the cached file '"
        + patternsURI + "' : " + StringUtils.stringifyException(ioe));
    }
        
}
