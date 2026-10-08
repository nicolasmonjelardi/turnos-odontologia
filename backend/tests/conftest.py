"""Conftest: pone backend/src en sys.path y expone fixtures base.

Sin fixtures pesadas: cada test crea su propio store en memoria
(ver src.deps / src.repos) para no compartir estado.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
