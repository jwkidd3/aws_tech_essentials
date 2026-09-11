# Lab 2: Launch Employee Directory on EC2

*AWS Technical Essentials*

> Wherever you see `<ID>`, substitute the student ID your instructor assigned you (for example `user7`).

---

## 💻 Lab 2

*Launch the Employee Directory Application on Amazon EC2 — AWS Technical Essentials • Lab 2 of 6*

**Instructor notes:** Welcome to Lab 2. Students will launch an EC2 instance running Apache with the Employee Directory web page. This instance will be used in later labs.

---

## 🏷️ Resource Names for This Lab

Replace `<ID>` with your assigned student ID (for example `user7`).

| Resource | Name |
| --- | --- |
| EC2 instance (Name tag) | `employee-directory-app-<ID>` |
| Key pair | `employee-dir-key-<ID>` |
| Security group | `employee-directory-app-sg-<ID>` |
| IAM instance profile | `EmployeeDirectoryAppRole` — shared, do not rename |

> **⚠️ Shared account:** the console lists every student's instances, key pairs and security groups together. Filter or sort by your ID so you only touch your own.

**Instructor notes:** Remind students of their ID before they start the launch wizard. The key pair and security group created here are reused in Labs 3 and 6, so the suffix has to be right the first time. Show them the EC2 console search bar — typing their ID filters the instance list to just theirs.

---

## 📋 Lab Overview

### 🎯 Objectives

- Launch an EC2 instance with Amazon Linux 2023
- Configure a security group for HTTP access
- Bootstrap Apache with a user data script
- Verify the web application in a browser
- Observe public IP behavior on stop/start

### 📝 Lab Details

- **Duration:** ~20 minutes
- **Region:** As assigned by instructor
- **Instance type:** t2.micro (Free Tier)

> **⚠️ Important:** Do NOT terminate this instance — it will be used in later labs.

**Instructor notes:** Review objectives. Emphasize this instance persists across multiple labs. Make sure everyone knows their region.

---

## 🚀 Launch an Instance

1. Navigate to **EC2**, click **Launch instance**
2. Name: `employee-directory-app-<ID>`
3. AMI: **Amazon Linux 2023** (default)
4. Instance type: **t2.micro**
5. Key pair: **Create new key pair** named `employee-dir-key-<ID>`, download the.pem file

> **💡 Tip:** Save the key pair file — you cannot download it again.

**Instructor notes:** Walk through the launch wizard. Amazon Linux 2023 is the default AMI. t2.micro is Free Tier eligible. The key pair is needed for SSH but we will primarily use Session Manager via the IAM role.

---

## 🔒 Configure Security Group

Under **Network settings**, click **Edit**:

1. Security group name: `employee-directory-app-sg-<ID>`
2. Description: *Allow HTTP access*

| Type | Port | Source |
| --- | --- | --- |
| SSH | 22 | My IP |
| HTTP | 80 | 0.0.0.0/0 |

Under **Advanced details**, set **IAM instance profile** to `EmployeeDirectoryAppRole` (if available).

**Instructor notes:** HTTP from anywhere allows browser access to the web app. SSH from My IP restricts remote access. The IAM role provides SSM Session Manager access as an alternative to SSH.

---

## 📜 Add User Data Script

In **Advanced details**, scroll to **User data** and paste:

```bash
#!/bin/bash -ex
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
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

**Instructor notes:** This script installs Apache httpd, starts and enables the service, then writes a static Employee Directory HTML page. No placeholders needed — works as-is. User data runs only once at first boot.

---

## 🚀 Launch and Wait

1. Click **Launch instance**
2. Click the **instance ID** link in the success message
3. Wait for **Instance state** to show **Running**
4. Wait for **Status checks** to show **2/2 checks passed**

> **⏲ Note:** The user data script takes 1-2 minutes after "Running" to finish installing Apache.

**Instructor notes:** Status checks confirm the instance is reachable and the OS is healthy. The user data script runs during this time. If the web page does not load after several minutes, check: security group allows port 80, using http:// not https://, correct public IP.

---

## 🌐 Test — Browse to Public IP

1. Select your instance and copy the **Public IPv4 address**
2. Open a new browser tab: `http://<PUBLIC_IP>`

> **✅ Expected:** The Employee Directory page displays with the employee table.

> **Not loading?** Verify: (1) using `http://` not `https://`, (2) security group allows port 80, (3) public IP is correct.

**Instructor notes:** If the page still does not load, have students check the system log: Actions > Monitor and troubleshoot > Get system log. Look for httpd errors. You can also use Session Manager to run 'systemctl status httpd'.

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
- IAM Role attached
- Inbound / Outbound rules

**Instructor notes:** Give students 1-2 minutes to browse the tabs. Point out the Monitoring tab with basic CloudWatch metrics. The Networking tab shows the VPC and subnet. No need to go deep here — just awareness.

---

## 🔄 Stop and Start — Note IP Change

1. Select your instance, click **Instance state** → **Stop instance**
2. Wait for state to show **Stopped**
3. Note the **Public IPv4 address** is now blank
4. Click **Instance state** → **Start instance**
5. Once running, note the **new Public IP**
6. Browse to the new IP — the app should load

> **✅ Expected:** The app loads at the new IP. Apache starts automatically because we used `systemctl enable`.

**Instructor notes:** This demonstrates dynamic public IPs. To keep a fixed IP, use an Elastic IP or place a load balancer in front (which students will do in Lab 6). Apache restarts automatically without re-running user data.

---

## ⚠️ Keep This Instance Running

> **Do NOT terminate this instance.** It will be used as a reference in Lab 3 (VPC). You will launch a new instance in a custom VPC and compare it to this one.

Make sure your instance is in the **Running** state before proceeding.

**Instructor notes:** Verify all students have a running instance with a working Employee Directory page before moving on. They will stop this instance in Lab 3 after launching a new one in the custom VPC.

---

## 🎉 Lab 2 Complete!

*Employee Directory Running on EC2*

**Instructor notes:** Congratulate students. Recap: launched an instance, bootstrapped Apache with user data, tested the app, observed IP behavior.

---

## 🎯 Key Takeaways

### 🛠️ What You Did

- Launched an EC2 instance with Amazon Linux 2023
- Configured security group and IAM role
- Bootstrapped Apache via user data
- Observed public IP change on stop/start

### 📚 Key Concepts

- **User data** runs once at first boot
- **Security groups** are stateful firewalls
- **Public IPs** change on stop/start
- **systemctl enable** persists across reboots

**Instructor notes:** Review key takeaways. Next module covers VPC networking, where students will build a custom VPC and launch a new instance inside it.

---

## ❓ Questions?

*Ask your instructor before proceeding to the next module*

**Instructor notes:** Common questions: How do I get a static IP? (Elastic IP or load balancer.) What if user data fails? (Check system log.) Can I change instance type later? (Yes — stop, change type, start.)

---
