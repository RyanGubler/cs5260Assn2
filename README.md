To run this program, 
run python3 main.py --database-type s3 --producer-bucket 'your bucket that the producer is pushing to' --consumer-bucket 'your bucket your consumer will push producer files to'
or python3 main.py --database-type dynamo --producer-bucket 'your bucket that the producer is pushing to' --consumer-bucket 'your bucket your consumer will push producer files to'
Here is an example of how I run this command with s3, python3 main.py --database-type s3 --producer-bucket usu-cs5260-goob-requests --consumer-bucket usu-cs5260-goob-dist

To run the unit test file, run python3 -m unittest tests/tests.py

My consumer program continually runs and can only be ended by closing the terminal or by cancelling the program. It listens for the producer.jar file.
Overall, this is a simple program to run.
I am pushing the producer.jar data to my bucket2 and then pulling it into my bucket1 with my consumer program.