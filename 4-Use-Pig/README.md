# learning-hadoop
Companion Repository to Learning Hadoop course on Linked In Learning

Course is here - https://www.lynda.com/Hadoop-tutorials/Hadoop-Fundamentals/191942-2.html  


Run Ways. You can run Pig three ways – using either local mode or hadoop (mapreduce) mode: Grunt Shell: Enter Pig commands manually using Pig's interactive shell, Grunt. Script File: Place Pig commands in a script file and run the script.

### How to start a Pig shell

First, copy the /etc/passwd file to your local working directory. Next, invoke the Grunt shell by typing the "pig" command (in local or hadoop mode). Then, enter the Pig Latin statements interactively at the grunt prompt (be sure to include the semicolon after each statement).

### Working with the Grunt Shell

There are 3 execute modes of accessing Grunt shell:

 - local – Type pig -x local to enter the shell
 - mapreduce – Type pig -x mapreduce to enter the shell
 - tez – Type pig -x tez to enter the shell  

Default is mapreduce, so if you just type pig, it will use mapreduce as the execution mode.

`pig`

### More Info

===============
1. To learn about Pig, try http://wiki.apache.org/pig/PigTutorial
2. To build and run Pig, try http://wiki.apache.org/pig/BuildPig and
http://wiki.apache.org/pig/RunPig
3. To check out the function library, try http://wiki.apache.org/pig/PiggyBank