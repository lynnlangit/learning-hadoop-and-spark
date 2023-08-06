import sys
from hadoop.io import Text, IntWritable

# This is the mapper function. It takes one line of input from the input file and emits key/value pairs.
def mapper(key, value):
    # Split the line into words.
    words = value.split()

    # For each word, emit a key/value pair where the key is the word and the value is 1.
    for word in words:
        yield (word, 1)

# This is the reducer function. It takes key/value pairs from the mapper and combines them into a single key/value pair.
def reducer(key, values):
    # Count the number of values for each key.
    count = 0
    for value in values:
        count += value

    # Emit the key/value pair where the key is the word and the value is the count.
    yield (key, count)

# This is the main function. It reads the input file, applies the mapper and reducer functions, and writes the output to the output file.
def main():
    # Get the input and output file names from the command line arguments.
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    # Create a Hadoop job.
    job = Job()

    # Set the input and output file names.
    job.setInputPath(input_file_name)
    job.setOutputPath(output_file_name)

    # Set the mapper and reducer classes.
    job.setMapperClass(mapper)
    job.setReducerClass(reducer)

    # Set the output key and value types.
    job.setOutputKeyClass(Text)
    job.setOutputValueClass(IntWritable)

    # Run the job.
    job.waitForCompletion(True)

if __name__ == "__main__":
    main()
