# Lab 1: Introduction to IAM

*AWS Technical Essentials*

> Wherever you see `<ID>`, substitute the student ID your instructor assigned you (for example `user7`).

---

## 🔐 Lab 1: Introduction to AWS IAM

*AWS Technical Essentials — Identity and Access Management*

**Instructor notes:** Welcome students to Lab 1. Ensure all students have their lab credentials ready before starting.

---

## 🏷️ Your Student ID — Read This First

> **⚠️ Everyone in this class shares one AWS account.** Every resource you create must carry your assigned student ID, or it will collide with someone else's.

Your instructor has assigned you an ID such as `user7`. In every lab, wherever you see `<ID>`, type your own ID instead.

| The lab shows | You type (if your ID is `user7`) |
| --- | --- |
| `lab-user-<ID>` | `lab-user-user7` |
| `employee-directory-app-sg-<ID>` | `employee-directory-app-sg-user7` |

> **💡 Two exceptions:** the IAM role `EmployeeDirectoryAppRole` is pre-created by your instructor and shared — use it as-is, do not rename it. S3 bucket names must be unique across *all* of AWS, so Lab 4 adds a random suffix on top of your ID.

**Instructor notes:** Hand out student IDs before starting. Keep them short (user1 through userN) — load balancer and target group names are capped at 32 characters in Lab 6. Tell students to write their ID on a sticky note; they will use it in every lab. Emphasise that if they skip the suffix, the console will either throw a duplicate-name error or, worse, hand them someone else's resource.

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

### ✅ Prerequisites

- AWS lab account credentials
- Web browser (Chrome or Firefox)

**Instructor notes:** Review objectives. IAM is foundational — every other lab builds on these concepts. Ensure all students have console access before proceeding.

---

## 📈 Explore the IAM Dashboard

1. In the console search bar, type **IAM** and select it
2. Note the **IAM sign-in URL** — copy it for later
3. Review the resource summary: Users, Groups, Roles, Policies

> **💡 Note:** IAM is a **global service** — not tied to any specific AWS Region.

> **✅ Expected:** You see the IAM Dashboard with resource counts and the account sign-in URL.

**Instructor notes:** Have students copy the IAM sign-in URL to a notepad — they will need it when testing permissions later. Point out that IAM is global (common exam topic). Give students about 1 minute to explore.

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

**Instructor notes:** Walk through this step carefully. Make sure students select "I want to create an IAM user" (not Identity Center). The password must be saved now — it cannot be viewed again after closing the page. If missed, it can be reset from the Security credentials tab.

---

## 👥 Create an IAM Group

1. Click **User groups** in the left nav, then **Create group**
2. Group name: `EC2-Admins-<ID>`
3. Under **Add users**, check **`lab-user-<ID>`**
4. Under **Attach permissions policies**, search and select **AmazonEC2FullAccess**
5. Click **Create user group**

> **✅ Expected:** `EC2-Admins-<ID>` group created with `lab-user-<ID>` as a member and AmazonEC2FullAccess attached.

**Instructor notes:** Explain that `lab-user-<ID>` now has permissions from two sources: S3 read-only (direct) and EC2 full access (via group). IAM evaluates the union of all attached policies.

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

**Instructor notes:** Walk through the JSON: Version is always 2012-10-17, Effect Allow, two Actions for list and get, two Resource ARNs because ListBucket operates on the bucket and GetObject operates on objects. The wildcard pattern scopes access to that student's own bucket only — their ID sits inside the ARN, so the policy cannot read a classmate's bucket. Remind them to substitute their ID in both Resource lines.

---

## 🔎 Test Permissions — Sign In as `lab-user-<ID>`

1. Open an **incognito/private browser window**
2. Navigate to the **IAM sign-in URL** you saved earlier
3. Sign in as **`lab-user-<ID>`** with the password you set

> **✅ Expected:** You sign in successfully. Confirm the user name in the top-right corner shows **`lab-user-<ID>`**.

**Instructor notes:** Use incognito to avoid session conflicts. If sign-in fails, verify the IAM sign-in URL (not root account URL). If the password was forgotten, return to admin session and reset it from the user's Security credentials tab.

---

## 🔎 Test Permissions — Verify Access

1. Navigate to **S3** — you should be able to **view** buckets
2. Try to **create a bucket** — you should get **Access Denied**
3. Navigate to **EC2** — you should have **full access** (via group)

> **❌ S3 write = denied:** `lab-user-<ID>` has read-only S3 access (direct policy).

> **✅ EC2 = full access:** `lab-user-<ID>` inherits EC2FullAccess from the `EC2-Admins-<ID>` group.

**Instructor notes:** This clearly demonstrates how IAM policies control access from multiple sources. Ask students to try accessing another service like RDS — they should see access denied (default deny). Close the incognito window when done and return to the admin session.

---

## 🗑 Clean Up

Return to your **admin session** and delete the following (in order):

1. **Policy:** Policies → search `S3ScopedReadPolicy-<ID>` → Delete
2. **Remove user from group:** User groups → `EC2-Admins-<ID>` → remove `lab-user-<ID>`
3. **Group:** User groups → delete `EC2-Admins-<ID>`
4. **User:** Users → delete `lab-user-<ID>`

> **✅ Verify:** `lab-user-<ID>`, `EC2-Admins-<ID>`, and `S3ScopedReadPolicy-<ID>` are all removed.

**Instructor notes:** Order matters: delete the policy first, remove the user from the group, then delete the group, then the user. Give students a moment to verify cleanup is complete.

---

## 🎉 Lab 1 Complete!

*Introduction to AWS IAM*

**Instructor notes:** Congratulate students. Briefly recap key takeaways before transitioning to the next module.

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

**Instructor notes:** Review key takeaways. The next module covers compute services (EC2), building on the IAM concepts learned here.

---

## ❓ Questions?

*Ask your instructor before proceeding to the next module*

**Instructor notes:** Common questions: What happens when Deny and Allow conflict? (Explicit Deny always wins.) Can a user belong to multiple groups? (Yes, permissions are the union.) What about Roles vs Users? (Roles use temporary credentials — preferred for services.)

---
