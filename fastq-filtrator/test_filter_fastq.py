import unittest
from filter_fastq import get_read_length
from filter_fastq import filter_by_length
from filter_fastq import count_gc_content
from filter_fastq import filter_by_gc_content


class FilterTest(unittest.TestCase):

    def test_length_in_header(self):
        self.assertEqual(get_read_length('@SRR1363257.37 GWZHISEQ01:153:C1W31ACXX:5:1101:14027:2198 length=101'), 101)
        self.assertEqual(get_read_length('@SRR1363257.37 length=101 GWZHISEQ01:153:C1W31ACXX:5:1101:14027:2198'), 101)

    def test_filter_by_length(self):
        header = '@SRR1363257.37 GWZHISEQ01:153:C1W31ACXX:5:1101:14027:2198 length=101'
        self.assertTrue(filter_by_length(50, header))
        self.assertFalse(filter_by_length(180, header))

    def test_count_gc_content(self):
        self.assertEqual(count_gc_content('GATCTAAGCTGAAGCCAGGCCAAAGTTTGACGATTGG'), 49)
        self.assertEqual(count_gc_content('GAtcTaaGCTGAAGccAGGCCAAAGTTTGACGATTGG'), 49)

    def test_filter_by_gc_content(self):
        seq = 'GAtcTaaGCTGAAGccAGGCCAAAGTTTGACGATTGG'
        self.assertTrue(filter_by_gc_content(60, 40, seq))
        self.assertFalse(filter_by_gc_content(30, 20, seq))

if __name__ == '__main__':
    unittest.main()