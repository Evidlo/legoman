----
author: evan
template: project.j2
date: 2019-04-09
title: Formatting and math demo
description: Demonstrating various formatting features
----

[TOC]

# Heading 1

### Heading 3

* bullet1
* bullet2
    * sub bullet
    

# Images

![inline image](cheetos_small.png "title"){: .inline } 
![inline image](cheetos_small.png){: .inline } 
![inline image](cheetos_small.png){: .inline } 

![](cheetos_small.png){: #id1 .class1 .class2 }  


# Math

$$3x + 4y$$

$$[Rf]\(t, \theta\) = \int_{\mathbb{R}^2} f(x)\delta(N_{\theta}^T x - t)\, dx$$

# Code

A code snippet
``` python
print('hello world')
print('my name is evan')
```

Including an external file

`test.py`

``` python
def fib():
    a, b = 0, 1
    while 1:
        yield a
        a, b = b, a + b

x = fib()
next(x)
```
