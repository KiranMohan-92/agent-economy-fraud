# Privacy Preservation Analysis

**Phase:** 03-detection-framework, Plan 03-03
**Created:** 2026-03-22
**Status:** Complete

## Overview

This document analyzes privacy implications of the agent-aware fraud detection framework and provides a compliance roadmap for banking data protection requirements. The analysis covers GDPR, CCPA, GLBA, and AML/KYC regulations, with specific recommendations for each signal.

---

## Executive Summary

**Finding:** The agent-invariant detection framework can be implemented within current privacy regulations with appropriate safeguards. No showstopper compliance issues identified.

**Key Principles:**
1. **Data Minimization:** Store only what's necessary for detection
2. **Purpose Limitation:** Use data only for fraud prevention
3. **Privacy by Design:** Separate PII from behavioral analysis
4. **Transparency:** Clear disclosure to customers

**Compliance Status:**
| Regulation | Compliance Path | Showstopper? |
|------------|-----------------|--------------|
| GDPR | Feasible with safeguards | ✗ No |
| CCPA | Feasible with safeguards | ✗ No |
| GLBA | Feasible within existing framework | ✗ No |
| AML/KYC | Data sharing permitted for fraud prevention | ✗ No |

---

## Part 1: Privacy Impact Assessment

### Signal-by-Signal Data Requirements

| Signal | PII Required | Behavioral Data | Retention Needed | Privacy Risk Level |
|--------|-------------|------------------|------------------|-------------------|
| Economic Rationality | Account ID (pseudonymized) | Amounts, timestamps, categories | 30 days | Medium |
| Network Topology | Account ID (pseudonymized) | Graph structure, degrees | 90 days | Medium |
| Value Flow | Account ID (pseudonymized), chain IDs | Transaction paths, intermediaries | 90 days | High |
| Temporal Consistency | Account ID (pseudonymized) | Timestamps, patterns | 30 days | Low |
| Cross-Platform | Identity hash (no PII), behavioral FP | Cross-platform patterns | 365 days | High |

**Privacy Risk Definitions:**
- **Low:** No PII, patterns not attributable to individuals
- **Medium:** Pseudonymized data, patterns potentially attributable with effort
- **High:** Potential re-identification or cross-platform linkage

### Data Flow Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│                     Transaction Event                            │
│                   (raw data from payment system)                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  PII Separation  │
                    └────────┬────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
    ┌───────────────┐                 ┌───────────────┐
    │  PII Storage  │                 │ Signal Data  │
    │  (encrypted)  │                 │  (pseudonymized)│
    │  - Account ID │                 │  - Hashed IDs │
    │  - Name       │                 │  - Amounts    │
    │  - Documents │                 │  - Timestamps │
    └───────────────┘                 └───────────────┘
            │                                 │
            ▼                                 ▼
    ┌───────────────┐                 ┌───────────────┐
    │  Access Log   │                 │  Detection    │
    │  (audit trail)│                 │  Algorithms   │
    └───────────────┘                 └───────────────┘
