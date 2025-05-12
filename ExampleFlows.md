# Example Flow for ILYMC Inventory, Crafting, & Action System

This document provides a walkthrough of a crafting scenario using the ILYMC API.

## Example Scenario: Crafting an Iron Pickaxe

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

## Example Scenario: Mining with a Wooden Pickaxe
Alex wants to gather basic resources using his wooden pickaxe. Drops are randomized but will never exceed "stone" quality and always return 1-3 units.
The ores that you have a chance to receive will be based on the pickaxe you have. Drop rates TBD

1. **Mine for resources**  
   **Request:** `POST /action/mine`

    **Body:**  
   ```json
   {
     "pickaxe_name": "wooden_pickaxe"
   }
   ```  
   **Possible Response (randomized):**  
   ```json
   {
     "sku": "cobblestone",
     "quantity": 3
   }
   ```

2. **View updated inventory**  
   **Request:** `GET /inventory`  
   **Response:**  
   ```json
   {
     "items": [
       { "sku": "stone", "quantity": 3 },
       { "sku": "wooden_pickaxe", "quantity": 1 }
     ]
   }
   ```
Alex successfully gathers stone resources and can now craft stone-tier tools.

## Example Scenario: Organizing Inventory
Alex now wants a better and more organized inventory. He performs the following steps:

1. **Collect a basic item**  
   **Request:** `POST /action/collect`  
   **Response:**  
   ```json
   {
     "sku": "OAK_LOG",
     "quantity": 1
   }
   ```

2. **View inventory**  
   **Request:** `GET /inventory`  
   **Response:**  
   ```json
   {
     "items": [
       {
         "sku": "OAK_LOG",
         "quantity": 1
       }
     ]
   }
   ```

3. **Favorite the collected item**  
   **Request:** `POST /inventory/OAK_LOG/favorite`  
   **Response:**  
   ```json
   {
     "success": true
   }
   ```
Alex now has an inventory with items favorited. He can now filter them out better.
