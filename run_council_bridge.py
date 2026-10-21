"""Start the offline Council Bridge; runtime files remain under runtime_data."""
import argparse
from pathlib import Path

from cczps_lite.council_bridge.fixtures import council_fixture
from cczps_lite.council_bridge.runtime import CouncilBridge
from cczps_lite.council_bridge.server import make_server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8767)
    args = parser.parse_args()
    bridge = CouncilBridge(Path(__file__).parent / "runtime_data/council_bridge", [
        council_fixture(), council_fixture("second-council-demo", "Second fictional Council — isolation rehearsal")])
    server, token = make_server(bridge, args.port)
    print(f"Open http://127.0.0.1:{server.server_port}/#{token}")
    print("Local capability is in the URL fragment, not sent in requests or logs. Keep it private.")
    print("SYNTHETIC ONLY. No Council endorsement, live data, external compute or production deployment.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