```

**Key Principle:** PII and behavioral data are stored separately. Detection algorithms operate on pseudonymized data; PII is accessed only when fraud is confirmed and action is required.

### Regulatory Mapping

#### GDPR (EU General Data Protection Regulation)

| Principle | Requirement | Framework Compliance |
|-----------|-------------|----------------------|
| **Lawfulness** | Art. 6: Legal basis for processing | Fraud prevention = legitimate interest (Art. 6(1)(f)) |
| **Data Minimization** | Art. 5(1)(c): Minimize data collected | ✓ Signals use only necessary data |
| **Purpose Limitation** | Art. 5(1)(b): Compatible purposes only | ✓ Fraud prevention only, no secondary use |
| **Storage Limitation** | Art. 5(1)(e): No longer than needed | ✓ 30-365 day retention defined |
| **Accuracy** | Art. 5(1)(d): Accurate and up-to-date | ✓ Real-time data updates |
| **Integrity & Confidentiality** | Art. 5(1)(f): Secure processing | ✓ Encryption, access controls |
| **Subject Rights** | Arts. 15-22: Access, erasure, portability | ✓ PII access mechanisms defined |

**GDPR Risk Assessment:**
- **Risk Level:** Medium
- **Mitigation:** Pseudonymization, data minimization, clear privacy policy
- **DPIA Required:** No (fraud detection is core business function, not high-risk processing)

#### CCPA (California Consumer Privacy Act)

| Requirement | Framework Compliance |
|-------------|----------------------|
| **Right to Know** | ✓ Customers can access their transaction data |
| **Right to Delete** | ✓ Data retention limits enable deletion |
| **Right to Opt-Out** | N/A (no sale of data) |
| **Right to Non-Discrimination** | ✓ Automated decision-making with human review |
| **Data Minimization** | ✓ Only necessary data collected |

**CCPA Risk Assessment:**
- **Risk Level:** Low
- **Mitigation:** Clear disclosure, no data sale, opt-in for sharing

#### GLBA (Gramm-Leach-Bliley Act)

| Requirement | Framework Compliance |
|-------------|----------------------|
| **Financial Privacy Rule** | ✓ Notices to customers about data practices |
| **Safeguards Rule** | ✓ Encryption, access controls, security measures |
| **Pretexting Protection** | ✓ Identity verification before account changes |
| **Opt-Out** | ✓ Customers can opt-out of certain sharing |

**GLBA Risk Assessment:**
- **Risk Level:** Low
- **Mitigation:** Existing bank safeguards sufficient

#### AML/KYC (Anti-Money Laundering)

| Requirement | Framework Compliance |
|-------------|----------------------|
| **BSA/AML Sharing** | ✓ Cross-platform sharing permitted for fraud prevention |
| **KYC Requirements** | ✓ Identity verification preserved |
| **CTR Reporting** | ✓ Large transaction reporting maintained |
| **Record Retention** | ✓ 5-year retention for suspicious activity |

**AML/KYC Risk Assessment:**
- **Risk Level:** Low
- **Mitigation:** Data sharing explicitly permitted for fraud prevention

---

## Part 2: Privacy-Preserving Design

### Principle 1: Pseudonymization

**Definition:** Replace PII with tokens/hashes that cannot be reversed without secret key.

**Implementation:**

```python
class Pseudonymizer:
    """
    Handles pseudonymization of account IDs for detection system.
    """
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.salt_cache = {}  # For deterministic salts

    def pseudonymize(self, account_id):
        """
        Convert account ID to pseudonym.
        Same account ID always produces same pseudonym.
        """
        if account_id not in self.salt_cache:
            self.salt_cache[account_id] = generate_secure_salt()

        salt = self.salt_cache[account_id]
        pseudonym = hmac_sha256(self.secret_key, account_id + salt)

        return {
            'pseudonym': pseudonym,
            'version': 1,  # For key rotation
            'created_at': current_timestamp()
        }

    def reverse_pseudonym(self, pseudonym, access_reason):
        """
        Reverse pseudonym to account ID.
        Requires: Audit log + legitimate access reason.
        """
        if not self.legitimate_access(access_reason):
            raise SecurityException("Unauthorized pseudonym reversal")

        account_id = self.lookup_pseudonym(pseudonym)

        # Log access
        self.log_access({
            'pseudonym': pseudonym,
            'account_id': account_id,
            'reason': access_reason,
            'timestamp': current_timestamp(),
            'operator': current_operator()
        })

        return account_id

    def legitimate_access(self, reason):
        """
        Check if access reason is legitimate.
        Legitimate reasons: fraud_investigation, legal_requirement, customer_request
        """
        legitimate_reasons = [
            'fraud_investigation',
            'legal_requirement',
            'customer_request',
            'regulatory_compliance'
        ]
        return reason in legitimate_reasons
