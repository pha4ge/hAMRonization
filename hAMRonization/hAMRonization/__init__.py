#!/usr/bin/env/python

from hAMRonization.hAMRonizedResult import hAMRonizedResult

from hAMRonization import AbricateIO
#from hAMRonization import AribaIO
#from hAMRonization import AmrFinderPlusIO
#from hAMRonization import RgiIO
#from hAMRonization import ResFinderIO
#from hAMRonization import SraxIO
#from hAMRonization import DeepArgIO
#from hAMRonization import KmerResistanceIO
#from hAMRonization import Srst2IO
#from hAMRonization import GrootIO
#from hAMRonization import StarAmrIO
#from hAMRonization import CSStarIO
#from hAMRonization import AmrPlusPlusIO
#from hAMRonization import ResFamsIO


_FormatToIterator = {
    "abricate": AbricateIO.AbricateIterator,
    #"ariba": AribaIO.AribaIterator,
    #"amrfinderplus": AmrFinderPlusIO.AmrFinderPlusIterator,
    #"rgi": RgiIO.RgiIterator,
    #"resfinder": ResFinderIO.ResFinderIterator,
    #"srax": SraxIO.SraxIterator,
    #"deeparg": DeepArgIO.DeepArgIterator,
    #"kmerresistance": KmerResistanceIO.KmerResistanceIterator,
    #"srst2": Srst2IO.Srst2Iterator,
    #"groot": GrootIO.GrootIterator,
    #"staramr": StarAmrIO.StarAmrIterator,
    #"csstar": CSStarIO.CSStarIterator,
    #"amrplusplus": AmrPlusPlusIO.AmrPlusPlusIterator,
    #"resfams": ResFamsIO.ResFamsIterator
    }

def parse(handle, tool):
    r"""Turn a sequence file into an iterator returning SeqRecords.
    Arguments:
     - handle   - handle to the file, or the filename as a string
     - tool - lower case string describing the file format.
    Typical usage, opening a file to read in, and looping over the record(s):
    >>> from hAMRonization import AmrIO
    >>> filename = "abricate_report.tsv"
    >>> for result in AmrIO.parse(filename, "abricate"):
    ...    print(record)

    """
    if not isinstance(tool, str):
        raise TypeError("Need a string for the file format (lower case)")
    if not tool:
        raise ValueError("Tool required (lower case string)")
    if not tool.islower():
        raise ValueError(f"Tool string '{tool}' should be lower case")

    iterator_generator = _FormatToIterator.get(tool)
    if iterator_generator:
        return iterator_generator(handle)
    raise ValueError(f"Unknown tool: {tool}\nMust be in {_FormatToIterator.keys()")
