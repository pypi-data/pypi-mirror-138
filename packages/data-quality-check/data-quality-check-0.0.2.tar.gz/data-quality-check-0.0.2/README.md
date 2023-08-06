# spark-profiling
[![CI Build](https://github.com/tw-data-quality-2022/spark-profiling/actions/workflows/python-package.yml/badge.svg)
](https://github.com/tw-data-quality-2022/spark-profiling/actions/workflows/python-package.yml)

## Requirements
- Java 8+
- Apache Spark 3.0+

## Dependencies

| Filename | Requirements|
|----------|-------------|
| requirements.txt | Package requirements|
| requirements-dev.txt |  Requirements for development|

## Usage
### Use GeneralProfiler
```python
from pyspark.sql import SparkSession
from data_quality_check.profiler.general_profiler import GeneralProfiler

spark = SparkSession.builder.appName("SparkProfilingApp").enableHiveSupport().getOrCreate()
data = [{'name': 'Alice', 'age': 1}]
df = spark.createDataFrame(data)

result_df = GeneralProfiler(spark, df).run(return_type='dataframe')
result_df.show()

```

### Test
```shell
PYTHONPATH=./src pytest tests/*
```

### Build
```
python setup.py sdist bdist_wheel
twine check dist/*
```

### Publish
```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
```