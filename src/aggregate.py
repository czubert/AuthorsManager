import shutil
import pandas as pd

# import src.utils as utils
import utils as utils


# Reading lists as DataFrames
def read_lists_as_df(file_names):
    lists_as_df = []
    for file_name in file_names:
        lists_as_df.append(utils.read_csv_as_df(file_name))
        # todo check if this file already exists in "after_update" if yes then delete it
        shutil.move(file_name, 'after_update')
    return lists_as_df


def concat_all_authors(main_file, lists_as_df):
    for auth_list in lists_as_df:
        auth_list.sort_values('num_of_publications', ascending=False, inplace=True)
        auth_list['sent'] = 0  # adding a column about mail status, if the mail has been sent

        main_file = pd.concat((main_file, auth_list), ignore_index=True)
    return main_file


def aggregate_data(df: pd.DataFrame):
    """
    Getting rid of repetitions and group by email
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    df.drop_duplicates(inplace=True)
    df.sort_values('num_of_publications', inplace=True)

    column_map = {col: "first" for col in df.columns}
    column_map["num_of_publications"] = "sum"
    column_map["sent"] = "sum"

    # Groups authors by eamil
    df.groupby(["email"], as_index=False).agg(column_map)

    # Removing records of the same author with different email
    df = df.drop_duplicates(['name', 'surname'], keep='first')
    df.sort_values('num_of_publications', ascending=False, inplace=True)
    df.loc[:, ['num_of_publications', 'sent']].astype('int')
    return df



