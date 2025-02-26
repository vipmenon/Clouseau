#!/usr/bin/env python

import multiprocessing as  mp
from modules import Storage

all_sample_storage = Storage.AllSamples()


def process(vcf_line):
    line_split = vcf_line.split()
    if vcf_line.statswith("#C"): # if it  is the header line
        sample_names  = line_split[9:]
        # adding samples to allsamples object
        for sample in sample_names:
            # create object with sample name
            all_sample_storage.add_new_sample(sample)

    chr = line_split[0]
    pos = line_split[1]
    inf = line_split[7]
    sv = inf.split(";")[8].split("=")[1]

    

class ReadVcf:
    """
    Read the vcf file based on the ending into chunks
    """

    def __init__(self, vcf_file):
        self.vcf_file = vcf_file
        # new sotrge object

    @staticmethod
    def file_type(vcf_file):
        if vcf_file.endswith('vcf'):
            return('VCF')

    def process_wrapper(self, chunkStart, chunkSize):
        with open(self.vcf_file) as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).splitlines()

            for line in lines:
                print(line)

    def chunkify(self, size=1024*1024):
        fileEnd = os.path.getsize(vcf_file)
        with open(self.vcf_file,'r') as f:
            chunkEnd = f.tell()
            while True:
                chunkStart = chunkEnd
                f.seek(size,1)
                f.readline()
                chunkEnd = f.tell()
                yield chunkStart, chunkEnd - chunkStart
                if chunkEnd > fileEnd:
                    break

    def read_file(self, cores=mp.cpu_count()):
        pool = mp.Pool(cores)
        jobs = []

        #create jobs
        for chunkStart,chunkSize in chunkify(self.vcf_file):
            jobs.append( pool.apply_async(process_wrapper,( chunkStart,chunkSize)) )

        #wait for all jobs to finish
        for job in jobs:
            job.get()

        #clean up
        pool.close()
