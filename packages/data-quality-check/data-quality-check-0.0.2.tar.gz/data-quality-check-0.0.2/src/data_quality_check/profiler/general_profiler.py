from typing import List, Dict

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.utils import AnalysisException

from data_quality_check.config import ConfigProfilingGeneral


class GeneralProfilingResult:
    field_name: str
    min_value = None
    max_value = None
    mean_value = None
    stddev_value = None
    zero_count = None  # 0
    null_count = None  # Null
    empty_count = None  # Empty String
    row_count = None
    duplicate_row_count = None
    unique_row_count = None
    value_count = None
    top_freq_count_by_values = None

    def __init__(self, field_name):
        self.field_name = field_name

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            'field_name': self.field_name,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'mean_value': self.mean_value,
            'stddev_value': self.stddev_value,
            'zero_count': self.zero_count,
            'null_count': self.null_count,
            'empty_count': self.empty_count,
            'row_count': self.row_count,
            'duplicate_row_count': self.duplicate_row_count,
            'unique_row_count': self.unique_row_count,
            'value_count': self.value_count,
            'top_freq_count_by_values': self.top_freq_count_by_values
        }

    def to_str_dict(self):
        return {
            'field_name': str(self.field_name),
            'min_value': str(self.min_value),
            'max_value': str(self.max_value),
            'mean_value': str(self.mean_value),
            'stddev_value': str(self.stddev_value),
            'zero_count': str(self.zero_count),
            'null_count': str(self.null_count),
            'empty_count': str(self.empty_count),
            'row_count': str(self.row_count),
            'duplicate_row_count': str(self.duplicate_row_count),
            'unique_row_count': str(self.unique_row_count),
            'value_count': str(self.value_count),
            'top_freq_count_by_values': str(self.top_freq_count_by_values)
        }


class GeneralProfiler:
    config: ConfigProfilingGeneral
    field_results: Dict[str, GeneralProfilingResult]
    field_names: List[str]
    spark: SparkSession

    def __init__(self, spark, df: DataFrame, config=ConfigProfilingGeneral()):
        self.df = df
        self.spark = spark
        self.config = config

    def run(self, return_type='dict'):
        if len(self.config.columns) < 1 or self.config.columns[0] == '*':
            self.field_names = self.df.columns
        else:
            self.field_names = self.config.columns

        self.field_results = {}
        for field_name in self.field_names:
            df = self.df
            spark = self.spark
            field_result = GeneralProfilingResult(field_name)
            field_result.row_count = get_field_summary_by_type(df, field_name, 'count')
            field_result.mean_value = get_field_summary_by_type(df, field_name, 'mean')
            field_result.stddev_value = get_field_summary_by_type(df, field_name, 'stddev')
            field_result.min_value = get_field_summary_by_type(df, field_name, 'min')
            field_result.max_value = get_field_summary_by_type(df, field_name, 'max')

            field_result.zero_count = get_count_by_field_condition(spark, df, f'`{field_name}` == 0')
            field_result.null_count = get_count_by_field_condition(spark, df, f'`{field_name}` is NULL')
            field_result.empty_count = get_count_by_field_condition(spark, df, f'`{field_name}` == ""')

            field_result.value_count = get_value_count(spark, df, field_name)
            field_result.top_freq_count_by_values = get_top_freq_count_by_values(spark, df, field_name)
            field_result.unique_row_count = get_unique_row_count(spark, df, field_name)
            field_result.duplicate_row_count = get_duplicated_row_count(spark, df, field_name)
            self.field_results[field_name] = field_result

        if return_type == 'dataframe':
            data = [vi.to_str_dict() for vi in list(self.field_results.values())]
            return spark.createDataFrame(data).select('field_name', 'min_value', 'max_value', 'mean_value',
                                                      'stddev_value', 'zero_count', 'null_count',
                                                      'empty_count', 'row_count', 'duplicate_row_count',
                                                      'unique_row_count', 'value_count')
        else:
            return self.field_results


def get_field_summary_by_type(df, field_name: str, summary_type: str):
    try:
        result_df = df.select(field_name).selectExpr(f'{summary_type}({field_name}) as value')
    except AnalysisException:
        return None
    return result_df.collect().pop()['value']


def get_value_count(spark, df, field_name: str):
    df.createOrReplaceTempView('temp_profiling_tb')
    return spark.sql(f'SELECT 1 AS ct from temp_profiling_tb GROUP BY ({field_name})').count()


def get_top_freq_count_by_values(spark, df, field_name: str):
    df.createOrReplaceTempView('temp_profiling_tb')
    query = f'SELECT SUM(1) as ct, {field_name} as value from temp_profiling_tb GROUP BY ({field_name}) ' \
            f' ORDER BY ct DESC limit 10'
    rows = spark.sql(query).collect()
    return [{'value': row['value'], 'count': row['ct']} for row in rows]


def get_unique_row_count(spark, df, field_name: str):
    df.createOrReplaceTempView('temp_profiling_tb')
    query = f'SELECT SUM(1) as ct, {field_name} as value from temp_profiling_tb GROUP BY ({field_name}) ' \
            f' HAVING ct=1'
    return spark.sql(query).count()


def get_duplicated_row_count(spark, df, field_name: str):
    df.createOrReplaceTempView('temp_profiling_tb')
    query = f' SELECT COALESCE(SUM(ct),0) AS ct FROM ' \
            f'(' \
            f' SELECT SUM(1) as ct, {field_name} as value from temp_profiling_tb GROUP BY ({field_name}) ' \
            f' HAVING ct>1' \
            f')'
    return spark.sql(query).collect().pop()['ct']


def get_count_by_field_condition(spark, df, field_condition: str):
    df.createOrReplaceTempView('temp_profiling_tb')
    query = f'SELECT 1 FROM temp_profiling_tb WHERE {field_condition}'
    return spark.sql(query).count()
