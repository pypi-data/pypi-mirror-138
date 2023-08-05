from enginelib.rds.client import db_name, db_client
from enginelib.errors import Error

from functools import lru_cache


class ProviderTaxonomyCrosswalk:
    @staticmethod
    @lru_cache()
    def medicare_specialty_code(taxonomy: str) -> str:
        query = f'''
        SELECT "medicare_specialty_code" 
            FROM {db_name}.ptxw_records 
            WHERE "provider_taxonomy_code"='{taxonomy}' 
        LIMIT 1;
        '''

        try:
            records, err = db_client.GetReferenceData('transaction_id', query)
            records = records or list()
            if records:
                return records[0]['medicare_specialty_code'].strip()

        except (IndexError, KeyError, TypeError):
            pass

        raise Error('Could not fetch data from Provider Taxonomy Crosswalk'
                    f' reference data set for taxonomy code {taxonomy}.')
