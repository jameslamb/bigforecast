from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import psycopg2


conn = psycopg2.connect(database="tcount",
                        user="postgres",
                        password="pass",
                        host="localhost",
                        port="5432")

class WordCounter(Bolt):
    """
    Streamparse bolt which counts the words in the incoming tweet tuple and
    updates the Postgres Database table with the newest counts.
    """

    def initialize(self, conf, ctx):
        self.counts = Counter()


    def process(self, tup):
        word = tup.values[0]
        # word = "dale"

        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        # Database name: Tcount
        # Table name: Tweetwordcount
        # you need to create both the database and the table in advance.

        # Increment the local count
        self.counts[word] += 1
        self.emit([word, self.counts[word]])


        # USert the database
        # Check if need insert, else update
        # Check to see what the errors are here and clean this up
        cur = conn.cursor()

        # If the wordcount != 1 locally, then it must be in the database and
        # only call update
        if True:
            try:
                cur.execute("INSERT INTO Tweetwordcount (word, count) \
                            VALUES (%s, %s);", (word, self.counts[word]))
                conn.commit()
                cur.close()
            except:
                conn.rollback()
                cur.close()
                cur = conn.cursor()
                cur.execute("UPDATE Tweetwordcount SET count=%s WHERE word=%s",
                        (self.counts[word], word))
                conn.commit()
                cur.close()

        # This method is going to hammer the database with 1-2 calls per word.
        # Maybe that's okay for a localhost DB but it could easily become a bottleneck

        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))
