from html.parser import HTMLParser


class DataParser(HTMLParser):
    data = []

    # always initialize before parsing new stuff
    def initialize(self):
        self.data = []

    def handle_starttag(self, tag, attrs):
        self.data.append(tag)

    def handle_endtag(self, tag):
        self.data.append(tag)

    def handle_data(self, data):
        self.data.append(data)

    def get_data(self):
        return self.data
