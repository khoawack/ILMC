# Example workflow
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

# Testing results
collecting a random item
![image](https://github.com/user-attachments/assets/5c17bc97-3928-411b-9d14-3b9ce62c4b30)

checking inventory
![image](https://github.com/user-attachments/assets/ced04991-2277-4df6-9e3a-eafac56f33c2)

adding item to favorite
![image](https://github.com/user-attachments/assets/634f6777-eae0-4153-9f58-8153b1526903)

checking inventory again to see if it worked
![image](https://github.com/user-attachments/assets/0ba30684-8901-4200-aca3-a92eeb4fba54)



