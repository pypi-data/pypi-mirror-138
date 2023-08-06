import pandas as pd
import numpy as np
from src.dvgroup_factory.etl.greenplum_utils import GreenplumUtils


class CopyUtils:

    @staticmethod
    def gp2ch(src_table: str, dst_table: str, factory, cols_map=None, types_map=None, gp_db='dvault', ch_db='db1', batch_size=1_000_000):
        """
        Copy table from greenplum aka gp to clickhouse aka ch in batch_mode
        :param src_table: src table name from gp
        :param dst_table: dst table name from ch
        :param factory: factory instance
        :param cols_map: column name relation between gp and ch
        :param gp_db: gp database name
        :param ch_db: ch database name
        :param batch_size: size of batch
        :return:
        """
        offset = 0
        ch_client = factory.clickhouse_client(new=True, settings={'use_numpy': True})
        with factory.gp_connection(new=True, dbname=gp_db) as conn:
            select_query = f"""
                select
                    {','.join(cols_map.keys()) if cols_map else '*'}
                from {src_table}
                limit {batch_size} offset %s
            """
            data_df = pd.read_sql_query(select_query % offset, conn)
            while data_df.shape[0] > 0:
                offset += batch_size
                data_df = data_df.astype(types_map)
                data_df = data_df.astype(str)
                data_df.fillna('', inplace=True)
                if cols_map:
                    data_df.rename(columns=cols_map, inplace=True)
                ch_client.insert_dataframe(f"INSERT INTO {ch_db}.{dst_table} VALUES", data_df)
                data_df = pd.read_sql_query(select_query % offset, conn)

    @staticmethod
    def ch2gp(src_table: str, dst_table: str, factory, cols_map=None, types_map=None, ch_db='db1', gp_db='dvault', batch_size=1_000_000):
        """
        Copy table from clickhouse aka ch to greenplum aka gp in batch_mode
        :param src_table: src table name from ch
        :param dst_table: dst table name from gp
        :param factory: factory instance
        :param cols_map: column name relation between gp and ch
        :param ch_db: ch database name
        :param gp_db: gp database name
        :param batch_size: size of batch
        :return:
        """
        offset = 0
        ch_client = factory.clickhouse_client(new=True, settings={'use_numpy': True})
        select_query = f"""
            SELECT {','.join(cols_map.keys()) if cols_map else '*'}
            FROM {ch_db}.{src_table} LIMIT {batch_size} OFFSET %s
        """
        data_df = ch_client.query_dataframe(select_query % offset)
        data_df = data_df.astype(types_map)
        data_df = data_df.astype(str)
        data_df.fillna('')
        if cols_map:
            data_df.rename(columns=cols_map, inplace=True)
        while data_df.shape[0] > 0:
            with factory.gp_connection(new=True, dbname=gp_db) as conn:
                GreenplumUtils.insert_dataframe(data_df, conn, dst_table)
            data_df = ch_client.query_dataframe(select_query % offset)
            if cols_map:
                data_df.rename(cols_map, inplace=True)
            data_df = data_df.astype(str)
            data_df.fillna('')