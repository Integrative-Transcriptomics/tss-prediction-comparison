from enum import Enum


# list of all file ending we want to allow the user to upload
class FileEndings(Enum):
    WIGGLE = ".wig"
    TSV = ".tsv"
    gff = ".gff"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
