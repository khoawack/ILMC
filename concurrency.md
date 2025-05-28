## Case 1: Lost update when dropping same item

Two or more users dro the same item at the same time. One change will overwrite all the other ones.

```mermaid
sequenceDiagram
    participant T1 as Transaction 1
    participant T2 as Transaction 2
    participant DB as Database

    T1->>DB: SELECT amount FROM inventory WHERE user_id = 1 AND sku = 'diamond'
    T2->>DB: SELECT amount FROM inventory WHERE user_id = 1 AND sku = 'diamond'
    T1->>DB: UPDATE inventory SET amount = amount - 3 WHERE user_id = 1 AND sku = 'diamond'
    T2->>DB: UPDATE inventory SET amount = amount - 3 WHERE user_id = 1 AND sku = 'diamond'
```

Solution: Use ```SELECT ... FOR UPDATE``` when updating inventory. This make sure first transaction blocks the row. This will block the other one until it completes, meaning there is no more overwrite. 



## Case 2: Non-repeataable read when veiwing floor items

One player view items on floor and another player picks up an item. When the user viewing the floor items tries to do something with the item that was picked up, the item is gone. 

```mermaid
sequenceDiagram
    participant T1 as Transaction 1
    participant T2 as Transaction 2
    participant DB as Database

    T1->>DB: SELECT * FROM floor ORDER BY dropped_at DESC
    T2->>DB: SELECT item_sku, quantity FROM floor WHERE id = 10
    T2->>DB: DELETE FROM floor WHERE id = 10
    T1->>DB: SELECT * FROM floor ORDER BY dropped_at DESC
```

Solution: Use the ```REPEATABLE READ``` isolation level to make sure floor items remains consistent during the entire transaction.



## Case 3: Write Skew with pickup

Two people try to pick up item at same time. Both see that its on the floor but only one pickup should succeed.

```mermaid
sequenceDiagram
    participant T1 as Transaction 1
    participant T2 as Transaction 2
    participant DB as Database

    T1->>DB: SELECT item_sku, quantity FROM floor WHERE id = 5
    T2->>DB: SELECT item_sku, quantity FROM floor WHERE id = 5
    T1->>DB: INSERT INTO inventory (user_id, sku, ...) VALUES (...)
    T2->>DB: INSERT INTO inventory (user_id, sku, ...) VALUES (...)
    T1->>DB: DELETE FROM floor WHERE id = 5
    T2->>DB: DELETE FROM floor WHERE id = 5
```

Solution: USe '''FOR UPDATE``` so that it locks the row until the transaction finishes. That way, only one pickup can happen at once.
