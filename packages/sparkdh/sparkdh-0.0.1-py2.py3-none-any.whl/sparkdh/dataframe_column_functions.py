from pyspark.sql import functions

def clone_column(df, existing_column_name, new_column_name):
    """
    Adds a column to the dataframe with a new name copying
    all the values from the existing column
    """
    df = df.withColumn(new_column_name, df[existing_column_name])

    return df