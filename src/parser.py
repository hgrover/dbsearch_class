import re

begin_re = re.compile('BEGIN IONS')
scan_re = re.compile('TITLE=Scan\s+([0-9]+)')
mz_re = re.compile('PEPMASS=([0-9\.]+)')
charge_re = re.compile('CHARGE=([0-9])')
peak_re = re.compile('([0-9\.]+)\s([0-9\.]+)')
end_re = re.compile('END IONS')
def mgf(file_):
    while True:
        line = file_.readline()
        if line == "":      ## End of File
            break
        else:
            if begin_re.match(line) != None:
                inside = True
                mz_int_tuples = []
                while inside:
                    line = file_.readline()
                    if scan_re.match(line) != None:
                        scan = scan_re.match(line).group(1).strip()
                    elif mz_re.match(line) != None:
                        mz = float(mz_re.match(line).group(1).strip())
                    elif charge_re.match(line) != None:
                        charge = int(charge_re.match(line).group(1).strip())
                    elif peak_re.match(line) != None:
                        mz, intensity = peak_re.match(line).group(0).strip().split()
                        mz_int_tuple = float(mz), float(intensity)
                        mz_int_tuples.append(mz_int_tuple)
                    elif end_re.match(line) != None:
                        inside = False
            else:
                continue

            yield {'mz': mz,
                   'charge': charge,
                   'scan': scan,
                   'peaks': mz_int_tuples}

pattern = '^BEGIN IONS$\n^TITLE=(?P<TITLE>.*?)$\n^PEPMASS=(?P<PEPMASS>.*?)$\n^CHARGE=(?P<CHARGE>.*?$)\n(?P<VALUES>.*?)\n^END IONS$'
def mgf2(file_):
    for i in re.finditer(pattern, file_.read(), flags=re.MULTILINE | re.DOTALL):
        yield i.groupdict()


def fasta(fp):
    curr_header = None
    curr_seq = []
    for line in fp:
        if line.startswith('>'):
            if curr_header:
                yield {'header': curr_header,
                       'seq': ''.join(curr_seq)}
            curr_header = line[1:].strip()
            curr_seq = []
        else:
            curr_seq.append(line.strip())



if __name__ == "__main__":
    import os
    import pprint
    # mgf_file = os.path.join(os.getcwd(),
    #                         '../test_data/1500cells_01.mzXML.MS2.HCD.mgf')
    fasta_file = os.path.join(os.getcwd(),
                              '../test_data/proteome.fasta')
    # fh = open(mgf_file)
    # for spectrum in mgf(fh):
    #     pprint.pprint(spectrum)
    #     input()
    # for spectrum in mgf2(fh):
    #     pprint.pprint(spectrum)
    #     input()

    fh = open(fasta_file)
    for seq in fasta(fh):
        pprint.pprint(seq)