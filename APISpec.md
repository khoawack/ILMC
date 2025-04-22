# API Specification for ILYMC Inventory, Crafting, & Action System

## 1. Inventory Management

### 1.1. View Inventory - `/inventory` (GET)

Retrieves the current inventory of the player.

**Response:**

```json
{
  "items": [
    {
      "item_name": "string",
      "sku": "string",
      "quantity": "integer"
    }
  ]
}
```

---

### 1.2. Discard Items - `/inventory/discard` (POST)

Removes specified quantities of items from the inventory.

**Request:**

```json
[
  {
    "sku": "string",
    "quantity": "integer"
  }
]
```

**Response:**

```json
{
  "success": true
}
```

---

### 1.3. Discard All Items - `/inventory/discard/all` (POST)

Clears the entire inventory.

**Response:**

```json
{
  "success": true
}
```

---

### 1.4. Favorite an Item - `/inventory/{sku}/favorite` (POST)

Marks an item as a favorite to improve organization.

**Response:**

```json
{
  "success": true
}
```

## 2. Item Collection and Mining

### 2.1. Collect Basic Item - `/action/collect` (POST)

Gives the player a random drop from a pool of basic items (e.g., wood, dirt).

**Response:**

```json
{
  "item_name": "string",
  "sku": "string",
  "quantity": "integer"
}
```

---

### 2.2. Mine for Resources - `/action/mine/{pickaxe_type}` (POST)

Simulates mining using a specified pickaxe. Drop chances depend on the pickaxe type.

**Response:**

```json
{
  "item_name": "string",
  "sku": "string",
  "quantity": "integer"
}
```

## 3. Crafting System

### 3.1. Craft Item - `/craft` (POST)

Attempts to craft an item using the player's current inventory.

**Request:**

```json
{
  "sku": "string",
  "quantity": "integer"
}
```

**Response:**

```json
{
  "success": true,
  "crafted_quantity": "integer"
}
```

---

### 3.2. View Craftable Items - `/craftable` (GET)

Returns a list of all items the player currently has materials to craft.

**Response:**

```json
[
  {
    "item_name": "string",
    "available_quantity": "integer"
  }
]
```

---

### 3.3. Get Recipe - `/craftable/recipe/{item_name}` (GET)

Returns the recipe required to craft a specific item.

**Response:**

```json
{
  "item_name": "string",
  "ingredients": [
    {
      "sku": "string",
      "quantity": "integer"
    }
  ]
}
```

