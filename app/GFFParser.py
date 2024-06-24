import pandas as pd


def parse_gff_to_df(filepath):
    df = pd.read_csv(filepath, sep='\t', comment='#', header=None,
                     names=["seqid", "source", "type", "start", "end", "score", "strand", "phase", "attributes"])
    df = df[df['type'] == 'gene'].reset_index(drop=True)
    return df


filepath = "../tests/test_files/NC_004703.gff"

# Display the first few rows
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

if __name__ == '__main__':
    print(parse_gff_to_df(filepath).head())
