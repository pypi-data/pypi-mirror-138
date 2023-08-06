# Data Analysis

### Why did I write this code?
I'm often handed a dataset and asked to do the same thing - determine if the experimental group is different than the control group, and generate some descriptive statistics along the way. As an alternative to writing all operations manually for each project I've created a Python module using Object Oriented Programming (OOP). This eliminates the need to search for old projects, copy and paste long lines of code and cross my fingers that it works. 

### What libraries does this code use?

This code uses a [Scipy](https://scipy.org/), a widely accepted statistical package, to perform hypothesis testing.

I also use [Pandas](https://pandas.pydata.org/), an extremely popular data analysis and manipulation library for organizing the data and providing descriptive statistics.

For data visualization I use the [Seaborn](https://seaborn.pydata.org/) library (built on top of matplotlib)

### Hypothesis Testing
My main task is often to determine if the results are statistically significant. For this we need to implement a hypthesis test, however there are many to [choose from](https://help.xlstat.com/s/article/which-statistical-test-should-you-use?language=en_US). The decision tree of this code looks something like this:
1. Is the data Normally Distributed and do the experimental and control groups have Equal Variance? Student's t-test
2. Is the data Normally Distributed but do the experimental and control groups have Unequal Variance? Welches' t-test
3. Is the data not Normally Distributed? Mann-Whitney U test

![](decision_tree.png)

### Where to Start

See [This Notebook](https://github.com/Gabriel-Aspen/data_analysis_example/blob/main/demo.ipynb) for a demo on the Breast Cancer Wisconsin (Diagnostic) Dataset found [Here](https://www.kaggle.com/uciml/breast-cancer-wisconsin-data)
# autohyp
