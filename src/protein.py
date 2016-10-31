import re

class Protein:
    pattern_re = {'trypsin': r'[RK](?!P)'}

    def __init__(self, desc, seq):
        self.desc = desc
        self.seq = seq

    def digest(self, enzyme='trypsin'):
        pattern = self.pattern_re[enzyme]
        matches = re.finditer(pattern, self.seq)
        start = 0
        for match in matches:
            end = match.start()
            yield self.seq[start:end+1]
            start = end+1
        if start < len(self.seq):
            yield self.seq[start:]


if __name__ == "__main__":
    protein = Protein(desc='blah blah',
                      seq='MVPPPPSRGGAAKPGQLGRSLGPLLLLLRPEEPEDGDREICSESK')

    for peptide in protein.digest():
        print(peptide)
