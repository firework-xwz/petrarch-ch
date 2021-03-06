import glob
import logging
import json
from stanfordcorenlp import StanfordCoreNLP
from PetrXmlConverter import *


class FromCorenlpConverter(PetrXmlConverter):
    def __init__(self, input_path, output_path='', corenlp_path='', port=8000, memory='4g', lang='zh', timeout=1500,
                 quiet=True, logging_level=logging.WARNING):
        PetrXmlConverter.__init__(self, input_path, output_path)

        self.corenlp_path = corenlp_path
        if self.corenlp_path == '' and not self.find_corenlp():
            raise IOError('Could not find stanford corenlp.')
        self.nlp = StanfordCoreNLP(self.corenlp_path, port, memory, lang, timeout, quiet, logging_level)

        print('\033[1;32m'+'Starting up StanfordCoreNLP...'+'\033[0m')

    def __del__(self):
        self.nlp.close()
        print('\033[1;32m'+'Corenlp closed!'+'\033[0m')

    def generate_events(self):
        with open(self.input_path, 'r') as source:
            for line in source.readlines():
                if not len(line) == 0:
                    properties = line.replace('\n', '').split('|')
                    event = {
                        Attr.id: properties[0],
                        Attr.date: properties[4].split(' ')[0].replace('-', ''),
                        Attr.source: properties[6],
                        Attr.url: properties[9]
                    }
                    content = re.sub(r'\s', '', properties[8])
                    # parse = self.parse(content)
                    # event[Attr.content] = self.sep_sentence(parse)
                    event[Attr.content] = self.sep_sentence(content)
                    print('parse event {0}'.format(event[Attr.id]))
                    self.events.append(event)

    def parse(self, text):
        return self.nlp.parse(text)

    def find_corenlp(self):
        corenlp_paths = glob.glob("stanford-corenlp-full-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]")
        if len(corenlp_paths) == 0:
            return False
        else:
            corenlp_paths.sort()
            self.corenlp_path = corenlp_paths[-1]
            return True
