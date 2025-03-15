import os
import unittest

class PublicHtmlTestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = os.path.join(os.getcwd(), 'public_html')

    def test_index_html_exists(self):
        index_file = os.path.join(self.base_path, 'index.html')
        self.assertTrue(os.path.exists(index_file), f"index.html not found in public_html at {index_file}.")

    def test_nexus_index_html_exists(self):
        nexus_index = os.path.join(self.base_path, 'nexus', 'index.html')
        self.assertTrue(os.path.exists(nexus_index), f"nexus/index.html not found in public_html at {nexus_index}.")

    def test_archive_chaos_index_exists(self):
        archive_index = os.path.join(self.base_path, 'archive', 'chaos-of-the-mind', 'index.htm')
        self.assertTrue(os.path.exists(archive_index), f"archive/chaos-of-the-mind/index.htm not found in public_html at {archive_index}.")

if __name__ == '__main__':
    unittest.main()
