# Lab 5: Implement DynamoDB

*AWS Technical Essentials*

> Wherever you see `<ID>`, substitute the student ID your instructor assigned you (for example `user7`).

---

## 📚 Lab 5

*Implement Amazon DynamoDB — AWS Technical Essentials • ~15 Minutes*

**Instructor notes:** Lab 5 of 6. Students will create a DynamoDB table, add items, query data, and observe schema flexibility.

---

## 🏷️ Resource Names for This Lab

Replace `<ID>` with your assigned student ID (for example `user7`).

| Resource | Name |
| --- | --- |
| DynamoDB table | `Employees-<ID>` |

> **💡 Note:** table names are unique per Region per account, so every student needs their own. Item keys (`E001`, `E002`, `E003`) live inside your table and do not need a suffix.

**Instructor notes:** Only the table name needs the ID — the items inside it are scoped to the table. The Tables list will show one row per student; point out that they should only ever select the table ending in their own ID, especially at clean-up time.

---

## 🎯 Lab Overview

### 📋 Objectives

- Create a DynamoDB table with a partition key
- Add items with different attributes
- Scan and query the table
- Edit an item to demonstrate schema flexibility

### 📝 Lab Details

- **Duration:** ~15 minutes
- **Capacity mode:** On-demand
- **Region:** Same as previous labs

**Instructor notes:** Review objectives. DynamoDB is a fully managed NoSQL database. This lab focuses on core CRUD operations and the schema-flexible nature of the service. Ensure everyone has console access.

---

## 📊 Create the `Employees-<ID>` Table

1. Navigate to **DynamoDB** in the console
2. Click **Create table**
3. Table name: `Employees-<ID>`
4. Partition key: `id` (String)
5. Table settings: **Customize settings**
6. Capacity mode: **On-demand**
7. Leave all other settings as default
8. Click **Create table**

> **✅ Expected:** Table status changes to **Active** within a few seconds.

**Instructor notes:** On-demand capacity mode is simpler for labs — no need to estimate read/write capacity units. The partition key (id) uniquely identifies each item. DynamoDB does not require you to define other attributes upfront — that is the schema flexibility.

---

## 📝 Add Employee Items

1. Click on the **`Employees-<ID>`** table, then **Explore table items**
2. Click **Create item**

Add these three items (click **Add new attribute** for each extra field):

| id | name | department | location |
| --- | --- | --- | --- |
| E001 | John Smith | Engineering | Seattle |
| E002 | Jane Doe | Marketing | New York |
| E003 | Bob Johnson | Sales | Austin |

> **💡 Tip:** For each item, click **Add new attribute** → **String** to add name, department, and location fields.

**Instructor notes:** Walk students through creating the first item step by step. For subsequent items they should be able to follow the pattern. Each attribute must be added individually since DynamoDB has no predefined schema beyond the key.

---

## 🔍 Scan and Query the Table

### Scan (returns all items):

1. In **Explore table items**, select **Scan**
2. Click **Run** — all 3 items appear

### Query (search by partition key):

1. Switch to **Query**
2. Partition key value: `E001`
3. Click **Run** — only John Smith's record appears

> **✅ Expected:** Scan returns all 3 items. Query returns only the matching item.

**Instructor notes:** Scans read every item in the table (expensive at scale). Queries use the partition key for efficient lookups. In production, always prefer queries over scans. You can also add filters to narrow results, but filters are applied after the read.

---

## 🔄 Edit an Item — Schema Flexibility

1. Click on item **E003** (Bob Johnson)
2. Click **Add new attribute** → **String**
3. Add: `phone` = `512-555-0199`
4. Click **Save changes**
5. Run a **Scan** again — notice E003 has a `phone` attribute that other items do not have

> **✅ Expected:** E003 now has 5 attributes while E001 and E002 still have 4. Each item can have different attributes.

**Instructor notes:** This is one of the key differences between DynamoDB and relational databases. Items in the same table can have different attributes. Only the partition key (and sort key, if defined) are required. This flexibility is powerful for evolving application schemas.

---

## 🗑 Clean Up

1. Go to **DynamoDB** → **Tables**
2. Select the **`Employees-<ID>`** table
3. Click **Delete**
4. Type `confirm` and click **Delete table**

> **✅ Expected:** The `Employees-<ID>` table is deleted. DynamoDB deletes all items and indexes with the table.

**Instructor notes:** Deleting the table removes all data permanently. In production, you would enable Point-in-Time Recovery or take on-demand backups before deletion. On-demand tables do not incur charges when idle.

---

## 🎉 Lab 5 Complete!

*DynamoDB Table Created and Queried*

**Instructor notes:** Congratulate students. They created a table, added items, queried data, and saw schema flexibility in action.

---

## 🎯 Key Takeaways

### 🛠️ What You Did

- Created a DynamoDB table with a partition key
- Added items with varying attributes
- Used Scan and Query operations
- Demonstrated schema flexibility

### 📚 Key Concepts

- **Partition key** uniquely identifies items
- **Schema-flexible** — items can differ
- **Query** is efficient, **Scan** reads all
- **On-demand** = pay per request

**Instructor notes:** Review key takeaways. The next module covers monitoring and high availability, leading into the capstone Lab 6.

---

## ❓ Questions?

*Ask your instructor before proceeding to the next module*

**Instructor notes:** Common questions: When should I use DynamoDB vs RDS? (DynamoDB for key-value/high scale, RDS for relational/joins.) What is a sort key? (Optional second part of primary key for range queries.) What about Global Secondary Indexes? (Allow querying by non-key attributes — covered in the presentation.)

---
