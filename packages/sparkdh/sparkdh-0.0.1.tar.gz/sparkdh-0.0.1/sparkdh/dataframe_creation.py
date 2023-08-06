
def sample_dataframe(spark_session):
    data = [{"Id": 1},{"Id": 2},{"Id": 3},{"Id": 4},{"Id": 5}]
    df = spark_session.createDataFrame(data)

    return df