```

**Key Properties:**
- **One-way function:** Pseudonym → Account ID requires secret key
- **Deterministic:** Same account ID always produces same pseudonym
- **Audit trail:** All reversals logged with reason

### Principle 2: Data Minimization

**Strategy:** Store only data required for each signal.

| Signal Type | Data Stored | Data NOT Stored |
|-------------|-------------|-----------------|
| **Economic** | Hashed account ID, amounts, timestamps, merchant category | Name, address, document images |
| **Network** | Hashed account IDs, graph edges | Names, personal details |
| **Temporal** | Hashed account ID, timestamps | Personal identifiers |
| **Cross-Platform** | Identity hash (no PII), behavioral fingerprint | Raw PII, cross-platform IDs |

**Implementation Schema:**

```sql
-- Pseudonymized Transaction Table
CREATE TABLE tx_signals (
    pseudonym_id VARCHAR(64) NOT NULL,  -- Hashed account ID
    counterparty_pseudo VARCHAR(64) NOT NULL,
    amount DECIMAL(20, 2) NOT NULL,
    currency CHAR(3) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    merchant_category VARCHAR(32),
    signal_features JSON,  -- Pre-computed signal features
    INDEX idx_pseudonym (pseudonym_id),
    INDEX idx_timestamp (timestamp)
);

-- PII Lookup Table (separate, restricted access)
CREATE TABLE pii_lookup (
    pseudonym_id VARCHAR(64) PRIMARY KEY,
    real_account_id VARCHAR(64) NOT NULL,  -- Actual account ID
    encryption_version INT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,  -- For GDPR right to erasure
    access_log JSON,  -- Track all accesses
    INDEX idx_real_account (real_account_id)
);
```

### Principle 3: Separation of Duties

**Architecture:** PII and signal data are physically separated.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Application Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Web App     │  │  Mobile App  │  │  API         │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
└─────────┼──────────────────┼──────────────────┼─────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
    ┌─────────────────────────────────────────────────────────┐
    │                   API Gateway / Auth                   │
    └────────────────────────────┬────────────────────────────┘
                                 │
              ┌──────────────────┴──────────────────┐
              ▼                                     ▼
    ┌───────────────────┐               ┌───────────────────┐
    │  Signal Service   │               │  PII Service       │
    │  (pseudonymized)  │               │  (encrypted)       │
    │                   │               │                   │
    │  - Economic       │               │  - Account lookup  │
    │  - Network        │               │  - KYC data        │
    │  - Temporal       │               │  - Documents       │
    │  - Cross-Platform │               │  - Name, address   │
    └───────────────────┘               └───────────────────┘
              │                                     │
              ▼                                     ▼
    ┌───────────────────┐               ┌───────────────────┐
    │  Signal Database  │               │  PII Database      │
    │  (pseudonymized)  │               │  (encrypted)       │
    └───────────────────┘               └───────────────────┘
```

**Access Rules:**
- **Signal Service:** No access to PII database
- **PII Service:** No access to raw behavioral data
- **Human Review:** Can access PII only after fraud confirmed

### Principle 4: Privacy-Preserving Cross-Platform Correlation

**Challenge:** Cross-platform correlation without sharing PII.

**Solution:** Federated identity hashing + behavioral fingerprinting.

```python
class PrivacyPreservingCorrelation:
    """
    Enables cross-platform fraud detection without PII sharing.
    """

    def create_identity_hash(self, account_data, platform_salt):
        """
        Create platform-independent identity hash.
        Same account produces same hash across platforms.
        """
        # Hash stable attributes (PII-free where possible)
        stable_attrs = {
            'country': account_data.country,
            'entity_type': account_data.entity_type,
            # Hash PII before including
            'tax_id_hash': hash_string(account_data.tax_id),
            'reg_number_hash': hash_string(account_data.registration_number)
        }

        canonical = json.dumps(stable_attrs, sort_keys=True)
        hash_input = canonical + platform_salt

        return hashlib.sha256(hash_input.encode()).hexdigest()

    def create_behavioral_fingerprint(self, transactions):
        """
        Create fingerprint from transaction behavior.
        No PII included.
        """
        features = self.extract_behavioral_features(transactions)
        vector = np.array(list(features.values()))

        # Normalize and hash
        normalized = self.normalize_vector(vector)
        fingerprint = hashlib.sha256(normalized.tobytes()).hexdigest()

        return {
            'fingerprint': fingerprint,
            'features': features,  # Summary statistics only
            'vector': normalized.tolist()
        }

    def cross_platform_query(self, identity_hash, fingerprint):
        """
        Query other platforms for matching identity/behavior.
        Platforms respond with match (yes/no) only, no PII.
        """
        query = {
            'identity_hash': identity_hash,
            'fingerprint': fingerprint,
            'response_format': 'match_only'  # No PII returned
        }

        results = {}
        for platform in self.participating_platforms:
            try:
                response = platform.query(query)
                if response.get('match'):
                    results[platform] = {
                        'match': True,
                        'confidence': response.get('confidence')
                    }
            except Exception:
                continue

        return results
```

