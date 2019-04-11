from io import open
import unittest
from filesplitor import human_readable_size
from filesplitor import get_slice_size
from filesplitor import get_max_index
from filesplitor import get_filenames
from filesplitor import do_split
from filesplitor import do_merge


class TestFileSplitor(unittest.TestCase):


    def test02(self):
        print(human_readable_size(2*1024))
        assert human_readable_size(2) == "2B"
        assert human_readable_size(2*1024) == "2.00K"
        assert human_readable_size(2*1024*1024) == "2.00M"
        assert human_readable_size(2*1024*1024*1024) == "2.00G"
        assert human_readable_size(2*1024*1024*1024*1024) == "2.00T"

    def test03(self):
        assert get_slice_size(2) == 2
        assert get_slice_size("1k") == 1024
        assert get_slice_size("2M") == 1024*1024*2
        assert get_slice_size("3G") == 1024*1024*1024*3
        assert get_slice_size("4t") == 1024*1024*1024*1024*4

    def test04(self):
        with open("test.txt", "rb") as fobj:
            assert get_max_index(fobj, 2) == 2

    def test05(self):
        names = get_filenames("*.txt")
        assert "test.txt" in names
        assert "requirements.txt" in names

    def test06(self):
        dst = "testdest.txt"
        with open("test.txt", "rb") as src:
            do_split(src, dst, 2)
        with open("testdest.txt.1", "rb") as fobj:
            assert fobj.read() == b"ab"
        with open("testdest.txt.2", "rb") as fobj:
            assert fobj.read() == b"c"

    def test07(self):
        dst = "test02src.txt"
        filename1 = "test02.txt.1"
        filename2 = "test02.txt.2"
        do_merge(dst, [filename1, filename2])
        with open(dst, "rb") as fobj:
            assert fobj.read() == b"abc"

if __name__ == "__main__":
    unittest.main()
