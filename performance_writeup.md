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
| QUERY PLAN                                                                                               |
| -------------------------------------------------------------------------------------------------------- |
| Sort  (cost=74.54..77.21 rows=1070 width=48) (actual time=0.041..0.041 rows=0 loops=1)                   |
|   Sort Key: dropped_at DESC                                                                              |
|   Sort Method: quicksort  Memory: 25kB                                                                   |
|   ->  Seq Scan on floor  (cost=0.00..20.70 rows=1070 width=48) (actual time=0.009..0.009 rows=0 loops=1) |
| Planning Time: 0.284 ms                                                                                  |
| Execution Time: 0.101 ms                                                                                 |
