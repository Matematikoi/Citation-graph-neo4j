import file_management as fm
import pandas as pd

def get_presented_in():
    inproceedings = fm.read_parsed_csv_with_header(fm.Filenames.inproceedings)
    proceedings = fm.read_parsed_csv_with_header(fm.Filenames.proceedings)
    relationship = pd.merge(inproceedings, proceedings, left_on='crossref', right_on='key')
    relationship = relationship[['inproceedings','proceedings']]
    relationship.columns = [':START_ID',':END_ID']
    return relationship

def main():
    relationship = get_presented_in()
    fm.save_parsed_csv(relationship, fm.Filenames.presented_in)

if __name__ == '__main__':
    publications = main()
