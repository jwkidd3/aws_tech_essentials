# Lab 2: Launch Employee Directory on EC2

*AWS Technical Essentials*

> Wherever you see `<ID>`, substitute the student ID your instructor assigned you (for example `user7`).

---

## 💻 Lab 2

*Launch the Employee Directory Application on Amazon EC2 — AWS Technical Essentials • Lab 2 of 6*

---

## 🏷️ Resource Names for This Lab

Replace `<ID>` with your assigned student ID (for example `user7`).

| Resource | Name |
| --- | --- |
| EC2 instance (Name tag) | `employee-directory-app-<ID>` |
| Key pair | `employee-dir-key-<ID>` |
| Security group | `employee-directory-app-sg-<ID>` |

> **⚠️ Shared account:** the console lists every student's instances, key pairs and security groups together. Filter or sort by your ID so you only touch your own.

---

## 📋 Lab Overview

### 🎯 Objectives

- Launch an EC2 instance with Amazon Linux 2023
- Configure a security group for HTTP access
- Bootstrap Apache with a user data script
- Verify the web application in a browser
- Observe public IP behavior on stop/start

### 📝 Lab Details

- **Duration:** ~25 minutes
- **Region:** `us-east-1` (N. Virginia) — same for every lab
- **Instance type:** t2.micro (Free Tier)

> **⚠️ Important:** Do NOT terminate this instance — it will be used in later labs.

---

## 🚀 Launch an Instance

1. Navigate to **EC2**, click **Launch instance**
2. Name: `employee-directory-app-<ID>`
3. AMI: **Amazon Linux 2023** (default)
4. Instance type: **t2.micro**
5. Key pair: **Create new key pair** named `employee-dir-key-<ID>`, download the.pem file

> **💡 Tip:** Save the key pair file — you cannot download it again.

---

## 🔒 Configure Security Group

Under **Network settings**, click **Edit**:

1. Security group name: `employee-directory-app-sg-<ID>`
2. Description: *Allow HTTP access*

| Type | Port | Source |
| --- | --- | --- |
| SSH | 22 | My IP |
| HTTP | 80 | 0.0.0.0/0 |

---

## 📜 Add User Data Script

In **Advanced details**, scroll to **User data** and paste:

```bash
#!/bin/bash
dnf install -y httpd
systemctl enable --now httpd
echo '<!DOCTYPE html>
<html><head><title>Employee Directory</title>
<style>body{font-family:Arial,sans-serif;max-width:800px;margin:50px auto;padding:20px}
h1{color:#1a365d}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ddd;padding:12px;text-align:left}
th{background:#2b6cb0;color:white}tr:nth-child(even){background:#f7fafc}</style></head>
<body><h1>Employee Directory</h1>
<p>Welcome to the Employee Directory Application</p>
<table><tr><th>Name</th><th>Department</th><th>Location</th></tr>
<tr><td>John Smith</td><td>Engineering</td><td>Seattle</td></tr>
<tr><td>Jane Doe</td><td>Marketing</td><td>New York</td></tr>
<tr><td>Bob Johnson</td><td>Sales</td><td>Austin</td></tr></table>
</body></html>' > /var/www/html/index.html
```

---

## 🚀 Launch and Wait

1. Click **Launch instance**
2. Click the **instance ID** link in the success message
3. Wait for **Instance state** to show **Running**
4. Wait for **Status checks** to show **2/2 checks passed**

> **⏲ Note:** The user data script takes 1-2 minutes after "Running" to finish installing Apache.

---

## 🌐 Test — Browse to Public IP

1. Select your instance and copy the **Public IPv4 address**
2. Open a new browser tab: `http://<PUBLIC_IP>`

> **✅ Expected:** The Employee Directory page displays with the employee table.

> **Not loading?** Verify: (1) using `http://` not `https://`, (2) security group allows port 80, (3) public IP is correct.

---

## 🔍 Explore Instance Details

With your instance selected, review these tabs:

### Details Tab

- Instance ID
- Public / Private IP
- AMI ID, Instance type
- Availability Zone

### Security Tab

- Security group rules
- Inbound / Outbound rules

---

## 🔄 Stop and Start — Note IP Change

1. Select your instance, click **Instance state** → **Stop instance**
2. Wait for state to show **Stopped**
3. Note the **Public IPv4 address** is now blank
4. Click **Instance state** → **Start instance**
5. Once running, note the **new Public IP**
6. Browse to the new IP — the app should load

> **✅ Expected:** The app loads at the new IP. Apache starts automatically because we used `systemctl enable`.

---

## ⚠️ Keep This Instance Running

> **Do NOT terminate this instance.** It will be used as a reference in Lab 3 (VPC). You will launch a new instance in a custom VPC and compare it to this one.

Make sure your instance is in the **Running** state before proceeding.

---

## 🎉 Lab 2 Complete!

*Employee Directory Running on EC2*

---

## 🎯 Key Takeaways

### 🛠️ What You Did

- Launched an EC2 instance with Amazon Linux 2023
- Configured a security group
- Bootstrapped Apache via user data
- Observed public IP change on stop/start

### 📚 Key Concepts

- **User data** runs once at first boot
- **Security groups** are stateful firewalls
- **Public IPs** change on stop/start
- **systemctl enable** persists across reboots

---

## ❓ Questions?

*Ask your instructor before proceeding to the next module*

---
