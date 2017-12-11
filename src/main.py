import time
from src.indexer import Indexer
from src.query_parser import QueryParser
from src.tfidf import TFIDF
from src.sqlm import SQLM
from src.helpers import load_config
from src.prf import PRF
from src.doc_parser import Parser
from src.result_writer import ResultWriter
from src.evaluator import Evaluator
from src.BM25 import BM25
from src.snippet_generator import SnippetGenerator

start_time = time.time()

config = load_config()

parser = Parser()
parser.parse_documents()
parser.stem_parse_documents()

print('Creating index...')
indexer = Indexer(mode=0)
indexer.create()
indexer.save_index()
index = indexer.get_index()
print()

print('Creating stemmed index...')
indexer_stem = Indexer(mode=2)
indexer_stem.create()
indexer_stem.save_index()
index_stem = indexer_stem. get_index()
print()

qp = QueryParser()
queries = qp.get_queries()
queries_stem = qp.get_stem_queries()

tfidf = TFIDF(mode=0)
tfidf_stop = TFIDF(mode=1)
tfidf_stem = TFIDF(mode=2)
sqlm = SQLM(mode=0)
sqlm_stop = SQLM(mode=1)
sqlm_stem = SQLM(mode=2)
sqlm_prf = PRF(sqlm)
bm25 = BM25(mode=0)
bm25_stop = BM25(mode=1)
bm25_stem = BM25(mode=2)

rw = ResultWriter()
results_file_tfidf = config.get('FILES', 'results_tfidf')
results_file_tfidf_stop = config.get('FILES', 'results_tfidf_stop')
results_file_tfidf_stem = config.get('FILES', 'results_tfidf_stem')
results_file_sqlm = config.get('FILES', 'results_sqlm')
results_file_sqlm_stop = config.get('FILES', 'results_sqlm_stop')
results_file_sqlm_stem = config.get('FILES', 'results_sqlm_stem')
results_file_sqlm_prf = config.get('FILES', 'results_sqlm_prf')
results_file_bm25 = config.get('FILES', 'results_bm25')
results_file_bm25_stop = config.get('FILES', 'results_bm25_stop')
results_file_bm25_stem = config.get('FILES', 'results_bm25_stem')
results_file_lucene = config.get('FILES', 'results_lucene')

results_tfidf = []
results_tfidf_stop = []
results_tfidf_stem = []
results_sqlm = []
results_sqlm_stop = []
results_sqlm_stem = []
results_sqlm_prf = []
results_bm25 = []
results_bm25_stop = []
results_bm25_stem = []

print()

for query_id in queries:
    print('Scoring documents for query:' + str(query_id) + '...')

    query = queries[query_id]
    score_tfidf = tfidf.scores(query)
    score_tfidf_stop = tfidf_stop.scores(query)
    score_sqlm = sqlm.scores(query)
    score_sqlm_stop = sqlm_stop.scores(query)
    score_sqlm_prf = sqlm_prf.scores(query)
    score_bm25 = bm25.scores(query_id, query)
    score_bm25_stop = bm25_stop.scores(query_id, query)

    results_tfidf.append(score_tfidf)
    results_tfidf_stop.append(score_tfidf_stop)
    results_sqlm.append(score_sqlm)
    results_sqlm_stop.append(score_sqlm_stop)
    results_sqlm_prf.append(score_sqlm_prf)
    results_bm25.append(score_bm25)
    results_bm25_stop.append(score_bm25_stop)

    # generating snippets
    snippet_generator = SnippetGenerator(query, score_sqlm)
    snippet_generator.get_snippet()
    snippet_generator.save_snippets(query_id)

print('...Done')
print()

for query_id in queries_stem:
    print('Scoring documents for stemmed query:' + str(query_id))

    query = queries_stem[query_id]
    score_tfidf_stem = tfidf_stem.scores(query)
    score_sqlm_stem = sqlm_stem.scores(query)
    score_bm25_stem = bm25_stem.scores(query_id, query)

    results_tfidf_stem.append(score_tfidf_stem)
    results_sqlm_stem.append(score_sqlm_stem)
    results_bm25_stem.append(score_bm25_stem)

print('...Done')
print()

rw.results_to_file(results_file_tfidf, results_tfidf, 'tfidf')
rw.results_to_file(results_file_tfidf_stop, results_tfidf_stop, 'tfidf_stop')
rw.results_to_file(results_file_tfidf_stem, results_tfidf_stem, 'tfidf_stem')
rw.results_to_file(results_file_sqlm, results_sqlm, 'sqlm')
rw.results_to_file(results_file_sqlm_stop, results_sqlm_stop, 'sqlm_stop')
rw.results_to_file(results_file_sqlm_stem, results_sqlm_stem, 'sqlm_stem')
rw.results_to_file(results_file_sqlm_prf, results_sqlm_prf, 'sqlm_prf')
rw.results_to_file(results_file_bm25, results_bm25, 'bm25')
rw.results_to_file(results_file_bm25_stop, results_bm25_stop, 'bm25_stop')
rw.results_to_file(results_file_bm25_stem, results_bm25_stem, 'bm25_stem')

eval_tfidf = Evaluator(results_file_tfidf, 'tfidf')
eval_tfidf_stop = Evaluator(results_file_tfidf_stop, 'tfidf_stop')
eval_sqlm = Evaluator(results_file_sqlm, 'sqlm')
eval_sqlm_stop = Evaluator(results_file_sqlm_stop, 'sqlm_stop')
eval_sqlm_prf = Evaluator(results_file_sqlm_prf, 'sqlm_prf')
eval_bm25 = Evaluator(results_file_bm25, 'bm25')
eval_bm25_stop = Evaluator(results_file_bm25_stop, 'bm25_stop')
eval_lucene = Evaluator(results_file_lucene, 'lucene')

print('Evaluating results for tf.idf...', end='')
eval_tfidf.evaluate()
eval_tfidf.eval_to_file()
print('Done')

print('Evaluating results for tf.idf with stopping...', end='')
eval_tfidf_stop.evaluate()
eval_tfidf_stop.eval_to_file()
print('Done')

print('Evaluating results for Smoothed Query Likelihood...', end='')
eval_sqlm.evaluate()
eval_sqlm.eval_to_file()
print('Done')

print('Evaluating results for Smoothed Query Likelihood with stopping...', end='')
eval_sqlm_stop.evaluate()
eval_sqlm_stop.eval_to_file()
print('Done')

print('Evaluating results for Smoothed Query Likelihood with Pseudo Relevance Feedback...', end='')
eval_sqlm_prf.evaluate()
eval_sqlm_prf.eval_to_file()
print('Done')

print('Evaluating results for BM25...', end='')
eval_bm25.evaluate()
eval_bm25.eval_to_file()
print('Done')

print('Evaluating results for BM25 with stopping...', end='')
eval_bm25_stop.evaluate()
eval_bm25_stop.eval_to_file()
print('Done')

print('Evaluating results for Lucene...', end='')
eval_lucene.evaluate()
eval_lucene.eval_to_file()
print('Done')

end_time = time.time()

print('***********************************************')
print('Execution time: ' + str(end_time - start_time) + 's')






