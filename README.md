To run this program, 
run python3 main.py --database-type s3 --producer-bucket 'your bucket that the producer is pushing to' --consumer-bucket 'your bucket your consumer will push producer files to'
or python3 main.py --database-type dynamo --producer-bucket 'your bucket that the producer is pushing to' --consumer-bucket 'your bucket your consumer will push producer files to'
Here is an example of how I run this command with s3, python3 main.py --database-type s3 --producer-bucket usu-cs5260-goob-requests --consumer-bucket usu-cs5260-goob-dist

To run the unit test file, run python3 -m unittest tests/tests.py

My consumer program continually runs and can only be ended by closing the terminal or by cancelling the program. It listens for the producer.jar file.
Overall, this is a simple program to run.
I am pushing the producer.jar data to my bucket2 and then pulling it into my bucket1 with my consumer program.



###########################HW3#############################

To run the program with sqs, you run python3 main.py --database-type sqs --queue-url 'your queues url' --consumer-bucket 'your consumer bucket'
In my example, I'm doing it like this, python3 main.py --database-type sqs --queue-url https://sqs.us-east-1.amazonaws.com/927548461110/cs5260-requests  --consumer-bucket usu-cs5260-goob-dist