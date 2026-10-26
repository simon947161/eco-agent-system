"""Risk-focused checks for the policy view in the existing Console."""
import json
import tempfile
import threading
import unittest
from urllib.request import urlopen

from cczps_lite.environmental_question_runtime.policy import console_packet
from cczps_lite.environmental_question_runtime.server import create_server


class PolicyConsoleIntegrationTests(unittest.TestCase):
    def test_missing_sources_propagate_without_promotion(self):
        packet = console_packet(source_dirs=[])
        self.assertEqual(len(packet['research_lines']), 3)
        self.assertFalse(packet['assessment_created'])
        self.assertFalse(packet['current_execution_documents_verified'])
        for line in packet['research_lines']:
            self.assertTrue(line['evidence_gaps'])
            self.assertEqual(line['conclusion_level'], 'L0')
            self.assertEqual(line['execution_status'], 'NOT_AUTHORISED_BY_POLICY_REFERENCE')
        self.assertEqual(packet['packet_digest'], console_packet(source_dirs=[])['packet_digest'])

    def test_http_policy_and_original_research_share_server(self):
        with tempfile.TemporaryDirectory() as root:
            server = create_server(root + '/research.sqlite3', port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            base = f'http://127.0.0.1:{server.server_address[1]}'
            try:
                with urlopen(base + '/api/policy-context') as response:
                    raw = response.read().decode(); packet = json.loads(raw)
                self.assertEqual(packet['continuity']['parent_issue'], 128)
                self.assertNotIn('source_dirs', raw)
                self.assertNotIn('H:\\', raw)
                with urlopen(base + '/program.html') as response:
                    html = response.read().decode()
                self.assertIn('id="policyContext"', html)
                self.assertIn('id="startCycle"', html)
                with urlopen(base + '/policy.js') as response:
                    self.assertIn('textContent', response.read().decode())
                with urlopen(base + '/api/health') as response:
                    self.assertEqual(json.load(response)['real_execution'], 'blocked')
            finally:
                server.shutdown(); server.server_close(); thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main()

