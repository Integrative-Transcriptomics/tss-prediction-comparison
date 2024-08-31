import pandas as pd
from app.TSSclassifier import GffFormatException


def parse_gff_to_df(filepath):
    """
    parses the entries of type gene from a gff file into a data frame
    :param filepath: path to the gff file
    :return: df
    """
    column_names = ["seqid", "source", "type", "start", "end", "score", "strand", "phase", "attributes"]
    df = pd.read_csv(filepath, sep='\t', comment='#', header=None, names=column_names)
    df = df[df['type'] == 'gene'].reset_index(drop=True)
    if df.empty:
        raise GffFormatException("your GFF file doesnt contain any entries of type gene, no classification of TSS "
                                 "possible")
    return df
