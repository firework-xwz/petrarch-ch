import sys
import os
from argparse import Namespace

from FromCorenlpConverter import FromCorenlpConverter
from petrarch2.petrarch2 import main as petrarch2_main


if __name__ == "__main__":
    # If you are using python2, the first two lines are needed.
    reload(sys)
    sys.setdefaultencoding('utf-8')
    file_name = 'test'
    input_path = 'input/'
    output_path = 'output/'
    corenlp_path = 'stanford-corenlp-full-2018-10-05'
    port = 400

    converter = FromCorenlpConverter(input_path + file_name + '.txt', '', corenlp_path, port)
    
    converter.run()

    converter.__del__()

    args = Namespace(command_name='batch', config=None, inputs=output_path + file_name + '.xml', nullactors=False, nullverbs=False, outputs=output_path + file_name + '_result.txt')
    # args = Namespace(command_name='batch', config=None, inputs='petrarch2/test-ch2.xml', nullactors=False, nullverbs=False, outputs=output_path + 'test-ch2' + '_result.txt')
    petrarch2_main(args)



