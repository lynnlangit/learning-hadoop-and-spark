from mrjob.job import MRJob

class MRWordCounter(MRJob):

    def mapper(self, _, line):
        words = line.split()
        for word in words:
            yield word, 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRWordCounter.run()

# This program uses the mrjob library to implement a MapReduce algorithm for word counting. 
# The mapper function takes in a line of text and splits it into individual words, 
# then yields each word with a count of 1. 
# 
# The reducer function takes in each word and its associated counts, 
# then sums up the counts for each word and yields the final count for that word. 
# Finally, the program runs the MapReduce job.

