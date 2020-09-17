#!/usr/bin/env python

from abc import ABC, abstractmethod

class hAMRonizedResultIterator(ABC):
    """
    Base class for the parsers for each AMR detection tool

    This should return an appopriate iterator for results from whatever
    AMR tool report is being parsed
    """

    def __init__(self, source, tool, mode="t"):
        """
        Create an AMRReportIterator for whichever tool report is being parsed

        Based on https://github.com/biopython/biopython/blob/master/Bio/SeqIO/Interfaces.py#L23

        Arguments:
            - source: input file stream or path to input
            - tool: name of amr tool report that is being parsed

        """

        supported_tools = ['abricate', 'ariba', 'amrfinderplus', 'rgi',
                                'resfinder', 'srax', 'deeparg', 'kmerresistance',
                                'srst2', 'groot', 'staramr', 'c-sstar',
                                'amrplusplus', 'resfams']
	if tool is not in supported_tools:
            raise ValueError(f"Tool must be on of {supported_tools}")


	try:
            self.stream = open(source, "r" + mode)
            self.should_close_stream = True
        except TypeError:  # not a path, assume we received a stream
            if mode == "t":
                if source.read(0) != "":
                    raise ValueError(
                        f"{fmt} files must be opened in text mode.")
                    ) from None
            elif mode == "b":
                if source.read(0) != b"":
                    raise ValueError(
                        f"{fmt} files must be opened in binary mode."
                    ) from None
            else:
                raise ValueError(f"Unknown mode {mode}") from None
            self.stream = source
            self.should_close_stream = False
        try:
            self.records = self.parse(self.stream)
	except Exception:
            if self.should_close_stream:
                self.stream.close()

    def __next__(self):
        try:
            return next(self.amr_results)
        except Exception:
            if self.should_close_stream:
                self.stream.close()
            raise

    def __iter__(self):
        """
        Iterate over entries as an AMRResult object

        Not to be overwritten in subclasses
        """
        return self

    @abtractmethod
    def parse(self, handle):
        """
        Start parsing the file and return an AMRResult iterator
        """

class hAMRonizedWriter(ABC):
    """
    Base class for outputting hAMRonized parsed AMR reports

    This doens't actually have to be an abtract class given that once
    parsed all output should be the same for all tools

    Not quite sure how to implement this for sequential writing of json
    Maybe just sequential write TSV for now and can convert to json later
    """

