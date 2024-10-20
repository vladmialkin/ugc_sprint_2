sh.addShard("mongo_rs1/mongo_rs1_n1:27017,mongo_rs1_n2:27017")
sh.addShard("mongo_rs2/mongo_rs2_n1:27017,mongo_rs2_n2:27017")
sh.enableSharding("test_db")
db.createCollection("test_db.bookmarks")
db.createCollection("test_db.rating")
db.createCollection("test_db.reviews")
sh.shardCollection("posts_db.rating", {"id": "hashed"})
sh.shardCollection("posts_db.reviews", {"id": "hashed"})