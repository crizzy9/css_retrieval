HOW TO RUN AND EXECUTE THE PYTHON PROJECT:
1) Install python 3.5
2) Install pycharm
3) Run the main.py file
4) The results will be stored in results directory according the file structure below

N.B : The imports used are src. to maintain the file structure

There are 3 modes in every model
mode 0 : normal
mode 1 : Stopping
mode 2 : Stemming


HOW TO RUN LUCENE PROGRAM
1) Install Java 8
2) Install Eclipse IDE
3) Download Lucene 4.7.2 (the required jar files are inside Shyam_Padia_TuTh_HW4/lucene/jar_files)
4) Add the following as reference libraries for the project
	-lucene-­core-4.7.2.jar
	-lucene-queryparser-4.7.2.jar
	-lucene-analyzers-common-4.7.2.jar
5) Run the Lucene.java file and provide the required paths


File structure:

- corpus
    - cacm (the raw corpus that is given)
    - parsed (parsed documents)
    - stemmed (stemmed parsed documents)
- data (data that is given)
    - cacm.query.parsed.txt (queries after parsing)
    - cacm.query.txt
    - cacm.rel.txt
    - cacm_stem.query.txt
    - cacm_stem.txt
    - common_words
- index (index is stored in pickle format for better compression and extraction)
    - index.pickle
    - stem.index.pickle
- results
    - eval (contains evaluation for all models)
        - bm25
            - bm25_map_mrr (format: map mrr)
            - bm25_p_at_5 (format: query_id precision_at_5)
            - bm25_p_at_20 (format: query_id precision_at_20)
            - bm25_precision (format: query_id rank doc_id precision_so_far relevant/non-relevant)
            - bm25_recall (format: query_id rank doc_id recall_so_far relevant/non-relevant)
        - bm25_stop
        - lucene
        - sqlm (Smoothed query likelihood model)
        - sqlm_prf
        - sqlm_stop
        - tfidf
        - tfidf_stop
    - ranking (contains top 100 matches for all queries using all models in TREC format)
    - snippets (contains snippets generated for all queries and their top 100 matches)
        - qid
            - doc-id
- src
    - lucene
        - Lucene.java
    - config.ini (contains the configurations for the project which is used throughout the project)
    - main.py
    - helpers.py
    - data_parser.py
    - doc_parser.py
    - query_parser.py
    - evaluator.py
    - indexer.py
    - result_writer.py
    - prf.py
    - bm25.py
    - sqlm.py
    - tfidf.py
    - snippet_generator.py (results are stored in .html documents)
- .gitignore
- README.md


Created by
Chetan, Shyam, Shaurya
