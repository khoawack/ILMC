# Example Flow for ILYMC Inventory, Crafting, & Action System

This document provides a walkthrough of a crafting scenario using the ILYMC API.

## Crafting an Iron Pickaxe

Alex the Miner wants to craft a new iron pickaxe but isn’t sure what he can make with the materials he has. He performs the following steps:

1. **Check item recipe**  
   **Request:** `GET /craft/recipe/iron_pickaxe`  
   **Response:**  
    ```json
    {
      "item_name": "iron_pickaxe",
      "ingredients": [
        {
          "sku": "IRON_ORE",
          "quantity": "3"
        },
        {
          "sku": "STICK",
          "quantity": "2"
        }
      ]
    }
    ```

2. **Craft the iron pickaxe**  
   **Request:** `POST /craft`  
   **Body:**  
   ```json
   {
     "item_name": "iron_pickaxe",
     "quantity": 1
   }
   ```  
   **Response:**  
   ```json
   {
     "success": true,
     "crafted_quantity": 1
   }
   ```

3. **View updated inventory**  
   **Request:** `GET /inventory`  
   **Response:**  
   ```json
   {
     "items": [
       {
         "sku": "iron_pickaxe",
         "quantity": 1
       }
     ]
   }
   ```

Alex successfully crafts the item and is ready to mine more resources.

## Track Progress Towards Collecting Items

Alex wants to keep track of all the items he's been wanting to collect in his checklist. 

1. **Get player's collected items checklist**
   **Request:** `GET /collection/checklist`
   **Response:**
   ```json
   {
    "collected_items": [
      "iron_ingot",
      "diamond",
      "bread",
      "stone_axe"
    ],
    "uncollected_items": [
      "ender_pearl",
      "golden_apple",
      "elytra",
    ]
   }
   ```

2. **Mark as collected**
   **Request:** `POST /collection/mark`
   **Body:**
```json
{
  "item_name": "ender_pearl"
}
```
**Reponse:**
```json
{
  "sucess": true,
  "message": "Marked ender_pearl as collected"
}
scenario ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~...
