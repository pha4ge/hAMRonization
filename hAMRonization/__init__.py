#!/usr/bin/env python

__version__ = "1.1.0"

from hAMRonization import AbricateIO
from hAMRonization import AmrFinderPlusIO
from hAMRonization import AribaIO
from hAMRonization import RgiIO
from hAMRonization import ResFinderIO
from hAMRonization import SraxIO
from hAMRonization import DeepArgIO
from hAMRonization import KmerResistanceIO
from hAMRonization import Srst2IO
from hAMRonization import GrootIO
from hAMRonization import StarAmrIO
from hAMRonization import CSStarIO
from hAMRonization import AmrPlusPlusIO
from hAMRonization import ResFamsIO
from hAMRonization import TBProfilerIO
from hAMRonization import MykrobeIO
from hAMRonization import PointFinderIO
from hAMRonization import FARGeneIO

_FormatToIterator = {
    "abricate": AbricateIO.AbricateIterator,
    "amrfinderplus": AmrFinderPlusIO.AmrFinderPlusIterator,
    "ariba": AribaIO.AribaIterator,
    "rgi": RgiIO.RgiIterator,
    "resfinder": ResFinderIO.ResFinderIterator,
    "srax": SraxIO.SraxIterator,
    "deeparg": DeepArgIO.DeepArgIterator,
    "kmerresistance": KmerResistanceIO.KmerResistanceIterator,
    "srst2": Srst2IO.Srst2Iterator,
    "groot": GrootIO.GrootIterator,
    "staramr": StarAmrIO.StarAmrIterator,
    "csstar": CSStarIO.CSStarIterator,
    "amrplusplus": AmrPlusPlusIO.AmrPlusPlusIterator,
    "resfams": ResFamsIO.ResFamsIterator,
    "tbprofiler": TBProfilerIO.TBProfilerIterator,
    "mykrobe": MykrobeIO.MykrobeIterator,
    "pointfinder": PointFinderIO.PointFinderIterator,
    "fargene": FARGeneIO.FARGeneIOIterator,
}

_ReportFileToUse = {
    "abricate": "OUTPUT.tsv",
    "amrfinderplus": "OUTPUT.tsv",
    "ariba": "OUTDIR/OUTPUT.tsv",
    "rgi": "OUTPUT.txt or OUTPUT_bwtoutput.gene_mapping_data.txt",
    "resfinder": "ResFinder_results_tab.txt",
    "srax": "sraX_detected_ARGs.tsv",
    "deeparg": "OUTDIR/OUTPUT.mapping.ARG",
    "kmerresistance": "OUTPUT.res",
    "srst2": "OUTPUT_srst2_report.tsv",
    "groot": "OUTPUT.tsv (from `groot report`)",
    "staramr": "resfinder.tsv",
    "csstar": "OUTPUT.tsv",
    "amrplusplus": "gene.tsv",
    "resfams": "resfams.tblout",
    "tbprofiler": "OUTPUT.results.json",
    "mykrobe": "OUTPUT.json",
    "pointfinder": "PointFinder_results.txt",
    "fargene": "retrieved-genes-*-hmmsearched.out"
}


_RequiredToolMetadata = {
    "abricate": AbricateIO.required_metadata,
    "amrfinderplus": AmrFinderPlusIO.required_metadata,
    "amrplusplus": AmrPlusPlusIO.required_metadata,
    "ariba": AribaIO.required_metadata,
    "csstar": CSStarIO.required_metadata,
    "deeparg": DeepArgIO.required_metadata,
    "fargene": FARGeneIO.required_metadata,
    "groot": GrootIO.required_metadata,
    "kmerresistance": KmerResistanceIO.required_metadata,
    "resfams": ResFamsIO.required_metadata,
    "resfinder": ResFinderIO.required_metadata,
    "mykrobe": MykrobeIO.required_metadata,
    "pointfinder": PointFinderIO.required_metadata,
    "rgi": RgiIO.required_metadata,
    "srax": SraxIO.required_metadata,
    "srst2": Srst2IO.required_metadata,
    "staramr": StarAmrIO.required_metadata,
    "tbprofiler": TBProfilerIO.required_metadata,
}


def parse(handle, metadata, tool):
    r"""Turn a sequence file into an iterator returning SeqRecords.
    Arguments:
     - handle   - handle to the file, or the filename as a string
     - tool - lower case string describing the file format.
     - required_arguments - dict containing the required arguments for tool
    Typical usage, opening a file to read in, and looping over the record(s):
    >>> import hAMRonization as hAMR
    >>> filename = "abricate_report.tsv"
    >>> metadata = {"analysis_software_version": "1.0.1",
    ...             "reference_database_version": "2019-Jul-28"}
    >>> for result in hAMR.parse(filename, required_arguments, "abricate"):
    ...    print(result)

    """
    if not isinstance(tool, str):
        raise TypeError("Need a string for the file format (lower case)")
    if not isinstance(metadata, dict):
        raise TypeError("Metadata must be provided as a dictionary")
    if not tool:
        raise ValueError("Tool required (lower case string)")
    if not tool.islower():
        raise ValueError(f"Tool string '{tool}' should be lower case")

    # check all required metadata has been provided
    try:
        tool_required_metadata = _RequiredToolMetadata[tool]
    except KeyError:
        raise ValueError(
            f"Unknown tool: {tool}\nMust be in " f"{_RequiredToolMetadata.keys()}"
        )
    missing_data = []
    for required in tool_required_metadata:
        if required not in metadata:
            missing_data.append(required)
    if missing_data:
        raise ValueError(
            f"{tool} requires {missing_data} supplied " "in metadata dictionary"
        )

    iterator_generator = _FormatToIterator.get(tool)
    if iterator_generator:
        return iterator_generator(handle, metadata)
    raise ValueError(f"Unknown tool: {tool}\nMust be in " f"{_FormatToIterator.keys()}")
