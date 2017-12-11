import os
from src.data_parser import DataParser
from src.helpers import load_config, abspath, read_file, parse_stuff, get_stoplist, create_dir
from collections import Counter


class SnippetGenerator:

    def __init__(self, query, scores):
        config = load_config()
        self.raw_docs = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'raw_docs'))
        self.parsed_dir = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'parsed_dir'))
        self.stoplist = get_stoplist()
        self.significant_words = set([term for term in query.split() if term not in self.stoplist])

        self.dataparser = DataParser()
        self.snippets = {}
        self.snippet_dir = abspath(config.get('DIRS', 'results'), config.get('DIRS', 'snippet_dir'))
        create_dir(self.snippet_dir)
        self.doc_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:100]
        self.titles = {}

    # using luhns formula to get medium frequency words from the document
    def get_freq_terms(self, doc):
        data = read_file(os.path.join(self.parsed_dir, 'CACM-' + doc + '.txt'))
        words = data.split()
        doc_len = len(words)/15
        word_freq = Counter(words)
        sig_words = []

        if doc_len < 25:
            threshold = 7 - 0.1*(25 - doc_len)
        elif 25 <= doc_len <= 40:
            threshold = 7
        else:
            threshold = 7 + 0.1*(doc_len - 40)

        for word in word_freq.keys():
            if word_freq[word] >= threshold:
                sig_words.append(word)

        return sig_words

    def get_snippet(self):

        parsed_sentences = {}
        org_sentences = {}
        for item in self.doc_scores:
            doc = item[0]
            content = read_file(os.path.join(self.raw_docs, 'CACM-' + doc + '.html'))
            self.dataparser.initialize()
            self.dataparser.feed(content)
            data = []
            dataparser_op = self.dataparser.get_data()
            end = len(dataparser_op)
            for i in range(end):
                if dataparser_op[i] == 'pre':
                    end = i
            if end > 3:
                org = " ".join(dataparser_op[3:end]).split('\n\n')
            else:
                org = dataparser_op[3].split('\n\n')

            self.titles[doc] = org[1]
            org_data = org[2:-2]

            # parsing document
            for line in org_data:
                data.append(parse_stuff(line, period=True))

            parsed_sentences[doc] = [line.split('.') for line in data]
            org_sentences[doc] = [line.split('.') for line in org_data]

            sig_words = self.significant_words.union(set(self.get_freq_terms(doc)))

            for portion_index in range(len(parsed_sentences[doc])):
                portion = parsed_sentences[doc][portion_index]
                for sent_index in range(len(portion)):
                    sent = portion[sent_index]
                    # print("Doc = {}, Data = {}".format(doc, sent))
                    if sent:
                        words = sent.strip().split()
                        first_sig = None
                        last_sig = 0
                        sig_count = 0
                        non_sig_count = 0
                        max_non_sig = 20
                        for i in range(len(words)):
                            if words[i] in sig_words:
                                if first_sig is None:
                                    first_sig = i
                                    sig_count += 1
                                elif non_sig_count <= max_non_sig:
                                    last_sig = i
                                    sig_count += 1
                            elif first_sig is not None and non_sig_count <= max_non_sig:
                                non_sig_count += 1
                        cts = Counter([sig_words.__contains__(word) for word in words])
                        if first_sig is not None and last_sig > first_sig:
                            sig_factor = sig_count**2/(last_sig - first_sig)
                        elif cts[True]:
                            sig_factor = cts[True]/max_non_sig
                        else:
                            sig_factor = 0
                        self.snippets.setdefault(doc, []).append(
                            (org_sentences[doc][portion_index][sent_index].strip(), sig_factor))

        for doc in self.snippets.keys():
            self.snippets[doc] = sorted(self.snippets[doc], key=lambda k: k[1], reverse=True)

    # results -> snippets -> QueryID -> Rank_DocumentID.html
    def save_snippets(self, qno):
        create_dir(os.path.join(self.snippet_dir, str(qno)))
        notfound = []
        for i in range(len(self.doc_scores)):
            doc = self.doc_scores[i][0]
            if not self.snippets.get(doc):
                notfound.append(doc)
                continue
            snips = self.snippets[doc]
            with open(os.path.join(self.snippet_dir, str(qno), 'Rank_' + str(i+1) + '_' + doc + '.html'), 'w+') as f:
                f.write('<html><pre><h2>' + self.titles[doc] + '</h2>')
                for j in range(len(snips[:2])):
                    f.write('<div>Snippet ' + str(j+1) + ':<p>')
                    for word in snips[j][0].replace('\n', ' <br>').split():
                        if parse_stuff(word.lower()) in self.significant_words:
                            f.write('<b>' + word + '</b> ')
                        else:
                            f.write(word + ' ')
                    f.write('</p></div>')
                f.write('</pre></html>')
        if notfound:
            print("Snippets not found for {} ... {}".format(len(notfound), notfound))


# Implementation
# snippet_generator = SnippetGenerator(query, docs)
# snippet_generator.get_snippet()
# snippet_generator.save_snippets(1)
