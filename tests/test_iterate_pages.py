import pytest
import iterate_pages

page_name_test_data = [('AIB blank Change 1\n\x0c', 'AIB blank'),
    ('Change 1\n\x0c', ''),
    ('eee ae a ee ee\n\n0017 00-1/2 blank Change 1\n\x0c', '0017 00-1/2 blank'),
    ('0030 00-1 Change 1\n\x0c', '0030 00-1'),
    ('Change 1 0030 00-2\n\x0c', '0030 00-2'),
    ('Change 1 0035 00-2\n\x0c', '0035 00-2'),
    ('0035 00-5/6 blank Change 1\n\x0c', '0035 00-5/6 blank'),
    ('0035B 00-1/2 blank Change 1\n\x0c', '0035B 00-1/2 blank'),
    ('0037 00-3 Change 1\n\x0c', '0037 00-3'),
    ('Change 1 0037 00-4\n\x0c', '0037 00-4')]

def test_get_page_name():
    for i in page_name_test_data:
        assert(iterate_pages.get_page_name(i[0]) == i[1])

range_raw = [[1,2,3],[19, 22, 71, 99, 100, 116, 119, 125, 131, 132]]
range_expected = [[(1,3)],[(19, 19), (22, 22), (71, 71), (99, 100), (116, 116), (119, 119), (125, 125), (131, 132)]]

def test_ranges():
    for i in range(len(range_raw)):
        assert(list(iterate_pages.ranges(range_raw[i])) == range_expected[i])

txt_test_data = {19: ('AIB blank', '1'), 22: ('', '1'), 71: ('0017 00-1/2 blank', '1'), 99: ('0030 00-1', '1'), 100: ('0030 00-2', '1'), 116: ('0035 00-2', '1'), 119: ('0035 00-5/6 blank', '1'), 125: ('0035B 00-1/2 blank', '1'), 131: ('0037 00-3', '1'), 132: ('0037 00-4', '1')}
squeeze_expected = [['AIB blank', 19, (19, 19), '1'], ['', 22, (22, 22), '1'], ['0017 00-1/2 blank', 71, (71, 71), '1'], ['0030 00-1 - 0030 00-2', 99, (99, 100), '1'], ['0035 00-2', 116, (116, 116), '1'], ['0035 00-5/6 blank', 119, (119, 119), '1'], ['0035B 00-1/2 blank', 125, (125, 125), '1'], ['0037 00-3 - 0037 00-4', 131, (131, 132), '1']]

def test_squeeze():
    assert(iterate_pages.squeeze(txt_test_data) == squeeze_expected)

