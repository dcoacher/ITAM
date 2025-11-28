# Tests file for CICD process
# Importing necessary modules
import importlib
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]   # Set Root Directory (from .github/workflows/tests/ to root)
APP_DIR = ROOT_DIR / "app"  # Set Application Directory

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


def test_storage(monkeypatch, tmp_path):    # Test Storage Function
    monkeypatch.setenv("ITAM_DATA_DIR", str(tmp_path))
    storage_mod = importlib.reload(importlib.import_module("storage"))
    test_users = {"1": {"name": "Eli Dror", "items": []}}
    test_items = {
        "1": {
            "id": "1",
            "main_category": "Assets",
            "sub_category": "Laptop",
            "manufacturer": "Dell",
            "model": "XPS",
            "price": 1000,
            "quantity": 1,
            "status": "In Stock",
            "assigned_to": None,
        }
    }

    storage_mod.save_users(test_users)    # Save Test Users to the file
    storage_mod.save_items(test_items)    # Save Test Items to the file

    assert storage_mod.load_users() == test_users
    assert storage_mod.load_items() == test_items


def test_add_new_user(monkeypatch, tmp_path):    # Test Add New User Function
    monkeypatch.setenv("ITAM_DATA_DIR", str(tmp_path))
    storage_mod = importlib.reload(importlib.import_module("storage"))
    
    # Simulate adding a user directly via storage (Flask app logic)
    test_users = storage_mod.load_users()
    if not test_users:
        next_id = "1"
    else:
        next_id = str(max(int(key) for key in test_users.keys()) + 1)
    
    test_users[next_id] = {"name": "Eli Dror", "items": []}
    storage_mod.save_users(test_users)

    stored_users = storage_mod.load_users()    # Load Test Users from the file
    assert next_id in stored_users
    assert stored_users[next_id]["name"] == "Eli Dror"
    assert stored_users[next_id]["items"] == []