**Protocol Specification:**

```
Request Format:
{
  "identity_hash": "abc123...",
  "fingerprint": "def456...",
  "query_type": "match_only",
  "requesting_platform": "platform_A",
  "request_id": "uuid-1234",
  "timestamp": "2026-03-22T10:00:00Z"
}

Response Format:
{
  "match": true,
  "confidence": 0.85,
  "platform": "platform_B",
  "request_id": "uuid-1234"
}
```

**Key Property:** No PII is exchanged. Platforms only respond whether they have a matching identity/behavior, not who it is.

---

## Part 3: Compliance Roadmap

### GDPR Compliance Path

#### Data Protection Impact Assessment (DPIA)

**Conclusion:** DPIA not required (fraud detection = core business function, not high-risk processing under GDPR Article 35).

**Justification:**
- Fraud detection is legitimate interest (Art. 6(1)(f))
- No automated decision-making with legal effects (human review for high-risk)
- Data minimization built into design
- Pseudonymization reduces risk

#### Privacy Policy Disclosure

**Required Disclosures:**

```markdown
## Fraud Detection Privacy Notice

**What data we collect:**
- Transaction amounts and timestamps
- Merchant categories
- Network relationship data (who you transact with)
- Temporal patterns (when you transact)

**How we use it:**
- Detect and prevent fraudulent transactions
- Identify suspicious patterns across our platform
- Comply with anti-money laundering regulations

**Legal basis:** Legitimate interest (fraud prevention)

**Your rights:**
- Access your data
- Request deletion (subject to legal retention requirements)
- Opt-out of certain behavioral analysis
- Object to automated decisions

**Data retention:**
- Transaction data: 5 years (legal requirement)
- Behavioral features: 90 days
- Suspicious activity records: 5 years
```

#### Subject Rights Implementation

**Right to Access (Art. 15):**

```python
def handle_data_access_request(account_id, requesting_user):
    """
    Provide customer with their personal data.
    """
    # Verify requester is account holder
    if not verify_identity(account_id, requesting_user):
        raise SecurityException("Unauthorized access request")

    # Gather data from PII database
    pii_data = pii_service.get_account_data(account_id)

    # Gather behavioral data (pseudonymized)
    signal_data = signal_service.get_behavioral_summary(
        pseudonymize(account_id)
    )

    # Combine and return
    return {
        'personal_data': pii_data,
        'behavioral_summary': signal_data,
        'retention_info': get_retention_info(account_id),
        'provided_at': current_timestamp()
    }
```

**Right to Erasure (Art. 17):**

```python
def handle_erasure_request(account_id, requesting_user):
    """
    Handle GDPR right to erasure request.
    """
    # Verify requester is account holder
    if not verify_identity(account_id, requesting_user):
        raise SecurityException("Unauthorized erasure request")

    # Check legal retention requirements
    if has_legal_hold(account_id):
        return {
            'status': 'denied',
            'reason': 'Legal retention requirement',
            'retention_until': get_legal_hold_expiry(account_id)
        }

    # Erase pseudonymized data
    pseudonym = pseudonymize(account_id)
    signal_service.delete_account_data(pseudonym)

    # Anonymize PII (keep for legal records but make irreversible)
    pii_service.anonymize_account(account_id)

    # Confirm to customer
    return {
        'status': 'completed',
        'erased_at': current_timestamp()
    }
```

**Right to Portability (Art. 20):**

