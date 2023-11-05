#########QUESTION 1####################

I believe it's possible that Update and Delete Widget Requests may fail, even when I'm running just one Consumer is because there are delays within queues when these widgets can be received and sent to my consumer. Because of this, there could be issues with when your consumer receives these requests that they may not exist yet, or there may be nothing to return still.


###########QUESTION 2##################

This would impact the design of distributed applications that use queues through failures of updating and deleting widgets by occaisionally holding outdated data that shouldn't be used.  This could be troublesome if you were trying to analyze data and not all of the data that was supposed to be changed or removed was changed or removed. Causing false assumptions on your data.