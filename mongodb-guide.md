---
title: "MongoDB Complete Guide"
description: "A production-ready, comprehensive reference for MongoDB — from basics to advanced operations, Python integration, security, and real-world troubleshooting."
---

# MongoDB Complete Guide

> **A production-ready reference covering MongoDB fundamentals, CLI, data modeling, performance, Python integration, replication, security, and real-world troubleshooting.**

---

## Table of Contents

1. [Introduction to MongoDB](#1-introduction-to-mongodb)
2. [MongoDB Basics](#2-mongodb-basics)
   - [Installation](#21-installation)
   - [BSON](#22-bson)
   - [CRUD Operations](#23-crud-operations)
   - [Data Types](#24-data-types)
3. [MongoDB CLI Commands](#3-mongodb-cli-commands)
   - [mongosh](#31-mongosh)
   - [mongoimport / mongoexport](#32-mongoimport--mongoexport)
   - [mongodump / mongorestore](#33-mongodump--mongorestore)
   - [Common Admin Commands](#34-common-admin-commands)
4. [Data Modeling](#4-data-modeling)
   - [Embedding vs Referencing](#41-embedding-vs-referencing)
   - [Schema Design Patterns](#42-schema-design-patterns)
   - [Schema Evolution](#43-schema-evolution)
5. [Indexing & Aggregation](#5-indexing--aggregation)
   - [Index Types](#51-index-types)
   - [Compound Indexes](#52-compound-indexes)
   - [Text, TTL, and Geospatial Indexes](#53-text-ttl-and-geospatial-indexes)
   - [Aggregation Pipeline](#54-aggregation-pipeline)
6. [Performance Tuning](#6-performance-tuning)
   - [Explain Plans](#61-explain-plans)
   - [Profiler](#62-profiler)
   - [Query Optimization](#63-query-optimization)
   - [Connection Pooling](#64-connection-pooling)
   - [Hardware Considerations](#65-hardware-considerations)
7. [Working with Python](#7-working-with-python)
   - [PyMongo Setup](#71-pymongo-setup)
   - [CRUD with PyMongo](#72-crud-with-pymongo)
   - [Bulk Operations](#73-bulk-operations)
   - [Transactions](#74-transactions)
   - [Change Streams](#75-change-streams)
   - [Async with Motor](#76-async-with-motor)
8. [Replication, Sharding, Backup & Monitoring](#8-replication-sharding-backup--monitoring)
9. [Security & Compliance](#9-security--compliance)
10. [Limitations & Real-World Issues](#10-limitations--real-world-issues)
11. [Best Practices & Cheatsheet](#11-best-practices--cheatsheet)
12. [Appendix](#12-appendix)

---

## 1. Introduction to MongoDB

> MongoDB is a document-oriented NoSQL database that stores data as flexible JSON-like BSON documents, offering horizontal scalability and a rich query language.

MongoDB was created by 10gen (now MongoDB, Inc.) in 2007 and open-sourced in 2009. It stores records as **documents** (similar to JSON objects) within **collections** (analogous to tables), grouped into **databases**.

### Why MongoDB?

| Feature | MongoDB | Relational DB (PostgreSQL) |
|---|---|---|
| Schema | Flexible (schemaless) | Rigid (predefined) |
| Scalability | Horizontal (sharding) | Vertical (primarily) |
| Joins | `$lookup` aggregation | Native SQL JOINs |
| Transactions | Multi-document (v4.0+) | Full ACID |
| Query Language | MQL (MongoDB Query Language) | SQL |
| Best For | Hierarchical/variable data, rapid iteration | Structured data, complex relationships |
| Replication | Replica Sets | Streaming replication |

### Core Concepts

- **Document**: A BSON record (analogous to a row). Max size: 16 MB.
- **Collection**: A group of documents (analogous to a table). Schema-free.
- **Database**: A namespace holding collections.
- **`_id`**: Every document has a unique `_id` field (default: `ObjectId`).
- **Replica Set**: A group of MongoDB instances maintaining the same data for high availability.
- **Shard**: A subset of data distributed across nodes for horizontal scaling.

---

## 2. MongoDB Basics

> This section covers installing MongoDB, understanding BSON, performing CRUD operations, and working with MongoDB's data types.

### 2.1 Installation

#### Linux (Ubuntu/Debian)

```bash
# Import the MongoDB public GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
  sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg

# Add the repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
  https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Install
sudo apt update && sudo apt install -y mongodb-org

# Start and enable the service
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify
mongod --version
```

#### macOS (Homebrew)

```bash
brew tap mongodb/brew
brew update
brew install mongodb-community@7.0

# Start as a service
brew services start mongodb-community@7.0
```

#### Docker (Recommended for Dev)

```bash
# Pull and run MongoDB
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -v mongo_data:/data/db \
  mongo:7.0

# Connect
docker exec -it mongodb mongosh -u admin -p secret --authenticationDatabase admin
```

---

### 2.2 BSON

> BSON (Binary JSON) is the binary serialization format MongoDB uses to store documents — a superset of JSON with additional types.

BSON extends JSON with types like `Date`, `ObjectId`, `Binary`, `Decimal128`, and `Int32`/`Int64`. This enables precise numeric typing and efficient binary encoding.

```javascript
// BSON document example in mongosh
{
  _id: ObjectId("64f1a2b3c4d5e6f7a8b9c0d1"),   // 12-byte unique identifier
  name: "Alice",
  age: NumberInt(30),                            // 32-bit integer
  balance: NumberDecimal("9999.99"),             // Decimal128 for financial data
  created_at: ISODate("2024-01-15T10:30:00Z"),  // BSON Date
  metadata: {                                    // Nested document
    tags: ["admin", "user"],                     // Array
    active: true
  },
  avatar: BinData(0, "base64encodedstring=="),   // Binary data
  score: NumberLong("123456789012345")           // 64-bit integer
}
```

**BSON vs JSON size:** BSON can be larger than equivalent JSON for small strings, but enables faster traversal and richer types.

---

### 2.3 CRUD Operations

> The four fundamental operations: Create, Read, Update, Delete.

#### Example 1: Create

```javascript
// mongosh

// Insert one document
db.users.insertOne({
  name: "Alice",
  email: "alice@example.com",
  age: 30,
  roles: ["admin"],
  created_at: new Date()
})

// Insert many documents
db.users.insertMany([
  { name: "Bob", email: "bob@example.com", age: 25, roles: ["user"] },
  { name: "Carol", email: "carol@example.com", age: 35, roles: ["user", "editor"] }
])
```

#### Example 2: Read

```javascript
// Find all users
db.users.find()

// Find with filter and projection
db.users.find(
  { age: { $gte: 25 }, roles: "admin" },  // filter
  { name: 1, email: 1, _id: 0 }           // projection: include name/email, exclude _id
)

// Find one
db.users.findOne({ email: "alice@example.com" })

// Sorting, limiting, skipping
db.users.find().sort({ age: -1 }).skip(0).limit(10)

// Count documents
db.users.countDocuments({ age: { $gte: 30 } })
```

#### Example 3: Update

```javascript
// Update one document
db.users.updateOne(
  { email: "alice@example.com" },
  {
    $set: { age: 31, "metadata.last_login": new Date() },
    $addToSet: { roles: "editor" }          // Add to array only if not exists
  }
)

// Update many
db.users.updateMany(
  { roles: "user" },
  { $set: { subscription: "free" } }
)

// Upsert: insert if not exists
db.users.updateOne(
  { email: "dave@example.com" },
  { $set: { name: "Dave", age: 28 } },
  { upsert: true }
)

// Replace entire document (except _id)
db.users.replaceOne(
  { email: "bob@example.com" },
  { email: "bob@example.com", name: "Robert", age: 26 }
)
```

#### Example 4: Delete

```javascript
// Delete one document
db.users.deleteOne({ email: "dave@example.com" })

// Delete many
db.users.deleteMany({ roles: "user", age: { $lt: 20 } })

// Delete all documents in collection (preserves collection and indexes)
db.users.deleteMany({})

// Drop entire collection (removes data + indexes)
db.users.drop()
```

---

### 2.4 Data Types

| BSON Type | Description | mongosh Example |
|---|---|---|
| `Double` | 64-bit float | `3.14` |
| `String` | UTF-8 string | `"hello"` |
| `Object` | Embedded document | `{ key: value }` |
| `Array` | Ordered list | `[1, 2, 3]` |
| `ObjectId` | 12-byte unique ID | `ObjectId("...")` |
| `Boolean` | true/false | `true` |
| `Date` | UTC datetime | `ISODate("2024-01-01")` |
| `Null` | Null value | `null` |
| `Int32` | 32-bit integer | `NumberInt(42)` |
| `Int64` | 64-bit integer | `NumberLong(1234567890)` |
| `Decimal128` | High-precision decimal | `NumberDecimal("9.99")` |
| `Binary` | Binary data | `BinData(0, "...")` |
| `Timestamp` | Internal BSON timestamp | `Timestamp(1, 1)` |
| `Regular Expression` | BSON regex | `/pattern/i` |

> **Production tip:** Use `Decimal128` for monetary values — never `Double` (floating point imprecision).

---

## 3. MongoDB CLI Commands

> The MongoDB shell (`mongosh`) and companion tools provide complete access to databases, collections, import/export, backup, and administration.

### 3.1 mongosh

`mongosh` is the modern MongoDB shell (replaces the legacy `mongo`).

```bash
# Connect with URI
mongosh "mongodb://username:password@host:27017/dbname"

# Connect to replica set
mongosh "mongodb://host1:27017,host2:27017,host3:27017/dbname?replicaSet=rs0"

# Connect to Atlas
mongosh "mongodb+srv://user:pass@cluster.mongodb.net/dbname"
```

```javascript
// mongosh — useful session commands

show dbs                    // List all databases
use mydb                    // Switch to / create database
show collections            // List collections in current db
db.stats()                  // Database statistics
db.collection.stats()       // Collection statistics
db.serverStatus()           // Server-level metrics
db.currentOp()              // Active operations
db.killOp(opId)             // Kill a running operation
db.adminCommand({ ping: 1}) // Verify connectivity
```

---

### 3.2 mongoimport / mongoexport

```bash
# Export collection to JSON
mongoexport \
  --uri="mongodb://localhost:27017" \
  --db=mydb \
  --collection=users \
  --out=users.json \
  --jsonArray

# Export with query filter
mongoexport \
  --uri="mongodb://localhost:27017" \
  --db=mydb \
  --collection=orders \
  --query='{"status": "completed"}' \
  --out=completed_orders.json

# Export to CSV
mongoexport \
  --uri="mongodb://localhost:27017" \
  --db=mydb \
  --collection=products \
  --type=csv \
  --fields=name,price,category \
  --out=products.csv

# Import from JSON
mongoimport \
  --uri="mongodb://localhost:27017" \
  --db=mydb \
  --collection=users \
  --file=users.json \
  --jsonArray \
  --drop           # Drop collection before import

# Import from CSV
mongoimport \
  --uri="mongodb://localhost:27017" \
  --db=mydb \
  --collection=products \
  --type=csv \
  --headerline \
  --file=products.csv
```

---

### 3.3 mongodump / mongorestore

```bash
# Dump entire server
mongodump \
  --uri="mongodb://localhost:27017" \
  --out=/backups/dump_$(date +%Y%m%d)

# Dump single database
mongodump \
  --uri="mongodb://localhost:27017" \
  --db=mydb \
  --out=/backups/

# Dump single collection with compression
mongodump \
  --uri="mongodb://localhost:27017" \
  --db=mydb \
  --collection=orders \
  --gzip \
  --archive=/backups/orders.archive

# Restore entire dump
mongorestore \
  --uri="mongodb://localhost:27017" \
  --drop \              # Drop before restore
  /backups/dump_20240101/

# Restore compressed archive
mongorestore \
  --uri="mongodb://localhost:27017" \
  --gzip \
  --archive=/backups/orders.archive \
  --nsInclude="mydb.orders"
```

---

### 3.4 Common Admin Commands

```javascript
// mongosh — administration

// --- User Management ---
db.createUser({
  user: "appuser",
  pwd: "securepassword",
  roles: [
    { role: "readWrite", db: "mydb" },
    { role: "read", db: "reporting" }
  ]
})

db.changeUserPassword("appuser", "newpassword")
db.dropUser("appuser")
db.getUsers()

// --- Replica Set Admin ---
rs.initiate()
rs.status()
rs.add("host2:27017")
rs.remove("host3:27017")
rs.stepDown()             // Step down primary

// --- Index Management ---
db.users.getIndexes()
db.users.dropIndex("email_1")
db.users.dropIndexes()    // Drop all non-_id indexes

// --- Maintenance ---
db.runCommand({ compact: "users" })       // Defragment collection
db.runCommand({ repairDatabase: 1 })      // Repair database (legacy)
db.adminCommand({ fsync: 1, lock: 1 })   // Lock for backup
db.adminCommand({ fsyncUnlock: 1 })      // Unlock after backup

// --- Collection Management ---
db.createCollection("logs", {
  capped: true,
  size: 10485760,    // 10 MB max
  max: 100000        // 100k documents max
})
db.users.renameCollection("customers")
```

---

## 4. Data Modeling

> Effective data modeling in MongoDB requires choosing between embedding related data in a single document or referencing it via IDs, guided by access patterns.

### 4.1 Embedding vs Referencing

The central design decision in MongoDB data modeling.

#### Embedding (Denormalization)

Store related data **inside** the same document.

```javascript
// Embedded model: User with addresses
{
  _id: ObjectId("..."),
  name: "Alice",
  email: "alice@example.com",
  addresses: [
    { type: "home", street: "123 Main St", city: "Austin", zip: "78701" },
    { type: "work", street: "456 Corp Ave", city: "Austin", zip: "78702" }
  ],
  payment_methods: [
    { type: "card", last4: "4242", brand: "Visa", expires: "12/26" }
  ]
}
```

**Use embedding when:**
- Data is always accessed together with the parent
- The embedded data is owned by the parent (one-to-few relationship)
- The embedded array won't grow unboundedly
- Read performance is critical

#### Referencing (Normalization)

Store related data in **separate collections** and link via IDs.

```javascript
// Referencing model: User references Orders

// users collection
{ _id: ObjectId("u001"), name: "Alice", email: "alice@example.com" }

// orders collection
{
  _id: ObjectId("o001"),
  user_id: ObjectId("u001"),    // Reference to user
  items: [...],
  total: 99.99,
  created_at: ISODate("2024-01-15")
}
```

**Use referencing when:**
- Data is accessed independently
- One-to-many or many-to-many relationships exist
- Related data is frequently updated in isolation
- Embedded arrays could grow very large (thousands of items)

#### Decision Matrix

| Criteria | Embed | Reference |
|---|---|---|
| Relationship cardinality | One-to-few | One-to-many / many-to-many |
| Access pattern | Always together | Often independently |
| Data ownership | Child owned by parent | Independent entities |
| Update frequency | Rarely updated separately | Frequently updated |
| Array growth | Bounded | Unbounded |
| Document size concern | Small | Large |

---

### 4.2 Schema Design Patterns

#### Bucket Pattern

Group time-series or sequential data into buckets to reduce document count and improve range queries.

```javascript
// Instead of one document per measurement:
// { sensor_id: "S1", ts: ISODate("2024-01-01T00:01:00"), value: 23.5 }
// { sensor_id: "S1", ts: ISODate("2024-01-01T00:02:00"), value: 23.7 }
// ... (millions of docs)

// Bucket by hour:
{
  sensor_id: "S1",
  bucket_start: ISODate("2024-01-01T00:00:00"),
  bucket_end: ISODate("2024-01-01T01:00:00"),
  measurements: [
    { ts: ISODate("2024-01-01T00:01:00"), value: 23.5 },
    { ts: ISODate("2024-01-01T00:02:00"), value: 23.7 },
    // ... up to 60 measurements per bucket
  ],
  count: 60,
  min: 23.1,
  max: 24.2,
  avg: 23.6
}
```

#### Computed Pattern

Pre-calculate expensive aggregations and store the result.

```javascript
// product_reviews collection has thousands of reviews per product.
// Instead of computing avg rating on every request:

// products collection — computed field updated on each new review
{
  _id: ObjectId("..."),
  name: "Widget Pro",
  review_stats: {                  // Pre-computed, updated on insert/update
    count: 1248,
    average: 4.3,
    distribution: { 5: 650, 4: 350, 3: 150, 2: 60, 1: 38 }
  }
}
```

#### Outlier Pattern

Handle documents that would otherwise exceed limits or cause issues for most queries.

```javascript
// Most users have <50 followers. A celebrity may have 10M.
// Base user document
{
  _id: ObjectId("..."),
  name: "Taylor",
  followers: [/* first 1000 IDs */],
  has_extras: true             // Flag when followers overflow
}

// Overflow documents in user_followers_overflow collection
{
  user_id: ObjectId("..."),
  followers: [/* additional follower IDs, paginated */],
  page: 2
}
```

#### Polymorphic Pattern

Store different types of entities in the same collection when they share common queries.

```javascript
// vehicles collection
{ _id: ObjectId("..."), type: "car",   make: "Toyota", seats: 5, doors: 4 }
{ _id: ObjectId("..."), type: "truck", make: "Ford",   payload_kg: 2000, axles: 2 }
{ _id: ObjectId("..."), type: "bike",  make: "Trek",   gears: 21, frame: "aluminum" }

// Query works on all types
db.vehicles.find({ make: "Toyota" })
```

---

### 4.3 Schema Evolution

MongoDB's flexible schema makes schema changes easier than SQL migrations, but still requires care.

```javascript
// Strategy 1: Add optional fields (backward compatible)
db.users.updateMany(
  { subscription: { $exists: false } },
  { $set: { subscription: "free", subscription_updated_at: new Date() } }
)

// Strategy 2: Schema versioning
// Add a schema_version field to track document structure
db.users.updateMany({}, { $set: { schema_version: 2 } })

// Application-level migration helper
function migrateUser(doc) {
  if (doc.schema_version === 1) {
    // Transform v1 to v2 structure on read
    doc.full_name = `${doc.first_name} ${doc.last_name}`;
    doc.schema_version = 2;
  }
  return doc;
}

// Strategy 3: Use $jsonSchema validator for new documents
db.runCommand({
  collMod: "users",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "email", "schema_version"],
      properties: {
        name:           { bsonType: "string" },
        email:          { bsonType: "string", pattern: "^.+@.+$" },
        schema_version: { bsonType: "int", minimum: 1 }
      }
    }
  },
  validationLevel: "moderate",   // Only validates new/updated docs
  validationAction: "warn"       // Log instead of reject on violation
})
```

---

## 5. Indexing & Aggregation

> Indexes dramatically improve query performance; the aggregation pipeline processes and transforms documents through a sequence of stages.

### 5.1 Index Types

```javascript
// Single field index
db.users.createIndex({ email: 1 })              // Ascending
db.users.createIndex({ created_at: -1 })        // Descending

// Unique index
db.users.createIndex({ email: 1 }, { unique: true })

// Sparse index (only indexes documents where field exists)
db.users.createIndex({ phone: 1 }, { sparse: true })

// Partial index (index only matching documents — more efficient than sparse)
db.orders.createIndex(
  { created_at: -1 },
  { partialFilterExpression: { status: { $in: ["pending", "processing"] } } }
)

// Background index build (non-blocking in older versions; default in v4.2+)
db.users.createIndex({ name: 1 }, { background: true })

// View all indexes
db.users.getIndexes()
```

---

### 5.2 Compound Indexes

Compound indexes cover multiple fields and follow the **ESR rule**: Equality → Sort → Range.

```javascript
// ESR rule example:
// Query: Find active users by country, sorted by created_at, where age > 18
db.users.find(
  { status: "active", country: "US", age: { $gt: 18 } }
).sort({ created_at: -1 })

// Optimal compound index (Equality first, Sort second, Range last)
db.users.createIndex({
  status: 1,       // E: Equality
  country: 1,      // E: Equality
  created_at: -1,  // S: Sort (match sort direction)
  age: 1           // R: Range
})

// Index prefix usage
// Index on { a: 1, b: 1, c: 1 } supports queries on:
//   { a: 1 }
//   { a: 1, b: 1 }
//   { a: 1, b: 1, c: 1 }
// But NOT: { b: 1 } or { b: 1, c: 1 } (must start with prefix)
```

---

### 5.3 Text, TTL, and Geospatial Indexes

#### Text Index

```javascript
// Create text index (one per collection)
db.articles.createIndex(
  { title: "text", body: "text", tags: "text" },
  { weights: { title: 10, tags: 5, body: 1 } }   // Relevance weights
)

// Text search query
db.articles.find(
  { $text: { $search: "mongodb performance tuning" } },
  { score: { $meta: "textScore" } }                // Include relevance score
).sort({ score: { $meta: "textScore" } })

// Phrase search and exclusion
db.articles.find({
  $text: { $search: '"replica set" -sharding' }    // Exact phrase, exclude term
})
```

#### TTL Index (Time-To-Live)

```javascript
// Automatically delete documents after 24 hours
db.sessions.createIndex(
  { created_at: 1 },
  { expireAfterSeconds: 86400 }     // 24 * 60 * 60
)

// Expire at a specific time (set expireAfterSeconds to 0, use a Date field)
db.scheduled_jobs.createIndex(
  { expires_at: 1 },
  { expireAfterSeconds: 0 }         // Delete when expires_at is in the past
)
```

#### Geospatial Index

```javascript
// 2dsphere index for GeoJSON data
db.locations.createIndex({ geo: "2dsphere" })

// Insert GeoJSON point
db.locations.insertOne({
  name: "Coffee Shop",
  geo: {
    type: "Point",
    coordinates: [-73.9857, 40.7484]   // [longitude, latitude]
  }
})

// Find locations within 1km radius
db.locations.find({
  geo: {
    $near: {
      $geometry: { type: "Point", coordinates: [-73.9857, 40.7484] },
      $maxDistance: 1000    // meters
    }
  }
})
```

---

### 5.4 Aggregation Pipeline

The aggregation pipeline transforms documents through sequential stages.

```javascript
// Example 5: Complex aggregation — Monthly revenue by category
db.orders.aggregate([
  // Stage 1: Filter completed orders in 2024
  {
    $match: {
      status: "completed",
      created_at: {
        $gte: ISODate("2024-01-01"),
        $lt: ISODate("2025-01-01")
      }
    }
  },

  // Stage 2: Unwind items array
  { $unwind: "$items" },

  // Stage 3: Lookup product details
  {
    $lookup: {
      from: "products",
      localField: "items.product_id",
      foreignField: "_id",
      as: "product"
    }
  },
  { $unwind: "$product" },

  // Stage 4: Project and compute fields
  {
    $project: {
      month: { $month: "$created_at" },
      year: { $year: "$created_at" },
      category: "$product.category",
      revenue: { $multiply: ["$items.qty", "$items.price"] }
    }
  },

  // Stage 5: Group by year, month, category
  {
    $group: {
      _id: { year: "$year", month: "$month", category: "$category" },
      total_revenue: { $sum: "$revenue" },
      order_count: { $sum: 1 }
    }
  },

  // Stage 6: Sort
  { $sort: { "_id.year": 1, "_id.month": 1, "total_revenue": -1 } },

  // Stage 7: Shape output
  {
    $project: {
      _id: 0,
      year: "$_id.year",
      month: "$_id.month",
      category: "$_id.category",
      total_revenue: { $round: ["$total_revenue", 2] },
      order_count: 1
    }
  }
])
```

#### Common Aggregation Operators

| Operator | Stage | Description |
|---|---|---|
| `$match` | Filter | Filter documents (use early to reduce dataset) |
| `$group` | Group | Group by key, apply accumulators (`$sum`, `$avg`, `$min`, `$max`) |
| `$project` | Transform | Include/exclude/reshape fields |
| `$sort` | Sort | Sort documents |
| `$limit` / `$skip` | Paginate | Pagination |
| `$unwind` | Flatten | Deconstruct arrays |
| `$lookup` | Join | Left outer join from another collection |
| `$addFields` | Add | Add computed fields |
| `$facet` | Multi-pipeline | Run multiple aggregation pipelines on same input |
| `$bucket` | Bucket | Categorize into buckets by expression |
| `$out` / `$merge` | Write | Write results to a collection |

---

## 6. Performance Tuning

> MongoDB performance depends on proper indexing, understanding query plans, profiling slow operations, and appropriate hardware configuration.

### 6.1 Explain Plans

```javascript
// Analyze query execution
db.users.find({ status: "active", age: { $gte: 25 } })
  .explain("executionStats")

// Key fields to check in explain output:
// - winningPlan.stage: Should be IXSCAN (index scan), not COLLSCAN (full scan)
// - executionStats.nReturned: Documents returned
// - executionStats.totalDocsExamined: Documents scanned
// - executionStats.totalKeysExamined: Index keys scanned
// - executionStats.executionTimeMillis: Query duration

// Ideal: nReturned ≈ totalDocsExamined (index selectivity is high)
// Bad: totalDocsExamined >> nReturned (low selectivity or no index)

// Verbose mode shows rejected plans
db.users.find({ status: "active" }).explain("allPlansExecution")
```

---

### 6.2 Profiler

```javascript
// Enable profiler: level 0=off, 1=slow ops only, 2=all ops
db.setProfilingLevel(1, { slowms: 100 })   // Log ops slower than 100ms

// Check current profiling level
db.getProfilingLevel()
db.getProfilingStatus()

// Query the profiler collection
db.system.profile.find(
  { millis: { $gt: 100 } },
  { op: 1, ns: 1, millis: 1, ts: 1, query: 1 }
).sort({ ts: -1 }).limit(20)

// Find the slowest queries
db.system.profile.aggregate([
  { $group: {
    _id: "$ns",
    max_ms: { $max: "$millis" },
    avg_ms: { $avg: "$millis" },
    count: { $sum: 1 }
  }},
  { $sort: { avg_ms: -1 } }
])
```

---

### 6.3 Query Optimization

```javascript
// 1. Use covered queries (all fields in index, no doc fetch needed)
db.users.createIndex({ status: 1, age: 1, name: 1 })
db.users.find(
  { status: "active" },
  { _id: 0, status: 1, age: 1, name: 1 }   // Only projected fields from index
)

// 2. Use projection to limit returned fields
db.orders.find({}, { items: 1, total: 1 })  // Only fetch needed fields

// 3. Avoid negation operators ($ne, $nin, $not) — cannot use indexes efficiently
// Bad:
db.users.find({ status: { $ne: "deleted" } })
// Better (if possible):
db.users.find({ status: { $in: ["active", "inactive", "suspended"] } })

// 4. Use $elemMatch for array queries
// Bad (scans all elements):
db.users.find({ "scores.value": { $gte: 90 } })
// Better (targets single element):
db.users.find({ scores: { $elemMatch: { type: "math", value: { $gte: 90 } } } })

// 5. Use hint() to force a specific index
db.orders.find({ user_id: ObjectId("..."), status: "pending" })
  .hint({ user_id: 1, status: 1 })
```

---

### 6.4 Connection Pooling

```javascript
// MongoDB driver connection pool configuration
// In URI format:
// mongodb://host:27017/db?maxPoolSize=100&minPoolSize=5&maxIdleTimeMS=60000

// PyMongo:
from pymongo import MongoClient
client = MongoClient(
    "mongodb://localhost:27017",
    maxPoolSize=100,       # Max connections in pool
    minPoolSize=5,         # Min connections maintained
    maxIdleTimeMS=60000,   # Close idle connections after 60s
    waitQueueTimeoutMS=5000  # Raise error if pool exhausted after 5s
)

// Node.js (mongoose):
mongoose.connect(uri, {
  maxPoolSize: 10,
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000
})
```

**Pool sizing rule:** Start with `maxPoolSize = (num_cores * 2) + disk_spindles`. Monitor with `db.serverStatus().connections`.

---

### 6.5 Hardware Considerations

| Resource | Recommendation | Notes |
|---|---|---|
| RAM | Working set fits in RAM | MongoDB relies heavily on OS page cache |
| Storage | NVMe SSD | HDDs cause severe latency under write load |
| CPU | Multi-core | Parallelism for aggregations and concurrent ops |
| Network | Low latency between replica members | High latency causes replication lag |
| NUMA | Disable or configure NUMA | MongoDB recommends disabling NUMA on Linux |
| Transparent Huge Pages | Disable THP | MongoDB requires THP disabled; can cause high latency |
| Filesystem | XFS or ext4 | ext4 for older systems; XFS recommended |

```bash
# Disable Transparent Huge Pages (production requirement)
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/defrag

# Add to /etc/rc.local for persistence
```

---

## 7. Working with Python

> PyMongo is the official synchronous Python driver; Motor provides async support built on top of PyMongo.

### 7.1 PyMongo Setup

```bash
pip install pymongo[srv]   # Include DNS SRV support for Atlas
pip install motor          # For async
```

```python
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# Connect
client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)

# Test connection
try:
    client.admin.command("ping")
    print("Connected to MongoDB")
except ConnectionFailure as e:
    print(f"Connection failed: {e}")

db = client["mydb"]
users = db["users"]
```

---

### 7.2 CRUD with PyMongo

```python
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
col = db["users"]

# --- Create ---
result = col.insert_one({
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30,
    "created_at": datetime.utcnow()
})
print(f"Inserted: {result.inserted_id}")

result = col.insert_many([
    {"name": "Bob", "email": "bob@example.com", "age": 25},
    {"name": "Carol", "email": "carol@example.com", "age": 35}
])
print(f"Inserted {len(result.inserted_ids)} documents")

# --- Read ---
user = col.find_one({"email": "alice@example.com"})

# Find with filter, projection, sort, limit
cursor = col.find(
    {"age": {"$gte": 25}},
    {"_id": 0, "name": 1, "email": 1}
).sort("age", ASCENDING).limit(10)

for doc in cursor:
    print(doc)

# Count
count = col.count_documents({"age": {"$gte": 25}})

# --- Update ---
col.update_one(
    {"email": "alice@example.com"},
    {"$set": {"age": 31, "updated_at": datetime.utcnow()}}
)

col.update_many(
    {"age": {"$lt": 18}},
    {"$set": {"category": "minor"}}
)

# Upsert
col.update_one(
    {"email": "new@example.com"},
    {"$setOnInsert": {"name": "New User", "created_at": datetime.utcnow()}},
    upsert=True
)

# --- Delete ---
col.delete_one({"email": "bob@example.com"})
col.delete_many({"age": {"$lt": 18}})

# --- Aggregation ---
pipeline = [
    {"$match": {"age": {"$gte": 25}}},
    {"$group": {"_id": None, "avg_age": {"$avg": "$age"}, "count": {"$sum": 1}}}
]
for result in col.aggregate(pipeline):
    print(result)
```

---

### 7.3 Bulk Operations

```python
# Example 6: Bulk write for high-throughput scenarios
from pymongo import InsertOne, UpdateOne, DeleteOne, ReplaceOne
from pymongo.errors import BulkWriteError

col = db["products"]

operations = [
    InsertOne({"sku": "WIDGET-001", "name": "Widget", "price": 9.99, "stock": 100}),
    UpdateOne(
        {"sku": "WIDGET-002"},
        {"$inc": {"stock": -5}, "$set": {"updated_at": datetime.utcnow()}}
    ),
    ReplaceOne(
        {"sku": "WIDGET-003"},
        {"sku": "WIDGET-003", "name": "New Widget Pro", "price": 19.99},
        upsert=True
    ),
    DeleteOne({"sku": "WIDGET-DISCONTINUED"}),
]

try:
    result = col.bulk_write(operations, ordered=False)  # ordered=False = fail-fast off
    print(f"Inserted: {result.inserted_count}")
    print(f"Updated: {result.modified_count}")
    print(f"Deleted: {result.deleted_count}")
except BulkWriteError as e:
    print(f"Bulk write errors: {e.details}")
```

---

### 7.4 Transactions

```python
# Example 7: Multi-document ACID transaction
from pymongo import MongoClient
from pymongo.errors import OperationFailure

client = MongoClient("mongodb://localhost:27017/")  # Must be replica set
db = client["banking"]
accounts = db["accounts"]
audit = db["audit_log"]

def transfer_funds(from_id: str, to_id: str, amount: float):
    with client.start_session() as session:
        with session.start_transaction():
            # Debit source account
            result = accounts.update_one(
                {"_id": from_id, "balance": {"$gte": amount}},
                {"$inc": {"balance": -amount}},
                session=session
            )
            if result.modified_count == 0:
                raise OperationFailure("Insufficient funds or account not found")

            # Credit destination account
            accounts.update_one(
                {"_id": to_id},
                {"$inc": {"balance": amount}},
                session=session
            )

            # Log the transaction
            audit.insert_one({
                "type": "transfer",
                "from": from_id,
                "to": to_id,
                "amount": amount,
                "ts": datetime.utcnow()
            }, session=session)
        # Transaction commits on exiting the context (or rolls back on exception)

try:
    transfer_funds("ACC001", "ACC002", 500.00)
    print("Transfer complete")
except OperationFailure as e:
    print(f"Transfer failed: {e}")
```

---

### 7.5 Change Streams

```python
# Example 8: Real-time change streams (requires replica set)
import threading

def watch_orders():
    col = db["orders"]
    pipeline = [
        {"$match": {
            "operationType": {"$in": ["insert", "update"]},
            "fullDocument.status": "pending"
        }}
    ]

    # resume_after allows resuming after a disconnect
    with col.watch(pipeline, full_document="updateLookup") as stream:
        for change in stream:
            op_type = change["operationType"]
            doc = change.get("fullDocument", {})
            print(f"[{op_type.upper()}] Order {doc.get('_id')}: {doc.get('status')}")
            # Process the change (e.g., trigger notification)

# Run in background thread
thread = threading.Thread(target=watch_orders, daemon=True)
thread.start()
```

---

### 7.6 Async with Motor

```python
# Example 9: Async MongoDB with Motor
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def main():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client["mydb"]
    col = db["products"]

    # Async insert
    result = await col.insert_one({
        "name": "Async Widget",
        "price": 14.99,
        "created_at": datetime.utcnow()
    })
    print(f"Inserted: {result.inserted_id}")

    # Async find
    async for doc in col.find({"price": {"$gt": 10}}):
        print(doc["name"], doc["price"])

    # Async aggregation
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$price"}, "count": {"$sum": 1}}}
    ]
    async for result in col.aggregate(pipeline):
        print(f"Total: {result['total']}, Count: {result['count']}")

    client.close()

asyncio.run(main())
```

#### FastAPI + Motor Integration

```python
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["mydb"]

@app.on_event("startup")
async def startup():
    await db.command("ping")

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    doc = await db.users.find_one({"_id": ObjectId(user_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="User not found")
    doc["_id"] = str(doc["_id"])
    return doc
```

---

## 8. Replication, Sharding, Backup & Monitoring

> Replication provides high availability; sharding provides horizontal scalability; together they form the backbone of production MongoDB deployments.

### Replica Sets

A **Replica Set** is a group of MongoDB instances (typically 3 or 5) that maintain the same data. One node is the **primary** (handles writes); others are **secondaries** (replicate from primary and handle reads if configured).

```javascript
// Initialize a 3-node replica set (run on primary node)
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017", priority: 2 },   // Preferred primary
    { _id: 1, host: "mongo2:27017", priority: 1 },
    { _id: 2, host: "mongo3:27017", priority: 0, hidden: true, votes: 0 } // Hidden secondary for backups
  ]
})

// Check replication lag
rs.printSecondaryReplicationInfo()

// Read from secondaries (read preference)
// In URI:
// mongodb://host1,host2,host3/?replicaSet=rs0&readPreference=secondaryPreferred
```

**Read Preference Modes:**

| Mode | Description | Use Case |
|---|---|---|
| `primary` | Default; reads from primary only | Requires strong consistency |
| `primaryPreferred` | Primary if available, else secondary | Tolerate brief secondary reads |
| `secondary` | Always from secondary | Reporting queries, analytics |
| `secondaryPreferred` | Secondary if available, else primary | Distribute read load |
| `nearest` | Lowest network latency | Geographically distributed apps |

---

### Sharding

**Sharding** distributes data across multiple shards (each a replica set) via a **shard key**.

```javascript
// Enable sharding on a database
sh.enableSharding("mydb")

// Shard a collection by hashed _id (even distribution)
sh.shardCollection("mydb.users", { _id: "hashed" })

// Shard by range (good for range queries, risk of hotspots)
sh.shardCollection("mydb.orders", { created_at: 1 })

// Check sharding status
sh.status()

// Move a chunk manually (rarely needed)
sh.moveChunk("mydb.orders", { created_at: ISODate("2024-01-01") }, "shard2")
```

**Shard Key Selection:**

| Criteria | Good Choice | Bad Choice |
|---|---|---|
| Cardinality | High (many unique values) | Low (e.g., boolean) |
| Distribution | Even across shards | Monotonically increasing (_id, timestamp → hotspot) |
| Query alignment | Matches common query patterns | Unrelated to queries |

---

### Backup Strategies

| Strategy | Tool | RPO | Best For |
|---|---|---|---|
| Physical backup | mongodump | Hours | Small-medium datasets |
| Filesystem snapshot | LVM / EBS snapshot | Minutes | Large datasets |
| Continuous backup | MongoDB Atlas / Ops Manager | Seconds | Production |
| Oplog backup | oplog replay | Seconds | Point-in-time recovery |

```bash
# Point-in-time restore using oplog
mongorestore \
  --oplogReplay \
  --oplogLimit=1704067200:1 \   # Timestamp in seconds:ordinal
  /backups/dump/
```

---

### Monitoring

Key metrics to monitor:

```javascript
// Server-level metrics
db.serverStatus()

// Key metrics to alert on:
// opcounters: insert/query/update/delete rates
// connections.current / connections.available
// mem.resident (RAM used by MongoDB process)
// wiredTiger.cache."bytes currently in cache" vs cache maximum
// repl.lag (replication lag in seconds)
// locks.* (lock contention)

// Top — see per-collection operation counts
db.adminCommand({ top: 1 })

// Current operations
db.currentOp({ "secs_running": { $gt: 5 } })  // Ops running > 5 seconds
```

**Recommended monitoring stack:** MongoDB Ops Manager / Atlas Monitoring, or Prometheus + `mongodb_exporter` + Grafana.

---

## 9. Security & Compliance

> A secure MongoDB deployment requires authentication, authorization, encryption, network isolation, and audit logging.

### Authentication

```javascript
// Enable authentication in mongod.conf
// security:
//   authorization: enabled

// Create admin user (run before enabling auth)
use admin
db.createUser({
  user: "root",
  pwd: passwordPrompt(),   // Secure prompt (not plaintext in shell)
  roles: [{ role: "root", db: "admin" }]
})

// Principle of least privilege: application user
db.createUser({
  user: "appuser",
  pwd: passwordPrompt(),
  roles: [
    { role: "readWrite", db: "mydb" },
    { role: "read", db: "reporting" }
  ]
})
```

### Network Security

```yaml
# mongod.conf — production network settings
net:
  port: 27017
  bindIp: 127.0.0.1,10.0.1.5    # Bind to specific IPs only
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/ssl/mongodb.pem
    CAFile: /etc/ssl/ca.pem

security:
  authorization: enabled
  javascriptEnabled: false       # Disable server-side JS if not needed

operationProfiling:
  slowOpThresholdMs: 100
  mode: slowOp
```

### Encryption

```bash
# Encryption at Rest (MongoDB Enterprise / Atlas)
# mongod.conf:
# security:
#   enableEncryption: true
#   encryptionKeyFile: /etc/mongodb/encryption.key

# TLS in connection URI
mongosh "mongodb://host:27017/?tls=true&tlsCAFile=/etc/ssl/ca.pem"

# Field-level encryption (PyMongo example)
from pymongo.encryption import ClientEncryption
from pymongo.encryption_options import AutoEncryptionOpts
```

### Audit Logging (Enterprise)

```yaml
# mongod.conf
auditLog:
  destination: file
  format: JSON
  path: /var/log/mongodb/audit.json
  filter: '{ atype: { $in: ["authenticate", "createCollection", "dropCollection", "createUser", "dropUser"] } }'
```

### Security Checklist

- [ ] Authentication enabled (`security.authorization: enabled`)
- [ ] Default port changed from 27017
- [ ] MongoDB bound to non-public IP
- [ ] TLS/SSL enabled for all connections
- [ ] Least-privilege roles for all application users
- [ ] `mongod` process runs as non-root user
- [ ] Network firewall restricts MongoDB port
- [ ] Encryption at rest enabled
- [ ] Audit logging enabled
- [ ] `javascriptEnabled: false` if not using `$where`/`$function`
- [ ] Regular patching and upgrades

---

## 10. Limitations & Real-World Issues

> Understanding MongoDB's limitations and common failure modes is critical for building resilient production systems.

### Consistency Trade-offs

MongoDB provides **eventual consistency** by default when reading from secondaries. Use write concern and read concern to control this:

```javascript
// Write concern: ensure write is persisted to majority
db.orders.insertOne(
  { ... },
  { writeConcern: { w: "majority", j: true, wtimeout: 5000 } }
)

// Read concern: read only committed data
db.orders.find({}).readConcern("majority")

// Linearizable read concern (strongest, slowest)
db.orders.findOne(
  { _id: orderId },
  { readConcern: { level: "linearizable" } }
)
```

---

### Schema Drift

Without enforcement, collections accumulate inconsistent document structures over time.

**Resolution:**

```javascript
// Audit schema variation
db.users.aggregate([
  { $project: { fields: { $objectToArray: "$$ROOT" } } },
  { $unwind: "$fields" },
  { $group: { _id: "$fields.k", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])

// Enforce via $jsonSchema validator (see Section 4.3)
// Use Mongoose (Node.js) or MongoEngine (Python) schemas
// Document expected schema in README and code
```

---

### Large Documents (>16 MB Limit)

MongoDB enforces a hard 16 MB document limit.

**Resolution:**
- Store large files (images, PDFs, videos) in **GridFS**
- Refactor large embedded arrays using the Outlier or Bucket Pattern
- Archive old data to a separate collection

```python
# GridFS — store and retrieve large files
import gridfs
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
fs = gridfs.GridFS(db)

# Store a file
with open("large_report.pdf", "rb") as f:
    file_id = fs.put(f, filename="large_report.pdf", content_type="application/pdf")

# Retrieve a file
with fs.get(file_id) as f:
    content = f.read()
```

---

### Index Bloat

Too many indexes waste memory and slow down writes (every write must update all indexes).

**Resolution:**

```javascript
// Find unused indexes (MongoDB 4.4+)
db.users.aggregate([{ $indexStats: {} }])
// Look for "accesses.ops": 0 since last restart

// Remove unused indexes
db.users.dropIndex("rarely_used_field_1")

// Guidelines:
// - Max ~5-7 indexes per collection in write-heavy workloads
// - Use compound indexes instead of multiple single-field indexes
// - Use partial/sparse indexes to reduce index size
```

---

### Memory Pressure

WiredTiger cache pressure causes performance degradation.

**Symptoms:** High `wiredTiger.cache.pages read into cache`, slow queries, high IOPS.

**Resolution:**

```javascript
// Check cache usage
db.serverStatus().wiredTiger.cache

// WiredTiger cache = max(1 GB, (RAM - 1 GB) / 2)
// Configure in mongod.conf:
// storage:
//   wiredTiger:
//     engineConfig:
//       cacheSizeGB: 8    # Explicit cache size

// Strategies:
// 1. Add RAM (most effective)
// 2. Reduce working set size (archive old data)
// 3. Add indexes to reduce full collection scans
// 4. Move to a larger instance
```

---

### Real-World Troubleshooting Cases

#### Case 1: Sudden Query Performance Degradation

**Symptoms:** Queries that took <10ms suddenly take 5+ seconds.

**Investigation:**

```javascript
// 1. Check for index changes
db.users.getIndexes()

// 2. Run explain on affected query
db.users.find({ email: "user@example.com" }).explain("executionStats")
// Found: COLLSCAN instead of IXSCAN

// 3. Check for index corruption or recent drops
db.system.profile.find({ millis: { $gt: 1000 } }).sort({ ts: -1 }).limit(10)

// Root cause: A deployment accidentally dropped an index in migration script
// Fix: Recreate the index (with background build in production)
db.users.createIndex({ email: 1 }, { unique: true, background: true })
```

#### Case 2: Replica Set Primary Keeps Stepping Down

**Symptoms:** Application frequently disconnects; primary changes every few minutes.

**Investigation:**

```bash
# Check MongoDB logs
grep "stepping down" /var/log/mongodb/mongod.log

# Common causes:
# - High election timeout due to network issues between members
# - Primary overloaded (high CPU/IO)
# - Clock skew between servers

# Fix:
# 1. Check network latency between replica members
ping mongo2 -c 100 | tail -5

# 2. Check server load
db.serverStatus().opcounters

# 3. Increase election timeout if network is flaky (default 10s)
rs.reconfig({ ...rs.conf(), settings: { electionTimeoutMillis: 20000 } })
```

#### Case 3: Application Gets "Too Many Open Files" Error

**Symptoms:** `MongoNetworkError: connect EMFILE` in application logs.

**Investigation:**

```bash
# Check current open file descriptors
cat /proc/$(pgrep mongod)/limits | grep "Max open files"

# Check current usage
ls /proc/$(pgrep mongod)/fd | wc -l

# Each connection uses 1+ file descriptors
db.serverStatus().connections

# Fix:
# 1. Increase ulimit
ulimit -n 65536

# Add to /etc/security/limits.conf:
# mongodb soft nofile 65536
# mongodb hard nofile 65536

# 2. Reduce connection pool size in application
# 3. Check for connection leaks (connections not being released)
```

---

### Common Errors Reference

| Error | Likely Cause | Resolution |
|---|---|---|
| `Document exceeds maximum size 16793600` | Document > 16 MB | Use GridFS or restructure document |
| `E11000 duplicate key error` | Unique constraint violation | Check data, handle in application |
| `WriteConflict` | Transaction write-write conflict | Retry the transaction |
| `ns not found` | Query on non-existent collection | Check collection name spelling |
| `not primary` | Write sent to secondary | Ensure write is sent to primary |
| `not enough data for query` | Query on uninitialized change stream | Use `startAtOperationTime` |
| `connection refused` | mongod not running / wrong port | `sudo systemctl status mongod` |
| `Authentication failed` | Wrong credentials | Verify username/password/authSource |
| `cursor id not found` | Cursor expired (default: 10 min idle) | Add `noCursorTimeout` or batch faster |

---

## 11. Best Practices & Cheatsheet

> Quick-reference best practices and common MongoDB operations.

### Data Modeling Best Practices

- Model data based on **access patterns**, not data relationships
- Embed when data is always read/written together
- Reference when data is independently accessed or arrays are unbounded
- Avoid deeply nested documents (hard to query and index)
- Use meaningful, short field names (saved in every document)
- Always include `created_at` and `updated_at` timestamps

### Indexing Best Practices

- Index all fields used in `find()`, `sort()`, and `aggregate()` `$match` stages
- Follow the **ESR rule** for compound indexes
- Use `explain("executionStats")` to verify indexes are used
- Remove unused indexes
- Avoid over-indexing write-heavy collections
- Use partial indexes to reduce index size

### Query Best Practices

- Always use projection to limit returned fields
- Avoid `$where` (evaluates JavaScript; slow and insecure)
- Use `$elemMatch` for array element matching
- Paginate with `_id`-based range queries instead of `skip()` for large offsets
- Set `maxTimeMS` to prevent runaway queries

```javascript
// ID-based pagination (efficient)
db.orders.find({ _id: { $gt: lastSeenId } }).sort({ _id: 1 }).limit(20)

// Skip-based pagination (avoid for large offsets)
db.orders.find().skip(10000).limit(20)  // BAD: scans 10,020 docs
```

### Quick Cheatsheet

```javascript
// ---- CONNECTION ----
mongosh "mongodb://user:pass@host:27017/db?authSource=admin"

// ---- CRUD ----
db.col.insertOne({})              // Insert
db.col.find({}).limit(10)         // Find
db.col.updateOne({}, {$set: {}})  // Update
db.col.deleteOne({})              // Delete

// ---- QUERY OPERATORS ----
// Comparison: $eq $ne $gt $gte $lt $lte $in $nin
// Logical:    $and $or $nor $not
// Element:    $exists $type
// Array:      $all $elemMatch $size
// Evaluation: $regex $text $where

// ---- UPDATE OPERATORS ----
// Field:   $set $unset $rename $inc $mul $min $max $setOnInsert
// Array:   $push $pop $pull $addToSet $pullAll $each $position $slice $sort

// ---- AGGREGATION QUICK ----
db.col.aggregate([
  { $match: { status: "active" } },
  { $group: { _id: "$category", total: { $sum: "$amount" }, count: { $sum: 1 } } },
  { $sort: { total: -1 } },
  { $limit: 10 }
])

// ---- INDEXES ----
db.col.createIndex({ field: 1 })
db.col.createIndex({ a: 1, b: -1 }, { unique: true })
db.col.getIndexes()
db.col.dropIndex("field_1")

// ---- ADMIN ----
db.stats()
db.col.stats()
db.serverStatus()
db.currentOp()
rs.status()
sh.status()
```

---

## 12. Appendix

### Sample Datasets

```javascript
// E-commerce dataset (mongosh)
db.products.insertMany([
  { sku: "P001", name: "Laptop Pro", category: "electronics", price: 1299.99, stock: 50, rating: 4.5 },
  { sku: "P002", name: "Wireless Mouse", category: "electronics", price: 29.99, stock: 200, rating: 4.2 },
  { sku: "P003", name: "Standing Desk", category: "furniture", price: 499.00, stock: 30, rating: 4.7 },
  { sku: "P004", name: "Coffee Maker", category: "appliances", price: 89.99, stock: 75, rating: 4.0 }
])

db.orders.insertMany([
  {
    order_id: "ORD-001",
    user_id: ObjectId("64f1a2b3c4d5e6f7a8b9c0d1"),
    items: [
      { sku: "P001", qty: 1, price: 1299.99 },
      { sku: "P002", qty: 2, price: 29.99 }
    ],
    total: 1359.97,
    status: "completed",
    created_at: ISODate("2024-03-15T10:30:00Z")
  },
  {
    order_id: "ORD-002",
    user_id: ObjectId("64f1a2b3c4d5e6f7a8b9c0d2"),
    items: [{ sku: "P003", qty: 1, price: 499.00 }],
    total: 499.00,
    status: "pending",
    created_at: ISODate("2024-03-16T14:20:00Z")
  }
])
```

---

### Exercises

1. **Beginner:** Create a `library` database with a `books` collection. Insert 10 books with fields: `title`, `author`, `genre`, `year`, `available`. Query all available books sorted by year descending.

2. **Intermediate:** Build an aggregation pipeline on the `orders` sample dataset to find the top 3 best-selling SKUs by total quantity ordered.

3. **Advanced:** Implement a Python script using PyMongo transactions to transfer "inventory" units between two product documents atomically. Ensure it handles `WriteConflict` errors with retry logic (up to 3 retries with exponential backoff).

4. **Performance:** Insert 1 million documents into a collection. Measure query time without an index vs with an index using `explain("executionStats")`. Document the difference.

5. **Modeling:** Design a data model for a social media platform (users, posts, comments, likes, followers). Justify each embedding/referencing decision based on access patterns.

---

### References

- **Official Documentation:** https://www.mongodb.com/docs/
- **MongoDB University (free courses):** https://learn.mongodb.com/
- **PyMongo Documentation:** https://pymongo.readthedocs.io/
- **Motor (Async) Documentation:** https://motor.readthedocs.io/
- **MongoDB Blog:** https://www.mongodb.com/blog/
- **MongoDB Specification (BSON):** https://bsonspec.org/
- **MongoDB Design Patterns:** https://www.mongodb.com/blog/post/building-with-patterns-a-summary
- **WiredTiger Storage Engine:** https://source.wiredtiger.com/
- **The Little MongoDB Book (free):** https://github.com/karlseguin/the-little-mongodb-book
- **MongoDB Performance Best Practices:** https://www.mongodb.com/docs/manual/administration/analyzing-mongodb-performance/
