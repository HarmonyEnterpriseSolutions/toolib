#!/usr/bin/python2

#
# Yapps 2 - yet another python parser system
# Copyright 1999-2003 by Amit J. Patel <amitp@cs.stanford.edu>
#
# This version of Yapps 2 can be distributed under the
# terms of the MIT open source license, either found in the LICENSE file
# included with the Yapps distribution
# <http://theory.stanford.edu/~amitp/yapps/> or at
# <http://www.opensource.org/licenses/mit-license.php>
#

import os
import sys
import toolib.text.yapps.yappsrt as yappsrt

def generate(inputfilename, outputfilename='', lazy=False, dump=0, use_devel_grammar=0, **flags):
    """Generate a grammar, given an input filename (X.g)
    and an output filename (defaulting to X.py)."""
    if (lazy and outputfilename 
        and os.path.exists(outputfilename)
        and os.path.exists(inputfilename)
        and os.stat(outputfilename).st_mtime > os.stat(inputfilename).st_mtime):
        return

    if use_devel_grammar:
        import toolib.text.yapps.yapps_grammar as grammar
    else:
        import toolib.text.yapps.grammar as grammar

    if not outputfilename:
        if inputfilename.endswith('.g'):
            outputfilename = inputfilename[:-2] + '.py'
        else:
            raise Exception('Must specify output filename if input filename is not *.g')
        
    DIVIDER = '\n%%\n' # This pattern separates the pre/post parsers
    preparser, postparser = None, None # Code before and after the parser desc

    # Read the entire file
    s = open(inputfilename,'r').read()

    # See if there's a separation between the pre-parser and parser
    f = s.find(DIVIDER)
    if f >= 0: preparser, s = s[:f]+'\n\n', s[f+len(DIVIDER):]

    # See if there's a separation between the parser and post-parser
    f = s.find(DIVIDER)
    if f >= 0: s, postparser = s[:f], '\n\n'+s[f+len(DIVIDER):]

    # Create the parser and scanner and parse the text
    scanner = grammar.ParserDescriptionScanner(s)
    if preparser: scanner.first_line_number = 1 + preparser.count('\n')
    parser = grammar.ParserDescription(scanner)
    t = yappsrt.wrap_error_reporter(parser, 'Parser')
    if t is None: return # Failure
    if preparser is not None: t.preparser = preparser
    if postparser is not None: t.postparser = postparser

    # Add command line options to the set
    t.options.update(flags)
            
    # Generate the output
    if dump:
        t.dump_information()
    else:
        t.output = open(outputfilename, 'w')
        t.generate_output()

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser("%prog [options] input.g [output.py]")

    parser.add_option("-d", "--dump", 
                      action="store_true", dest="dump",
                      help="Dump out grammar information",
    )
    
    parser.add_option("", "--use-devel-grammar", 
                      action="store_true", dest="use_devel_grammar",
                      help="Use the devel grammar parser from yapps_grammar.py"
                           " instead of the stable grammar from grammar.py",
    )

    parser.add_option("", "--context-insensitive-scanner", 
                      action="store_true", dest="context_insensitive_scanner",
                      help="Scan all tokens (see docs)",
    )

    parser.add_option("", "--lazy", 
                      action="store_true", dest="lazy",
                      help="Compile only if input is more recent than output",
    )

    options, files = parser.parse_args()

    if not files or len(files) > 2:
        parser.error("Use --help for details.")
    else:
        # is it safe to use options.__dict__?
        generate(*files, **options.__dict__)
