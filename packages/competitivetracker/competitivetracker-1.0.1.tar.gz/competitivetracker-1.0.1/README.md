[![Build Status](https://travis-ci.com/darrensmith223/CompetitiveTracker.svg?branch=main)](https://travis-ci.com/darrensmith223/CompetitiveTracker)
[![Documentation Status](https://readthedocs.org/projects/competitivetracker/badge/?version=latest)](https://competitivetracker.readthedocs.io/en/latest/?badge=latest)

# CompetitiveTracker
Python library for SparkPost's [Competitive Tracker](https://www.sparkpost.com/competitive-tracker/)

# Documentation
Documentation for [CompetitiveTracker Python Client](https://competitivetracker.readthedocs.io/en/latest/)

[Competitive Tracker API Documentation](http://api.edatasource.com/docs/#/competitive)


# Installation

Install from Pypi using pip:

```code-block:: bash
$ pip install competitivetracker
```

You may need to use `pip3` to install.


# Authentication

You will need an API key to use the Competitive Tracker API.  To get an API key, contact support through the [Competitive Tracker app](https://app.emailanalyst.com/bin/#/login). 

Once you have an API key, you can pass it to the CompetitiveTracker class:

```python
    from competitivetracker import CompetitiveTracker
    ct = CompetitiveTracker("API_KEY")
```

# How to Use

You can use the underlying Competitive Tracker API with the classes in the `competitivetracker` module:

* `competitivetracker.core.brands`
* `competitivetracker.core.companies`
* `competitivetracker.core.discover`
* `competitivetracker.core.domains`
* `competitivetracker.core.esps`
* `competitivetracker.core.graph`
* `competitivetracker.core.industries`
* `competitivetracker.core.ping`
* `competitivetracker.domain_info`
* `competitivetracker.intelligence.brand`
* `competitivetracker.intelligence.campaign`
* `competitivetracker.intelligence.domain`
* `competitivetracker.intelligence.ipdeliverability`
* `competitivetracker.overlaps`
* `competitivetracker.ping`
* `competitivetracker.search`


For example, we can retrieve campaign data for all of the campaigns from the previous day for a particular domain using the `competitivetracker.intelligence.domain` class:

```python
    from competitivetracker import CompetitiveTracker

    ct = CompetitiveTracker("API_KEY")

    response = ct.intelligence.domain.get_campaigns(domain="example.com", qd="daysBack:1")
    print(response)
```

For a complete list of classes and functions, see the [Competitive Tracker Python documentation](https://competitivetracker.readthedocs.io/en/latest/api.html).


# Contribute

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork the [repository](https://github.com/darrensmith223/CompetitiveTracker) on GitHub and make your changes in a branch on your fork
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request.
