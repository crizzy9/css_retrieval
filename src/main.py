from src.indexer import Indexer
from src.query_parser import QueryParser
from src.tfidf import TFIDF
from src.sqlm import SQLM
from src.helpers import load_config
from src.prf import PRF
from src.doc_parser import Parser
from src.result_writer import ResultWriter
from src.evaluator import Evaluator
import time
from src.BM25 import BM25

start_time = time.time()

config = load_config()

parser = Parser()
parser.parse_documents()

indexer = Indexer(mode=1)
indexer.create()
indexer.save_index()
index = indexer.get_index()

queries = QueryParser().get_queries()

tfidf = TFIDF(mode=1)
tfidf_stop = TFIDF(mode=2)
sqlm = SQLM(mode=1)
sqlm_stop = SQLM(mode=2)
sqlm_prf = PRF(sqlm)
# bm25 = BM25(mode=1).bm25()

rw = ResultWriter()
results_file_tfidf = config.get('FILES', 'results_tfidf')
results_file_tfidf_stop = config.get('FILES', 'results_tfidf_stop')
results_file_sqlm = config.get('FILES', 'results_sqlm')
results_file_sqlm_stop = config.get('FILES', 'results_sqlm_stop')
results_file_sqlm_prf = config.get('FILES', 'results_sqlm_prf')
results_file_bm25 = config.get('FILES', 'results_bm25')

print()

for query_id in queries:
    print('Scoring documents for query:' + str(query_id) + '...', end='')
    query = queries[query_id]
    score_tfidf = tfidf.scores(query)
    score_tfidf_stop = tfidf_stop.scores(query)
    score_sqlm = sqlm.scores(query)
    score_sqlm_stop = sqlm_stop.scores(query)
    score_sqlm_prf = sqlm_prf.scores(query)
    rw.results_to_file(results_file_tfidf, query_id, score_tfidf, 'tfidf')
    rw.results_to_file(results_file_tfidf_stop, query_id, score_tfidf_stop, 'tfidf_stop')
    rw.results_to_file(results_file_sqlm, query_id, score_sqlm, 'sqlm')
    rw.results_to_file(results_file_sqlm_stop, query_id, score_sqlm_stop, 'sqlm_stop')
    rw.results_to_file(results_file_sqlm_prf, query_id, score_sqlm_prf, 'sqlm_prf')
    print('Done')

print()

eval_tfidf = Evaluator(results_file_tfidf)
eval_tfidf_stop = Evaluator(results_file_tfidf_stop)
eval_sqlm = Evaluator(results_file_sqlm)
eval_sqlm_stop = Evaluator(results_file_sqlm_stop)
eval_sqlm_prf = Evaluator(results_file_sqlm_prf)
# eval_bm25 = Evaluator(results_file_bm25)

print('Evaluating results for tf.idf...', end='')
eval_tfidf.evaluate()
eval_tfidf.eval_to_file('tfidf')
print('Done')

print('Evaluating results for tf.idf with stopping...', end='')
eval_tfidf_stop.evaluate()
eval_tfidf_stop.eval_to_file('tfidf_stop')
print('Done')

print('Evaluating results for Smoothed Query Likelihood...', end='')
eval_sqlm.evaluate()
eval_sqlm.eval_to_file('sqlm')
print('Done')

print('Evaluating results for Smoothed Query Likelihood with stopping...', end='')
eval_sqlm_stop.evaluate()
eval_sqlm_stop.eval_to_file('sqlm_stop')
print('Done')

print('Evaluating results for Smoothed Query Likelihood with Pseudo Relevance Feedback...', end='')
eval_sqlm_prf.evaluate()
eval_sqlm_prf.eval_to_file('sqlm_prf')
print('Done')

# print('Evaluating results for BM25...', end='')
# eval_bm25.eval_to_file('bm25')
# print('Done')

end_time = time.time()

print('***********************************************')
print('Execution time: ' + str(end_time - start_time))






