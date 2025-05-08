from fastapi.testclient import TestClient
from app.main import app  

client = TestClient(app)

def test_collect_item():
    res = client.post("/action/collect")
    assert res.status_code == 200
    data = res.json()
    assert "sku" in data
    assert "item_name" in data
    assert "quantity" in data
    assert data["quantity"] in [1, 2, 3]

def test_craft_valid_item():
    res = client.post("/action/craft", json={"item_name": "iron_pickaxe", "quantity": 2})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["crafted_quantity"] == 2

def test_craft_invalid_item():
    res = client.post("/action/craft", json={"item_name": "banana_sword", "quantity": 1})
    assert res.status_code == 200 or res.status_code == 400
    data = res.json()
    assert "error" in data or "detail" in data

def test_get_inventory():
    res = client.get("/inventory/")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_reset_inventory():
    client.post("/action/collect")

    res = client.post("/admin/reset")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True

    res = client.get("/inventory/")
    data = res.json()
    assert data["items"] == []

def test_set_and_get_favorite():
    # First collect an item to ensure it exists
    collect_res = client.post("/action/collect")
    sku = collect_res.json()["sku"]

    # Mark as favorite
    fav_res = client.post("/inventory/favorite", json={"sku": sku, "favorite": True})
    assert fav_res.status_code == 200
    fav_data = fav_res.json()
    assert fav_data["success"] is True
    assert fav_data["sku"] == sku
    assert fav_data["favorite"] is True

    # Get favorites and confirm it's included
    get_favs = client.get("/inventory/favorite")
    assert get_favs.status_code == 200
    favs_data = get_favs.json()
    assert "favorites" in favs_data
    assert any(item["sku"] == sku for item in favs_data["favorites"])
