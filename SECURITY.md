# Coastal Alpine Tech - 'Weaver' SecOps Protocol

This document outlines the security perimeter setup and SecOps protocols configured for the **Weaver** repository.

---

## 1. Local Edge Environment Security (`.gitignore`)
The `.gitignore` has been updated to prevent key edge/development secrets and runtime artifacts from being committed:
* **Exclusions:**
  * Local configuration override templates (`.env.*`)
  * Local private/public certificates (`*.pem`, `*.key`, `*.crt`)
  * Edge secrets directory (`secrets/`)
  * Local baseline mapping configuration (`.secrets.baseline`)
  * Logs and debug directories (`*.log`)

---

## 2. Secure Configuration Template (`.env.example`)
Environment templates are set up to capture all required edge keys safely without leaking credentials. 
* **Key configurations declared:**
  ```bash
  MQTT_BROKER_URL=ssl://your-broker-ip:8883
  MQTT_USER=weaver_edge_node
  MQTT_PASSWORD=insert_secure_password
  MAGICBAG_API_KEY=insert_key_here
  ```

---

## 3. GitHub Actions Pipelines
Automated vulnerability scans are scheduled on the main repository via:
* **Dependabot (`.github/dependabot.yml`):** Auto-evaluates Python pip packages weekly and creates patches for vulnerable dependencies.
* **Bandit SAST Scan (`.github/workflows/secops.yml`):** Performs static code analysis (SAST) on push/PR events to main.

---

## 4. Local Hook Validation (`pre-commit`)
A local pre-commit hook is registered in the Git database `.git/hooks/pre-commit` to intercept commits containing plaintext secrets.
* **Service Provider:** Yelp's `detect-secrets` hook.
* **Execution:** Intercepts files and validates their signatures against `.secrets.baseline` prior to staging changes.
