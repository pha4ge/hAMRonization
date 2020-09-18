#!/usr/bin/env python

from abc import ABC, abstractmethod
from .hAMRonizedResult import hAMRonizedResult

class hAMRonizedResultIterator(ABC):
    """
    Base class for the parsers for each AMR detection tool

    This should return an appopriate iterator for results from whatever
    AMR tool report is being parsed
    """

    def __init__(self, source, tool, field_map, additional_data, mode="t"):
        """
        Create an hAMRonizedResultIterator for whichever tool report is being parsed

        Based on https://github.com/biopython/biopython/blob/master/Bio/SeqIO/Interfaces.py#L23

        Arguments:
            - source: input file stream or path to input
            - tool: name of amr tool report that is being parsed

        """
        self.field_map = field_map
        self.additional_data = additional_data

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

    def hAMRonize(self, report_result, additional_fields):
        """
        Convert a line of parsed AMR report in original format to the
        hAMRonization specification
        """
        hAMRonized_result_data = {}

        for field_name, field_value in additional_fields.items()
            hAMRonized_result_data[field_name] = field_value

        for original_field, hAMRonized_field in self.field_map.items():
            if hAMRonized_field:
                hAMRonized_result_data[hAMRonized_result_data] = \
                        report_result[original_field]

        hAMRonized_result = hAMRonizedResult(**hAMRonized_result_data)

        return hAMRonized_result

    def __next__(self):
        try:
            return next(self.amr_results)
        except Exception:
            if self.should_close_stream:
                self.stream.close()
            raise

    def __iter__(self):
        """
        Iterate over entries as an hAMRonizedResult object

        Not to be overwritten in subclasses
        """
        return self

    @abtractmethod
    def parse(self, handle):
        """
        Start parsing the file and return an hAMRonizedResult iterator
        """

class hAMRonizedWriter(ABC):
    """
    Base class for outputting hAMRonized parsed AMR reports

    This doens't actually have to be an abtract class given that once
    parsed all output should be the same for all tools

    Not quite sure how to implement this for sequential writing of json
    Maybe just sequential write TSV for now and can convert to json later
    """

