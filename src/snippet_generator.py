import os
from src.data_parser import DataParser
from src.helpers import load_config, abspath, read_file, parse_stuff
from collections import Counter
import pprint


class SnippetGenerator:

    def __init__(self, query):
        config = load_config()
        self.raw_docs = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'raw_docs'))
        self.parsed_dir = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'parsed_dir'))
        common_words = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'common_words'))
        self.stoplist = []
        with open(common_words, 'r') as f:
            self.stoplist = f.read().split('\n')
        self.significant_words = set([term for term in query.split() if term not in self.stoplist])
        print("Significant words")
        print(self.significant_words)
        self.dataparser = DataParser()

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

    def get_snippet(self, docs):
        pp = pprint.PrettyPrinter(indent=4)

        parsed_sentences = {}
        org_sentences = {}
        snippets = {}
        for doc in docs:
            content = read_file(os.path.join(self.raw_docs, 'CACM-' + doc + '.html'))
            self.dataparser.initialize()
            self.dataparser.feed(content)
            data = []
            org_data = self.dataparser.get_data()[3].split('\n\n')[2:-2]

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
                        for i in range(len(words)):
                            if words[i] in sig_words:
                                if first_sig is None:
                                    first_sig = i
                                    sig_count += 1
                                elif non_sig_count <= 4:
                                    last_sig = i
                                    sig_count += 1
                            elif first_sig is not None and non_sig_count <= 4:
                                non_sig_count += 1
                        if first_sig is not None and last_sig > first_sig:
                            sig_factor = sig_count**2/(last_sig - first_sig)
                            # snippets.setdefault(doc, []).append((sent.strip(), sig_factor, portion_index, sent_index))
                            snippets.setdefault(doc, []).append((org_sentences[doc][portion_index][sent_index].strip(), sig_factor))
                            # print(doc)
                            # print("word match: Doc = {}, firstSig={}, lastSig={}, sigCount={}, nonSigCount={}, sigFactor={}".format(doc, first_sig, last_sig, sig_count, non_sig_count, sig_factor))
                            # print(words)
                            # print(words[first_sig: last_sig+1])
                            # print(sent)

        # print(org_sentences)
        # print(parsed_sentences)
        # print(snippets)
        for doc in snippets.keys():
            snippets[doc] = sorted(snippets[doc], key=lambda k: k[1], reverse=True)
        pp.pprint(snippets)


# Implementation
query1 = 'what articles exist which deal with tss time sharing system an operating system for ibm computers'
query2 = parse_stuff('Interested in articles on robotics, motion planning particularly the geometric and combinatorial aspects.  We are not interested in the dynamics of arm motion.')
snippet_generator = SnippetGenerator(query1) #q2
docs1 = ['2312', '0195', '0248', '2578', '2313', '1010', '0494']
docs2 = ['1605', '1572', '2319', '1410', '2379', '1033', '1519']
docs3 = ['2078', '2828', '1543']
snippet_generator.get_snippet(docs2) #d3
