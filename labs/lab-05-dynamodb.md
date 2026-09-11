# Lab 5: Implement DynamoDB

*AWS Technical Essentials*

> Wherever you see `<ID>`, substitute the student ID your instructor assigned you (for example `user7`).

---

## 📚 Lab 5

*Implement Amazon DynamoDB — AWS Technical Essentials • ~15 Minutes*

---

## 🏷️ Resource Names for This Lab

Replace `<ID>` with your assigned student ID (for example `user7`).

| Resource | Name |
| --- | --- |
| DynamoDB table | `Employees-<ID>` |

> **💡 Note:** table names are unique per Region per account, so every student needs their own. Item keys (`E001`, `E002`, `E003`) live inside your table and do not need a suffix.

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

---

## 🔄 Edit an Item — Schema Flexibility

1. Click on item **E003** (Bob Johnson)
2. Click **Add new attribute** → **String**
3. Add: `phone` = `512-555-0199`
4. Click **Save changes**
5. Run a **Scan** again — notice E003 has a `phone` attribute that other items do not have

> **✅ Expected:** E003 now has 5 attributes while E001 and E002 still have 4. Each item can have different attributes.

---

## 🗑 Clean Up

1. Go to **DynamoDB** → **Tables**
2. Select the **`Employees-<ID>`** table
3. Click **Delete**
4. Type `confirm` and click **Delete table**

> **✅ Expected:** The `Employees-<ID>` table is deleted. DynamoDB deletes all items and indexes with the table.

---

## 🎉 Lab 5 Complete!

*DynamoDB Table Created and Queried*

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

---

## ❓ Questions?

*Ask your instructor before proceeding to the next module*

---
