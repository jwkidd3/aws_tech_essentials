# Lab 1: Introduction to IAM

*AWS Technical Essentials*

> Wherever you see `<ID>`, substitute the student ID your instructor assigned you (for example `user7`).

---

## 🔐 Lab 1: Introduction to AWS IAM

*AWS Technical Essentials — Identity and Access Management*

---

## 🏷️ Your Student ID — Read This First

> **⚠️ Everyone in this class shares one AWS account.** Every resource you create must carry your assigned student ID, or it will collide with someone else's.

Your instructor has assigned you an ID such as `user7`. In every lab, wherever you see `<ID>`, type your own ID instead.

| The lab shows | You type (if your ID is `user7`) |
| --- | --- |
| `lab-user-<ID>` | `lab-user-user7` |
| `employee-directory-app-sg-<ID>` | `employee-directory-app-sg-user7` |

> **💡 One exception:** S3 bucket names must be unique across *all* of AWS, so Lab 4 adds a random suffix on top of your ID.

> **⚠️ One Region for the whole course:** set the Region picker (top right of the console) to **US East (N. Virginia) `us-east-1`** and do not change it. Every lab after this one builds on resources from the previous labs, and they are invisible from any other Region.

---

## 📋 Lab Overview

### 🎯 Objectives

- Navigate the IAM Dashboard
- Create an IAM User with console access
- Create an IAM Group with a managed policy
- Author a custom scoped IAM Policy
- Test permissions as the new user

### 📝 Lab Details

- **Duration:** ~15 minutes
- **Level:** Introductory
- **Services:** IAM, S3, EC2
- **Region:** `us-east-1` (N. Virginia) — stay in it all day

### ✅ Prerequisites

- AWS lab account credentials
- Web browser (Chrome or Firefox)

---

## 📈 Explore the IAM Dashboard

1. In the console search bar, type **IAM** and select it
2. Note the **IAM sign-in URL** — copy it for later
3. Review the resource summary: Users, Groups, Roles, Policies

> **💡 Note:** IAM is a **global service** — not tied to any specific AWS Region.

> **✅ Expected:** You see the IAM Dashboard with resource counts and the account sign-in URL.

---

## 📝 Create an IAM User

1. Click **Users** in the left nav, then **Create user**
2. User name: `lab-user-<ID>`
3. Check **Provide user access to the AWS Management Console**
4. Select **I want to create an IAM user**
5. Set a custom password (e.g., `Lab@User123!`), uncheck "require password reset"
6. Click **Next**
7. Select **Attach policies directly**, search `S3ReadOnly`, check **AmazonS3ReadOnlyAccess**
8. Click **Next**, then **Create user**

> **✅ Expected:** Success banner. Save the sign-in URL and password — you will need them later.

---

## 👥 Create an IAM Group

1. Click **User groups** in the left nav, then **Create group**
2. Group name: `EC2-Admins-<ID>`
3. Under **Add users**, check **`lab-user-<ID>`**
4. Under **Attach permissions policies**, search and select **AmazonEC2FullAccess**
5. Click **Create user group**

> **✅ Expected:** `EC2-Admins-<ID>` group created with `lab-user-<ID>` as a member and AmazonEC2FullAccess attached.

---

## 📜 Create a Custom IAM Policy

1. Click **Policies**, then **Create policy**
2. Switch to the **JSON** tab and paste:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::employee-directory-app-bucket-<ID>-*",
                "arn:aws:s3:::employee-directory-app-bucket-<ID>-*/*"
            ]
        }
    ]
}
```

3. Click **Next**, name it `S3ScopedReadPolicy-<ID>`, click **Create policy**

---

## 🔎 Test Permissions — Sign In as `lab-user-<ID>`

1. Open an **incognito/private browser window**
2. Navigate to the **IAM sign-in URL** you saved earlier
3. Sign in as **`lab-user-<ID>`** with the password you set

> **✅ Expected:** You sign in successfully. Confirm the user name in the top-right corner shows **`lab-user-<ID>`**.

---

## 🔎 Test Permissions — Verify Access

1. Navigate to **S3** — you should be able to **view** buckets
2. Try to **create a bucket** — you should get **Access Denied**
3. Navigate to **EC2** — you should have **full access** (via group)

> **❌ S3 write = denied:** `lab-user-<ID>` has read-only S3 access (direct policy).

> **✅ EC2 = full access:** `lab-user-<ID>` inherits EC2FullAccess from the `EC2-Admins-<ID>` group.

---

## 🗑 Clean Up

Return to your **admin session** and delete the following (in order):

1. **Policy:** Policies → search `S3ScopedReadPolicy-<ID>` → Delete
2. **Remove user from group:** User groups → `EC2-Admins-<ID>` → remove `lab-user-<ID>`
3. **Group:** User groups → delete `EC2-Admins-<ID>`
4. **User:** Users → delete `lab-user-<ID>`

> **✅ Verify:** `lab-user-<ID>`, `EC2-Admins-<ID>`, and `S3ScopedReadPolicy-<ID>` are all removed.

---

## 🎉 Lab 1 Complete!

*Introduction to AWS IAM*

---

## 🎯 Key Takeaways

### 🛠️ What You Did

- Navigated the IAM Dashboard
- Created an IAM User with console access
- Created a Group with a managed policy
- Authored a custom JSON policy
- Tested permissions across services

### 📚 Key Concepts

- **IAM is global** — not Region-specific
- **Least privilege** — grant only needed permissions
- **Groups** — manage permissions at scale
- **Default deny** — everything denied unless allowed

---

## ❓ Questions?

*Ask your instructor before proceeding to the next module*

---