```python
def handle_portability_request(account_id, requesting_user):
    """
    Provide data in machine-readable format.
    """
    if not verify_identity(account_id, requesting_user):
        raise SecurityException("Unauthorized portability request")

    # Export data
    data = {
        'format': 'JSON',
        'version': '1.0',
        'account_data': pii_service.get_account_data(account_id),
        'transactions': get_transaction_history(account_id),
        'behavioral_features': signal_service.get_features(account_id)
    }

    # Return as downloadable file
    return create_export_file(data, account_id)
```

### CCPA Compliance Path

#### Notice at Collection

```markdown
## California Privacy Notice

**Categories of Collected Information:**
- Identifiers (account number, device ID)
- Financial information (transaction amounts, payment history)
- Internet activity (timing of transactions, merchant categories)
- Inferences (fraud risk scores, behavioral patterns)

**Purposes:**
- Fraud prevention and detection
- Security screening
- Compliance with legal requirements

**Sharing:**
- We do not sell your personal information
- We may share with service providers for fraud prevention
- We may share as required by law (AML/KYC)

**Your Rights:**
- Right to know what we collect
- Right to delete (with exceptions for legal requirements)
- Right to opt-out of data sharing
- Right to non-discrimination
```

#### Do Not Sell My Information

**Implementation:** Since no data sale occurs, provide clear notice:

```python
# No actual opt-out needed, but provide mechanism for transparency
def ccpa_opt_out_handler(account_id):
    """
    CCPA "Do Not Sell" opt-out handler.
    Even though we don't sell data, we provide this for transparency.
    """
    # Log opt-out preference
    set_ccpa_preference(account_id, 'opt_out_sale': True)

    return {
        'status': 'confirmed',
        'message': 'We do not sell your information. Your preference has been recorded.'
    }
```

### GLBA Compliance Path

#### Privacy Notice to Customers

**Required Components (GLBA §503):**

1. **Categories of collected information**
   - Transaction information
   - Account information
   - Identification information

2. **Categories of disclosure**
   - Service providers (fraud detection services)
   - Law enforcement (when required)
   - Regulatory agencies

3. **Confidentiality and security**
   - Encryption standards
   - Access controls
   - Employee training

4. **Customer opt-out**
   - Disclosure to non-affiliated third parties
   - Customer can opt-out

**Implementation:**

```python
def glba_disclosure_handler(account_id):
    """
    Provide GLBA-mandated disclosure to customer.
    """
    return {
        'information_collected': [
            'Transaction history',
            'Account information',
            'Device identifiers'
        ],
        'disclosure_parties': [
            'Fraud detection service providers',
            'Payment processors',
            'Law enforcement (when required by law)'
        ],
        'security_practices': [
            '256-bit encryption',
            'Multi-factor authentication',
            'Access logging and monitoring',
            'Regular security audits'
        ],
        'opt_out_available': True,
        'opt_out_method': 'contact_privacy@example.com'
    }
```

### AML/KYC Compliance Path

#### Permissible Data Sharing

**BSA/AML Exception:** Cross-platform data sharing is explicitly permitted for fraud prevention and anti-money laundering.

```python
def aml_data_sharing_agreement():
    """
    Template for cross-platform data sharing agreement.
    """
    agreement = {
        'purpose': 'Fraud prevention and AML compliance',
        'legal_basis': 'Bank Secrecy Act, USA PATRIOT Act',
        'permitted_sharing': [
            'Identity hashes (no PII)',
            'Behavioral fingerprints',
            'Fraud risk scores',
            'Suspicious activity reports'
        ],
        'prohibited_sharing': [
            'Raw PII (names, addresses)',
            'Full transaction history',
            'Customer documents'
        ],
        'data_retention': '5 years for flagged activity',
        'customer_rights': 'Right to access and correction',
        'liability': 'Shared liability for data breaches'
    }

    return agreement
```

#### Suspicious Activity Report (SAR)

When fraud is detected, SAR must be filed. Privacy framework supports this:

