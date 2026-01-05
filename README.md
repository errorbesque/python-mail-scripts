# mail autoreplier project
I tried to implement this day-of for our event, and it mostly worked.
## purpose
This program serves two purposes:

(1) We wanted to send an email with one message to people who have emailed us before, 
and a different message with people who haven't emailed us before.

(2) We also wanted to produce a live graph that showed the cumulative email responses on demand. 
This is a loose predictor of attendance (based on subjective observation), and also can show increased rates of response to interventions like posts or messages.

![screenshot of plot](https://github.com/errorbesque/python-mail-scripts/blob/main/plot.jpg?raw=true)

# notes
I was frustrated by the manual process of having to vet the list (given the high number of people who were novel senders who were recognizable as known entities, this turned the previously easily-computable filter into an unpleasant 2-hour task).

We had 2 hours of downtime: due to automated session logout (on the pm side)
we missed 15 emails (I manually responded to these and restarted the process). 
I came back in the morning after teardown and it was still up though, so not sure if there is another thing to anticipate re: process longevity.
