import numba
import re
from intervaltree import Interval, IntervalTree
from Bio.Seq import translate, reverse_complement
from Bio.SeqFeature import CompoundLocation, FeatureLocation

@numba.njit
def sliding(seq, window, step):
    for i in range(0, len(seq)-window+1, step):
        yield seq[i:i+window]

def bac_translate(seq):
    return translate(seq, table='Bacterial')

def is_regular(cds_feature, record):
    return (
        # not annotated as pseudo
        cds_feature.qualifiers.get('pseudo') is None and 
        cds_feature.qualifiers.get('pseudogene') is None                            and

        # has length in a multiple of three
        len(loc := cds_feature.location) % 3 == 0                                   and

        # consists of a single part
        (len(pt := loc.parts) == 1 or
          (len(pt) == 2 and record.annotations.get('topology') == 'circular' and 
            ((loc.strand > 0 and pt[0].end == len(record) and pt[1].start == 0) or
             (loc.strand < 0 and pt[1].end == len(record) and pt[0].start == 0))))  and

        # starts with a start codon and ends with a stop codon
        re.fullmatch(                                         
            '([ACGT]TG|AT[ACGT]).*(TAA|TAG|TGA)', loc.extract(str(record.seq))     
        ) is not None
    )

def get_intervaltree(record, filt_func=None):
    # By default, all features except for 'source' is recorded.
    filt_func = filt_func or (lambda feat: feat.type != 'source')
    intervals = IntervalTree.from_tuples([
        (pt.start, pt.end, cds)
        for cds in filter(filt_func, record.features)
        for pt in cds.location.parts
    ])
    return intervals
    
def iter_cds_nonoverlapping_regions(record):
    intervals = get_intervaltree(record, filt_func=lambda feat: feat.type=='CDS')
    intervals.split_overlaps()
    intervals.merge_overlaps()
    
    for s, e, cds in intervals:
        if cds and len((loc:=cds.location).parts) == 1 and is_regular(cds, record):
            if loc.start+(2+s-loc.start)//3*3 > loc.end-(2+loc.end-e)//3*3: continue
            loc = FeatureLocation(
                loc.start+(2+s-loc.start)//3*3, loc.end-(2+loc.end-e)//3*3, cds.strand
            )
            yield cds.qualifiers['locus_tag'][0], loc
            assert len(loc) % 3 == 0
    
    # a bit messy...
    # Try to rescue a CDS that crosses a boundary on a record of circular DNA.
    if record.annotations.get('topology') == 'circular' and len(itv1:=intervals[len(record)-1]) > 0 and len(itv2:=intervals[0]) > 0:
        try: 
            assert len(itv1) == 1 and len(itv2) == 1
            (s1, e1, cds1), (s2, e2, cds2) = [*itv1][0], [*itv2][0]
            assert e1 == len(record) and s2 == 0
            
            if (cds := cds1) == cds2 and cds is not None and is_regular(cds, record):
                pt1, pt2 = cds.location.parts[::cds.strand]
                loc = CompoundLocation([
                    FeatureLocation(pt1.start + (2+s1-pt1.start)//3*3, pt1.end, cds.strand),
                    FeatureLocation(pt2.start, pt2.end - (2+pt2.end-e2)//3*3, cds.strand)
                ][::cds.strand])
                yield cds.qualifiers['locus_tag'][0], loc
                assert len(loc) % 3 == 0
                
            if (cds := cds2) is not None and cds1 is None and is_regular(cds, record):
                _, pt2 = cds.location.parts[::cds.strand]
                loc = FeatureLocation(
                    pt2.start-(e1-s1) + (e1-s1+2)//3*3, pt2.end - (2+pt2.end-e2)//3*3, cds.strand
                )
                yield cds.qualifiers['locus_tag'][0], loc
                assert len(loc) % 3 == 0
                
            if (cds := cds1) is not None and cds2 is None and is_regular(cds, record):
                pt1, _ = cds.location.parts[::cds.strand]
                loc = FeatureLocation(
                    pt1.start + (2+s1-pt1.start)//3*3, pt1.end+e2 - (2+e2)//3*3, cds.strand
                )
                yield cds.qualifiers['locus_tag'][0], loc
                assert len(loc) % 3 == 0
        except:
            raise Exception('Unexpected cases in rescuing CDSs across boundaries on circular DNA records')
    