```python
def generate_sar(fraud_case_id):
    """
    Generate Suspicious Activity Report.
    Accesses PII only for confirmed fraud cases.
    """
    case = get_fraud_case(fraud_case_id)

    if not case.confirmed:
        raise SecurityException("SAR only for confirmed fraud")

    # Access PII for SAR filing
    pseudonym = case.pseudonym
    account_id = pii_service.reverse_pseudonym(
        pseudonym,
        access_reason='legal_requirement_sar'
    )

    # Gather SAR information
    sar = {
        'case_id': fraud_case_id,
        'account_id': account_id,
        'suspicious_activity': case.suspicious_patterns,
        'transaction_details': case.involved_transactions,
        'signal_scores': case.signal_scores,
        'reporting_date': current_date(),
        'filed_by': current_operator()
    }

    # File with FinCEN (or relevant authority)
    fincen_filing = file_sar(sar)

    # Log filing
    log_sar_filing({
        'case_id': fraud_case_id,
        'sar_reference': fincen_filing.reference,
        'filed_at': current_timestamp()
    })

    return fincen_filing
```

---

## Part 4: Data Retention Policy

### Retention Schedule

| Data Category | Retention Period | Legal Basis | Deletion Mechanism |
|---------------|------------------|--------------|-------------------|
| **Raw transactions** | 5 years | BSA/AML requirement | Secure delete after 5 years |
| **Signal features** | 90 days | Business necessity | Automated deletion |
| **Network graphs** | 90 days | Business necessity | Automated deletion |
| **Suspicious activity records** | 5 years | Legal requirement | Secure delete after 5 years |
| **PII lookup table** | 2 years post-closure | Business necessity | Automated deletion |
| **Access logs** | 1 year | Audit requirement | Automated deletion |
| **Cross-platform queries** | 1 year | Audit requirement | Automated deletion |

### Deletion Implementation

```python
class DataRetentionManager:
    """
    Manages automated data deletion per retention policy.
    """

    def process_expired_data(self):
        """
        Run daily to delete expired data.
        """
        # Delete expired signal features
        expired_signals = self.get_expired_signal_data(days=90)
        for record in expired_signals:
            self.secure_delete('signal_db', record.id)
            self.log_deletion(record)

        # Delete expired network graphs
        expired_graphs = self.get_expired_graph_data(days=90)
        for record in expired_graphs:
            self.secure_delete('graph_db', record.id)
            self.log_deletion(record)

        # Delete expired PII lookup entries
        expired_pii = self.get_expired_pii_lookup(days=730)  # 2 years
        for record in expired_pii:
            if not self.has_legal_hold(record.account_id):
                self.secure_delete('pii_db', record.id)
                self.log_deletion(record)

        # Archive (not delete) suspicious activity records
        # These are kept for 5 years per legal requirement
        self.archive_suspicious_activity()

    def secure_delete(self, database, record_id):
        """
        Securely delete record (overwrite before delete).
        """
        # 1. Overwrite data
        record = database.get(record_id)
        for _ in range(3):  # 3-pass overwrite
            database.update(record_id, {'data': random_string(len(record.data))})

        # 2. Delete record
        database.delete(record_id)

        # 3. Verify deletion
        if database.exists(record_id):
            raise DataRetentionException("Secure delete failed")
```

---

## Part 5: Data Governance

### Access Control Matrix

| Role | PII Access | Signal Data Access | Cross-Platform Access |
|------|-----------|-------------------|----------------------|
| **Detection Algorithm** | None | Read-only (pseudonymized) | None |
| **Human Reviewer** | Read (flagged cases only) | Read (flagged cases only) | None |
| **Fraud Investigator** | Read (confirmed cases) | Read (confirmed cases) | Read (hashes only) |
| **Compliance Officer** | Read/Write | Read/Write | Read/Write |
| **Auditor** | Read (audit log only) | Read (audit log only) | Read (audit log only) |
| **Platform Partner** | None | None | Read (hashes only) |

### Audit Logging

All access to PII or raw data must be logged:

```python
def audit_log_access(access_type, resource, operator, justification):
    """
    Log all sensitive data access.
    """
    log_entry = {
        'timestamp': current_timestamp(),
        'operator': operator,
        'access_type': access_type,  # 'PII_READ', 'PII_REVERSE', 'CROSS_PLATFORM_QUERY'
        'resource': resource,  # account_id, pseudonym, etc.
        'justification': justification,
        'ip_address': get_client_ip(),
        'session_id': get_session_id(),
        'outcome': 'success'  # or 'failure'
    }

    # Write to append-only audit log
    audit_log.append(log_entry)

    # Also send to SIEM for monitoring
    siem.send_event('DATA_ACCESS', log_entry)
```

