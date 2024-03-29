## This project is trying to collect and analyze weather data

The main purpose is to have some practical exercise with python programming, hadoop, hive, and spark.

Data Source: 
1. [Meteorological Service of Canada (MSC) Datamart](https://eccc-msc.github.io/open-data/msc-datamart/readme_en/)
1. [VisualCrossing](https://www.visualcrossing.com)

## Installation

```sh
# export requirements.txt
pip freeze > requirements.txt
# import requirements.txt
pip install -r requirements.txt
```

## Work Flow

This project plans to:

- fetch data from weather api provided by [VisualCrossing](https://www.visualcrossing.com)
- save it in mysql or csv/json files in hdfs
- load data sources in hive
- load data with pyspark
- data pre-preparation: clean pipeline
- make prediction
- create visualization with tableau