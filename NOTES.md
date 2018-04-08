Notes:

I tested the fine details well. I didn't write enough integration tests. Once I started writing
the client, bugs started turning up like flies. (A good lesson learned on the side - if you're 
building a tool, using it as users will is the best way to test the interface with users.) Testing
databases is hard, but forced me to split up code into multiple steps: "should I change this", 
"what should I change it to" and "change it to that". Databases don't play well with unit tests, 
and I always have this temptation to just read the entire table (or the columns I need) and then
write pure functions that product the correct results. However, that's obviously not scalable and
defeats the whole point of a database.

Although, why am I using a database for this? And why did I choose pgsql? I used a database because
its what is done, its how you design systems for the web. And that makes sense, for long-running
stateful web applications. But in this case, the state only sticks around for a few hours, and the
server won't last long either. It's a game meant to be played in three hours, locally. I guess I
used a database to get experience writing code that connects a externally-facing API to a database,
but if I were writing this purely for fun (to play the game, not to experience developing it) I
might have chosen to not use a database at all.

Python is a lot less fun than I remembered. Flask is a neat, small framework that does exactly what
I want it to do when I'm making an API. But the lack of types (and my own failings at writing 
informal data definitions & signatures) meant that I missed a lot of bugs. Type annotations are
something, and I'll go through and add them so that adding features doesn't become impossible, but
they aren't racket-style contracts, they aren't enforcable. I could write lines and lines of code
per function checking the inputs, but my functions are only a few lines long anyway and it feels
like a waste.  

I made a security mistake. At the beginning, I had functions that manipulated the database, some of
which validated a civilization's key to make sure they were allowed to do what they were trying to
do. The issue came when I wanted to reuse that code to do back-end, server-side game mechanics. The
user-facing code did two things: check a key, and then perform the operation, so I had to refactor
each function. I should have split the two tasks from the beginning. I'm certain there are some API
endpoints that let any civ do something they shouldn't be able to.

I feel relatively confident about the layered-function architecture I used. The Flask app, `app.py`,
does the request processing - extracting headers, delegating to functions based on the HTTP method 
used, etc. The second layer checks the key and composes simple database-manipulating functions. The
database manipulating functions are split into checking the values are correct, and then setting 
operations. While it does mean that lots of functions are defined (it's hard to remember names), it
makes it easier to reason about how each piece works.