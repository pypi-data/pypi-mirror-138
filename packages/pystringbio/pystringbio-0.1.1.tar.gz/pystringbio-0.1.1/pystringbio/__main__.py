"""STRING manipulation tool and microservice

Usage:
    pystringbio server start <mapper_tsv_file> [--rh=<redis_host> --rp=<redis_port>]
    pystringbio load mapper <mapper_tsv_file> [--rh=<redis_host> --rp=<redis_port>]
    pystringbio load ppi <interactions_tsv_file> [--rh=<redis_host> --rp=<redis_port>]
   
Options:
  -h --help     Show this screen.
  --rp=<redis_port>  redis DB TCP port [default: 6379]
  --rh=<redis_host>  redis DB http adress [default: localhost]
"""

from docopt import docopt
from .io.mapping import parseMappingRulesFile
from .io.interactions import parseInteractionFile

from .client import loadMappingRules, loadInteractionData


## Run a service 
# just start
# use cli to do any add
# core/
# cli/ 
# comptibl

args = docopt(__doc__)

if args["mapper"]:
    mRules = parseMappingRulesFile(args['<mapper_tsv_file>'])
    loadMappingRules(mRules)

if args["ppi"]:
    ppiData = parseInteractionFile(args['<interactions_tsv_file>'])
    loadInteractionData(ppiData)
    