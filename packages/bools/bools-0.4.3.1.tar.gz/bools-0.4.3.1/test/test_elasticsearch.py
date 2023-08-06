import unittest
import pandas as pd
from bools.dbc import ElasticSearch

pd.set_option('display.max_columns', 500)


class ElasticSearchTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        data = pd.read_csv('C:/Users/cb229/Desktop/1231.csv')
        data = data[filter(lambda x: not x.startswith('_'), data.columns)]
        data['datetime'] = pd.to_datetime(data.pop('timestamp'))
        data['date'] = pd.to_datetime(data['date'], utc=True)
        data['date_uct+8'] = data['date'].apply(lambda x: x.tz_convert('Asia/shanghai'))
        data['resp_time'] = data['resp_time'].apply(lambda x: x.replace(',', ''))
        data['index'] = ['test-2020-12-14', 'test-2020-12-13'] * (data.shape[0] // 2) + ['test-2020-12-13']
        self.data = data
        print(data.shape)
        # print(data.head())
        """
        self.es = ElasticSearch(base_url='http://elastic:cb1998827@localhost:9200', patch_pandas=True)
        # self.es.delete('test*')

    @classmethod
    def test_init(cls):
        # ElasticSearch()
        # print(ElasticSearch(base_url='http://elastic:cb1998827@localhost:9200').version)
        # ElasticSearch(host='http://10.0.80.167', patch_pandas=False)
        # ElasticSearch(user='elastic', password='cb1998827', patch_pandas=True)
        pass

    def test_write(self):
        # self.es.delete('test*')
        # self.es.write('test', [{'a': 1, 'b': 2}] * 20000)
        pass

    def test_es_write(self):
        self.es.delete('test')
        pd.DataFrame({'a': [1, 2] * 20, 'b': range(40)}).to_es(index='test')
        # self.data.to_es(numeric_detection=True, index='test')
        pass

    def test_query(self):
        # self.es.delete('test*')
        # pd.DataFrame({'a': [1, 2] * 20000, 'b': range(40000)}).to_es(index='test')
        # assert len(self.es.query('test', {
        #     "size": 2000,
        #     "query": {
        #         "terms": {
        #             "a": [1]
        #         }
        #     }
        # })['hits']['hits']) == 2000
        len_ = len(self.es.scroll_query('test', {
            "query": {
                "terms": {
                    "a": [1]
                }
            }
        })['hits']['hits'])
        print(len_)
        assert len_ == 20000

    def test_read_es(self):
        print(pd.read_es('test', {
            "query": {
                "terms": {
                    "a": [1]
                }
            }
        }))

    def test_create_or_cover(self):
        print(self.es.create_or_cover('test', {'a': 2}, doc_id='test'))


if __name__ == '__main__':
    unittest.main()
