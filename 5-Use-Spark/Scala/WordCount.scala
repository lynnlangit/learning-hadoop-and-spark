import org.apache.spark.sql.functions._

object WordCount{

    def main(args: Array[String]): Unit = {
        val input = "Hello hello world Hello hello world Hello how are you world"
        val ds = sqlContext.read.text(input).as[String]
        val result = ds
            .flatMap(_.split(" "))               // Split on whitespace
            .filter(_ != "")                     // Filter empty words
            .toDF()                              // Convert to DataFrame to perform aggregation / sorting
            .groupBy($"value")                   // Count number of occurences of each word
            .agg(count("*") as "numOccurances")
            .orderBy($"numOccurances" desc)      // Show most common words first

        display(result)
  }
    
}