import importlib.util
import hashlib
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('smrc_policy_console', Path(__file__).resolve().parents[1] / 'tools/smrc_policy_console.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PolicyConsoleTests(unittest.TestCase):
    def setUp(self):
        self.config = {'data_class': 'PUBLIC_REFERENCE_METADATA', 'mission_id': 'TEST',
                       'documents': [{'id': 'TEST-SOURCE', 'filename': 'missing.pdf', 'sha256': '0' * 64,
                                      'temporal_status': 'HISTORICAL_BASELINE'}], 'research_lines': []}

    def test_missing_source_is_visible_without_blocking(self):
        packet = module.build_packet(self.config)
        self.assertEqual(packet['sources'][0]['local_copy_state'], 'MISSING_LOCAL_COPY')
        self.assertIsNone(packet['official_decision'])
        self.assertFalse(packet['sources'][0]['current_execution_authority'])

    def test_matching_and_changed_bytes_are_distinguished(self):
        # Use this test file as a small read-only stand-in; no PDF parsing implied.
        file = Path(__file__)
        self.config['documents'][0]['filename'] = file.name
        self.config['documents'][0]['sha256'] = hashlib.sha256(file.read_bytes()).hexdigest()
        packet = module.build_packet(self.config, [file.parent])
        self.assertEqual(packet['sources'][0]['local_copy_state'], 'MATCHED_RECORDED_VERSION')
        self.config['documents'][0]['sha256'] = '0' * 64
        packet = module.build_packet(self.config, [file.parent])
        self.assertEqual(packet['sources'][0]['local_copy_state'], 'QUARANTINED_VERSION_MISMATCH')
        self.assertNotIn(str(file.parent), str(packet))

    def test_new_document_does_not_gain_admission(self):
        file = Path(__file__)
        self.config['documents'][0].update(filename=file.name, sha256=None)
        packet = module.build_packet(self.config, [file.parent])
        self.assertEqual(packet['sources'][0]['local_copy_state'], 'NEW_COPY_REQUIRES_ADMISSION')

    def test_private_data_and_path_traversal_rejected(self):
        self.config['data_class'] = 'COUNCIL_INTERNAL'
        with self.assertRaises(ValueError): module.build_packet(self.config)
        self.config['data_class'] = 'PUBLIC_REFERENCE_METADATA'
        self.config['documents'][0]['filename'] = '../private.pdf'
        with self.assertRaises(ValueError): module.build_packet(self.config)

    def test_bad_hash_and_duplicate_source_rejected(self):
        self.config['documents'][0]['sha256'] = 'bad'
        with self.assertRaises(ValueError): module.build_packet(self.config)
        self.config['documents'][0]['sha256'] = '0' * 64
        self.config['documents'].append(dict(self.config['documents'][0]))
        with self.assertRaises(ValueError): module.build_packet(self.config)


if __name__ == '__main__':
    unittest.main()
