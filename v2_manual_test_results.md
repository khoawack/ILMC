## Example Scenario: Crafting an Iron Pickaxe

Alex the Miner wants to craft a new iron pickaxe but isn’t sure what he can make with the materials he has. He performs the following steps:

1. **Check item recipe**  
   **Request:** `GET /craft/recipe?item_name={item_name}`  
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

# Testing results
First, we check the recipe for iron pickaxe
![image](https://github.com/user-attachments/assets/a62f14f0-f568-43db-9d23-28c83074fe09)


Then, we craft it
![image](https://github.com/user-attachments/assets/7d040277-f159-43a9-959f-0aa43e4ff742)

Lastly, we check our inventory to see if we have it.
![image](https://github.com/user-attachments/assets/ab7f6888-2710-46f0-8213-59428d27d26b)



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

# TESTING RESULTS
First, lets mine with our iron pick we just got.
![image](https://github.com/user-attachments/assets/13ad3245-549c-4df3-b0e2-0af8277d3701)

Looks like we got iron, lets check our inventory.
![image](https://github.com/user-attachments/assets/73ca4295-f820-4883-94c2-c8ff7dc5f3b8)
As you can see, our iron went from 0 to 1.

