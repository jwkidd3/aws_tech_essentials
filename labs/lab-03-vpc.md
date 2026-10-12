# Lab 3: Create a VPC

*AWS Technical Essentials*

> Wherever you see `<ID>`, substitute the student ID your instructor assigned you (for example `user7`).

---

## 🌐 Lab 3

*Create a Custom VPC and Deploy EC2 — AWS Technical Essentials • Lab 3 of 6*

---

## 🏷️ Resource Names for This Lab

Replace `<ID>` with your assigned student ID (for example `user7`).

| Resource | Name |
| --- | --- |
| VPC wizard — name tag auto-generation | `employee-directory-<ID>` |
| Resulting VPC | `employee-directory-<ID>-vpc` |
| Security group (new, in your VPC) | `employee-directory-vpc-sg-<ID>` |
| EC2 instance (Name tag) | `employee-directory-app-vpc-<ID>` |

> **💡 Nice side effect:** the wizard applies your name tag to every resource it creates — subnets, route tables and the internet gateway all pick up your ID automatically.

---

## 📋 Lab Overview

### 🎯 Objectives

- Create a VPC with public subnets using the wizard
- Create a security group in the new VPC
- Launch an EC2 instance in the custom VPC
- Verify the web application works

### 📝 Lab Details

- **Duration:** ~25 minutes
- **Region:** `us-east-1` (N. Virginia) — same for every lab
- **Prerequisite:** Lab 2 instance running

> **⚠️** Keep this VPC — it is needed for Lab 6.

---

## 🔧 Create VPC — Settings

1. Navigate to **VPC** in the console
2. Click **Create VPC**
3. Select **"VPC and more"**

| Setting | Value |
| --- | --- |
| Name tag auto-generation | `employee-directory-<ID>` |
| IPv4 CIDR block | `10.1.0.0/16` |
| Number of Availability Zones | **2** |
| Number of public subnets | **2** |
| Number of private subnets | **0** |
| NAT gateways | **None** |

---

## 🔧 Create VPC — Execute

1. Review the **Preview** panel on the right
2. Click **Create VPC**
3. Wait for all resources to show **green checkmarks**
4. Click **View VPC**

> **✅ Expected:** VPC created with 2 public subnets, an internet gateway, and route tables — all auto-configured.

---

## 🔒 Create Security Group

1. In the VPC console left nav, click **Security groups**
2. Click **Create security group**
3. Name: `employee-directory-vpc-sg-<ID>` — a *new* group, not the Lab 2 one
4. Description: *Allow HTTP access for Employee Directory*
5. VPC: Select **`employee-directory-<ID>-vpc`**

| Type | Port | Source |
| --- | --- | --- |
| HTTP | 80 | 0.0.0.0/0 |
| SSH | 22 | My IP |

6. Click **Create security group**

---

## 🚀 Launch EC2 in the New VPC

1. Navigate to **EC2** → **Launch instance**
2. Name: `employee-directory-app-vpc-<ID>`
3. AMI: **Amazon Linux 2023**
4. Instance type: **t2.micro**
5. Key pair: **`employee-dir-key-<ID>`** (from Lab 2)
6. Under **Network settings**, click **Edit**:
    - VPC: **`employee-directory-<ID>-vpc`**
    - Subnet: Choose any **public** subnet
    - Auto-assign public IP: **Enable**
    - Select existing security group: **`employee-directory-vpc-sg-<ID>`**

---

## 🚀 Add User Data and Launch

1. Under **Advanced details**, scroll to **User data** and paste:

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

3. Click **Launch instance**

---

## 🌐 Test the Web Server

1. Wait for the new instance to reach **Running** with **2/2 checks passed**
2. Copy the **Public IPv4 address**
3. Open a browser tab: `http://<PUBLIC_IP>`

> **✅ Expected:** The Employee Directory page loads — now running inside your custom VPC.

> **⏲ Note:** Allow 1-2 minutes after "Running" for Apache to finish installing.

---

## 🛑 Stop the Lab 2 Instance

1. In the EC2 console, find your original **`employee-directory-app-<ID>`** instance (from Lab 2)
2. Select it, click **Instance state** → **Stop instance**

> **💡 Why?** The Lab 2 instance was in the default VPC. Now that you have a working instance in your custom VPC, you no longer need the old one running. Stopping saves cost.

---

## ⚠️ Resources to Keep

> **Do NOT delete these resources** — they are needed for Lab 6:

- **VPC:** `employee-directory-<ID>-vpc` (with subnets, IGW, route tables)
- **Security Group:** `employee-directory-vpc-sg-<ID>`
- **Key Pair:** `employee-dir-key-<ID>`

You may terminate the EC2 instance from this lab — Lab 6 will create new instances via Auto Scaling.

---

## 🎉 Lab 3 Complete!

*Custom VPC with EC2 Deployed*

---

## 🎯 Key Takeaways

### 🛠️ What You Did

- Created a VPC with the "VPC and more" wizard
- Configured 2 public subnets across 2 AZs
- Created a security group in the new VPC
- Launched and tested an EC2 instance

### 📚 Key Concepts

- **VPC** = isolated network in the cloud
- **Public subnets** have routes to an IGW
- **Multi-AZ** enables high availability
- **Security groups** are VPC-specific

---

## ❓ Questions?

*Ask your instructor before proceeding to the next module*

---
