# Fake Data Modeling
To simulate realistic usage and test the scalability of our service, we generated a total of 1,000,000 rows of data across four main tables. 
We started with 10,000 users, which felt like a reasonable base to model a mid sized player base. There’s no specific reason for that number other than it being a nice, reasonable number. 
For the inventory, we created 300,000 rows to give each user approximately 30 items on average similar to Minecraft's 27 slots. This leaves room for adding more items later while still keeping inventory sizes realistic. 
We inserted 100,000 floor item entries to mimic a large, active world where frequent player actions leave items behind, and where regular worldly activities happen. This in turn simulates real time activity and allows us to test features like periodic floor cleanup processes. 
The remaining 590,000 rows are used for logging player actions such as crafting, mining, or collecting, since these actions are the most frequent and naturally generate a high volume of entries. We allow duplicate entries in the inventory table for the same user and item SKU, which simulates item stacks. While we don’t currently consolidate these stacks like Minecraft, but this setup provides flexibility for implementing stack management logic in the future. 
This overall distribution reflects how a real world game backend might scale.


# Performance results of hitting endpoints
TODO

# Performance tuning


EXPLAIN BEFORE INDEX

EXPLAIN ANALYZE
SELECT * FROM floor
ORDER BY dropped_at DESC;


| QUERY PLAN                                                                                                     |
| -------------------------------------------------------------------------------------------------------------- |
| Sort  (cost=828.39..853.39 rows=10000 width=21) (actual time=3.162..4.024 rows=10000 loops=1)                  |
|   Sort Key: dropped_at DESC                                                                                    |
|   Sort Method: quicksort  Memory: 1010kB                                                                       |
|   ->  Seq Scan on floor  (cost=0.00..164.00 rows=10000 width=21) (actual time=0.020..0.891 rows=10000 loops=1) |
| Planning Time: 0.278 ms                                                                                        |
| Execution Time: 4.608 ms                                                                                       |



EXPLAIN AFTER INDEX

CREATE INDEX idx_floor_dropped_at_desc
ON floor (dropped_at DESC);

EXPLAIN ANALYZE
SELECT * FROM floor
ORDER BY dropped_at DESC;


| QUERY PLAN                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------------------ |
| Index Scan using idx_floor_dropped_at_desc on floor  (cost=0.29..253.68 rows=10000 width=21) (actual time=0.025..4.274 rows=10000 loops=1) |
| Planning Time: 0.364 ms                                                                                                                    |
| Execution Time: 4.746 ms                                                                                                                   |


To optimize the slowest endpoint (/world/view), We used EXPLAIN ANALYZE on the query SELECT * FROM floor ORDER BY dropped_at DESC and saw that the database performed a sequential scan followed by a sort, which is inefficient as data grows. The actual execution time was about 4.6 ms. To improve performance, We added an index on the dropped_at column in descending order using CREATE INDEX idx_floor_dropped_at_desc ON floor (dropped_at DESC);. After rerunning EXPLAIN ANALYZE, the query used an index scan instead, which avoids sorting and is better for scalability. Although the actual execution time after indexing was similar (around 4.7 ms), the database is now using a more efficient access path. This change prepares the system to handle larger datasets more efficiently, making the endpoint more scalable and performant in the long run.
