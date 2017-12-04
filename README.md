# Basic analytics on server log file
Perform basic analytics on the server log file, provide useful metrics, and implement basic security measures. 

## Getting Started
This is a program providing basic analytics on server log files, including the following features:

* Feature 1:
List the top 10 most active host/IP addresses that have accessed the site.

* Feature 2:
Identify the 10 resources that consume the most bandwidth on the site

* Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods

* Feature 4:
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.

As for implementation, this program implements count-min sketch(https://sites.google.com/site/countminsketch/) to process the large amount of streaming data efficiently, at the price of the occasional error. The probability of an error can be quantified and one can trade off the expected error rate with the amount of resources (storage, time) afforded. 

Another hightlight is the controller-features structure of the whole analysis program. Basically, there is a single controller taking care of the input and output path. And there are bunches of features each of them providing a specific metric. Each time you can choose to subscribe different features to the controller, run the controller, and then get the metrics corresponding to the features. 

This project was created for a coding challenge in Insight Data Engineering program. The insight_testsuite subfolder is provided by Insight Data Enigneeering program. There are sample inputs in the log_input folder and sample outpus in the log_output folder.

### Installing 

* Fork the repo.

* Create a new branch.

* Run the app. In your command line, type:
./run.sh 

Note: before you run the app, you may need to change the mode of run.sh by typing: chmod +x run.sh

## Todo

### Wrtie additional tests 

## Comments
Very welcome! 

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Credit:
The controller-features structure is modified based on http://www.tldp.org/LDP/LG/issue83/tougher.html
 
The hash function generation in CM_sketch is modified based on https://tech.shareaholic.com/2012/12/03/the-count-min-sketch-how-to-count-over-large-keyspaces-when-about-right-is-good-enough/

The description of the features is modified based on the project description page from Insight Data Science: https://github.com/InsightDataScience/fansite-analytics-challenge