### Data Breach Response Plan

```python
class DataBreachResponder:
    """
    Protocol for responding to data breaches.
    """

    def assess_breach(self, incident):
        """
        Assess breach severity and determine response.
        """
        severity = self.calculate_severity(incident)

        if severity == 'HIGH':
            self.activate_high_severity_protocol(incident)
        elif severity == 'MEDIUM':
            self.activate_medium_severity_protocol(incident)
        else:
            self.activate_low_severity_protocol(incident)

    def calculate_severity(self, incident):
        """
        Calculate breach severity based on data exposed.
        """
        factors = {
            'pii_exposed': incident.includes_pii,
            'record_count': incident.records_affected,
            'sensitive_data': incident.includes_financial_data,
            'encrypted': incident.data_was_encrypted,
            'access_gained': incident.unauthorized_access
        }

        score = 0
        if factors['pii_exposed']:
            score += 40
        if factors['record_count'] > 10000:
            score += 30
        if factors['sensitive_data']:
            score += 20
        if not factors['encrypted']:
            score += 20
        if factors['access_gained']:
            score += 30

        if score >= 80:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        else:
            return 'LOW'

    def activate_high_severity_protocol(self, incident):
        """
        High severity: Notify regulators within 72 hours (GDPR).
        """
        # 1. Containment
        self.contain_breach(incident)

        # 2. Notification
        self.notify_regulators(incident)  # Within 72 hours
        self.notify_affected_individuals(incident)
        self.notify_media(incident)  # If required

        # 3. Documentation
        self.create_breach_report(incident)

        # 4. Remediation
        self.remediate_breach(incident)
```

---

## Part 6: Customer Communication

### Privacy Notice Template

```markdown
# Privacy Policy - Fraud Detection

## How We Protect Your Information

### What We're Doing Differently

Our fraud detection system is designed with **privacy by design**:

1. **Separation of PII:** Your personal information is stored separately from your behavioral data. Our fraud detection algorithms analyze patterns without accessing your name, address, or other personal details.

2. **Pseudonymization:** Your account is represented by a random token in our detection system. Even if someone accessed the detection database, they couldn't identify you.

3. **Data Minimization:** We only collect the data needed for fraud detection. We don't store unnecessary information about your transactions.

4. **Cross-Platform Privacy:** When we work with other platforms to detect fraud, we exchange only anonymous hashes—not your personal information.

### What Data We Use

**For Fraud Detection:**
- Transaction amounts (not what you bought, just how much)
- Transaction times (when you transact)
- Merchant categories (e.g., "retail," "dining")
- Network patterns (who you transact with, anonymously)

**NOT Used for Detection:**
- Your name or address
- What specific items you purchased
- Your account balance
- Your personal documents

### Your Rights

- **Access:** Request a copy of your data
- **Deletion:** Request deletion (subject to legal requirements)
- **Opt-out:** Opt-out of certain behavioral analysis
- **Object:** Object to automated decisions (human review available)

### Questions?

Contact us at privacy@example.com
```

---

## Conclusion

**Summary:** The agent-invariant detection framework is compatible with all major privacy regulations when implemented with the safeguards described in this document.

**Compliance Status:**
- ✓ GDPR: Feasible with pseudonymization and data minimization
- ✓ CCPA: Feasible with clear disclosure and opt-out mechanisms
- ✓ GLBA: Feasible within existing bank safeguards framework
- ✓ AML/KYC: Data sharing explicitly permitted

**Implementation Priority:**
1. **Phase 1:** Implement pseudonymization layer
2. **Phase 2:** Separate PII and signal databases
3. **Phase 3:** Implement access control and audit logging
4. **Phase 4:** Deploy cross-platform privacy-preserving correlation

**No Showstopper Issues:** All regulatory requirements can be met with appropriate safeguards.

---

**Document Status:** COMPLETE
**Companion Document:** `analysis/privacy-compliance-roadmap.md` (detailed implementation guidance)
