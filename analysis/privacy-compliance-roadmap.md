# Privacy Compliance Roadmap

**Phase:** 03-detection-framework, Plan 03-03
**Created:** 2026-03-22
**Status:** Complete

## Overview

This document provides a detailed implementation roadmap for privacy compliance across the detection framework, with specific tasks, timelines, and verification checkpoints.

---

## Implementation Roadmap

### Phase 1: Pseudonymization Layer (Weeks 1-4)

**Objective:** Implement pseudonymization of all account IDs before data enters detection system.

#### Tasks

| Task | Description | Owner | Duration | Dependencies |
|------|-------------|-------|----------|--------------|
| 1.1 | Design pseudonymization schema | Security Architect | 1 week | None |
| 1.2 | Implement Pseudonymizer service | Engineering | 2 weeks | 1.1 |
| 1.3 | Deploy pseudonymization API | DevOps | 1 week | 1.2 |
| 1.4 | Migrate existing data to pseudonymized form | Data Engineering | 2 weeks | 1.3 |
| 1.5 | Verify pseudonym properties | QA | 1 week | 1.4 |

**Deliverables:**
- Pseudonymization service API documentation
- Migration scripts for existing data
- Verification test suite

**Acceptance Criteria:**
- [ ] All account IDs pseudonymized before detection processing
- [ ] Pseudonyms are deterministic (same ID → same pseudonym)
- [ ] Pseudonyms are irreversible without secret key
- [ ] Performance impact <10ms per transaction

#### Technical Specification

```python
# Pseudonymization Service API

POST /pseudonymize
Request:
{
  "account_id": "acc_12345",
  "context": "fraud_detection"
}

Response:
{
  "pseudonym": "pseudo_abc123...",
  "version": 1,
  "created_at": "2026-03-22T10:00:00Z"
}

POST /reverse_pseudonym
Request:
{
  "pseudonym": "pseudo_abc123...",
  "access_reason": "fraud_investigation",
  "requester": "user_123",
  "justification": "Case #456 requires identity verification"
}

Response:
{
  "account_id": "acc_12345",
  "access_granted": true,
  "logged": true
}
```

---

### Phase 2: Data Separation (Weeks 5-8)

**Objective:** Physically separate PII storage from signal data storage.

#### Tasks

| Task | Description | Owner | Duration | Dependencies |
|------|-------------|-------|----------|--------------|
| 2.1 | Design separated database schema | Data Architect | 1 week | Phase 1 |
| 2.2 | Implement PII database with encryption | Engineering | 2 weeks | 2.1 |
| 2.3 | Implement signal database (pseudonymized) | Engineering | 2 weeks | 2.1 |
| 2.4 | Migrate data to separated architecture | Data Engineering | 3 weeks | 2.2, 2.3 |
| 2.5 | Implement access control layer | Security | 2 weeks | 2.4 |

**Deliverables:**
- Separated database architecture
- Access control policy implementation
- Data migration scripts

**Acceptance Criteria:**
- [ ] PII and signal databases on separate infrastructure
- [ ] Signal service has no direct access to PII database
- [ ] All PII access logged with justification
- [ ] Access control matrix enforced at database level

#### Database Schema

```sql
-- PII Database (encrypted, restricted access)
CREATE TABLE pii_accounts (
    account_id VARCHAR(64) PRIMARY KEY,
    pseudonym_id VARCHAR(64) UNIQUE NOT NULL,
    encrypted_name TEXT NOT NULL,  -- AES-256-GCM
    encrypted_address TEXT NOT NULL,
    kyc_documents JSONB,  -- Encrypted document storage
    created_at TIMESTAMP NOT NULL,
    last_accessed TIMESTAMP,
    access_log JSONB,
    expires_at TIMESTAMP  -- For GDPR right to erasure
);

-- Signal Database (pseudonymized only, broader access)
CREATE TABLE signal_transactions (
    pseudonym_id VARCHAR(64) NOT NULL,
    counterparty_pseudo VARCHAR(64) NOT NULL,
    amount DECIMAL(20, 2) NOT NULL,
    currency CHAR(3) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    merchant_category VARCHAR(32),
    signal_features JSONB,
    INDEX idx_pseudonym (pseudonym_id),
    INDEX idx_counterparty (counterparty_pseudo),
    INDEX idx_timestamp (timestamp)
);

-- Cross-reference table (restricted access)
CREATE TABLE pseudonym_lookup (
    pseudonym_id VARCHAR(64) PRIMARY KEY,
    account_id_ref VARCHAR(64) REFERENCES pii_accounts(account_id),
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    access_count INT DEFAULT 0,
    last_accessed TIMESTAMP
);
```

---

### Phase 3: Access Control & Audit (Weeks 9-12)

**Objective:** Implement role-based access control and comprehensive audit logging.

#### Tasks

| Task | Description | Owner | Duration | Dependencies |
|------|-------------|-------|----------|--------------|
| 3.1 | Define role-based access control matrix | Compliance | 1 week | Phase 2 |
| 3.2 | Implement RBAC in API gateway | Engineering | 2 weeks | 3.1 |
| 3.3 | Implement audit logging service | Engineering | 2 weeks | 3.2 |
| 3.4 | Integrate with SIEM for monitoring | Security Ops | 2 weeks | 3.3 |
| 3.5 | Conduct access control audit | Audit | 1 week | 3.4 |

**Deliverables:**
- RBAC policy documentation
- Audit logging service
- SIEM integration
- Access control audit report

**Acceptance Criteria:**
- [ ] All PII access requires appropriate role
- [ ] All PII access logged with justification
- [ ] Audit logs are append-only and tamper-evident
- [ ] Unauthorized access attempts generate alerts

#### RBAC Policy Definition

```yaml
# roles.yaml
roles:
  - name: detection_algorithm
    description: Service account for fraud detection algorithms
    permissions:
      - signal_database:read
      - pseudonym_lookup:read  # No PII access
    constraints:
      - automated_only: true
      - no_pii_access: true

  - name: human_reviewer
    description: Analyst who reviews flagged transactions
    permissions:
      - signal_database:read  # Flagged cases only
      - pii_database:read  # Via PII service only
      - audit_log:read
    constraints:
      - case_approval_required: true
      - pii_access_justification: required

  - name: fraud_investigator
    description: Senior investigator for confirmed fraud
    permissions:
      - signal_database:read
      - pii_database:read
      - cross_platform:read
      - audit_log:read
    constraints:
      - confirmed_cases_only: true
      - audit_log_frequency: per_access

  - name: compliance_officer
    description: Compliance and privacy oversight
    permissions:
      - all:read
      - pii_database:write
      - access_policy:write
    constraints:
      - annual_review_required: true

  - name: auditor
    description: External or internal auditor
    permissions:
      - audit_log:read
      - access_policy:read
    constraints:
      - read_only: true
      - investigation_scope: provided
```

#### Audit Logging Schema

```sql
-- Audit Log Table (append-only)
CREATE TABLE audit_log (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_timestamp TIMESTAMP NOT NULL,
    operator_id VARCHAR(64) NOT NULL,
    operator_role VARCHAR(32) NOT NULL,
    access_type VARCHAR(32) NOT NULL,  -- PII_READ, PII_REVERSE, etc.
    resource_type VARCHAR(32) NOT NULL,  -- ACCOUNT, TRANSACTION, etc.
    resource_id VARCHAR(64) NOT NULL,
    justification TEXT,
    ip_address INET NOT NULL,
    session_id VARCHAR(128),
    outcome VARCHAR(16) NOT NULL,  -- SUCCESS, FAILURE, DENIED
    additional_context JSONB,
    INDEX idx_operator (operator_id),
    INDEX idx_timestamp (event_timestamp),
    INDEX idx_resource (resource_type, resource_id)
);
```

---

### Phase 4: Cross-Platform Privacy (Weeks 13-16)

**Objective:** Implement privacy-preserving cross-platform correlation.

#### Tasks

| Task | Description | Owner | Duration | Dependencies |
|------|-------------|-------|----------|--------------|
| 4.1 | Draft cross-platform data sharing agreement | Legal | 2 weeks | None |
| 4.2 | Implement identity hashing protocol | Engineering | 2 weeks | 4.1 |
| 4.3 | Implement behavioral fingerprinting | Engineering | 2 weeks | 4.2 |
| 4.4 | Deploy cross-platform query API | Engineering | 2 weeks | 4.3 |
| 4.5 | Execute partnership agreements | Business | 4 weeks | 4.4 |

**Deliverables:**
- Cross-platform data sharing agreement template
- Identity hashing service
- Behavioral fingerprinting service
- Cross-platform query API

**Acceptance Criteria:**
- [ ] No PII exchanged between platforms
- [ ] Identity matching uses cryptographic hashes only
- [ ] Behavioral fingerprinting contains no PII
- [ ] All cross-platform queries logged

#### Cross-Platform API Protocol

```python
# Platform-to-Platform Query Protocol

POST /platform/query
Request:
{
  "query_type": "identity_match",
  "identity_hash": "abc123...",
  "behavioral_fingerprint": "def456...",
  "requesting_platform": "platform_A",
  "request_id": "uuid-1234",
  "timestamp": "2026-03-22T10:00:00Z",
  "signature": "HMAC-SHA256(request, shared_secret)"
}

# Response (NO PII returned)
Response:
{
  "match": true,
  "confidence": 0.85,
  "platform": "platform_B",
  "request_id": "uuid-1234",
  "timestamp": "2026-03-22T10:00:01Z",
  "signature": "HMAC-SHA256(response, shared_secret)"
}
```

---

### Phase 5: Customer Communication (Weeks 17-18)

**Objective:** Implement customer-facing privacy notices and consent mechanisms.

#### Tasks

| Task | Description | Owner | Duration | Dependencies |
|------|-------------|-------|----------|--------------|
| 5.1 | Draft privacy policy | Legal + Product | 2 weeks | Phase 1-4 |
| 5.2 | Implement consent management UI | Product | 2 weeks | 5.1 |
| 5.3 | Implement data access request UI | Product | 2 weeks | 5.1 |
| 5.4 | Implement deletion request UI | Product | 2 weeks | 5.1 |
| 5.5 | Deploy privacy notices | Marketing | 1 week | 5.1 |

**Deliverables:**
- Privacy policy documentation
- Consent management UI
- Data access request form
- Deletion request form
- Customer notification system

---

## Verification Checkpoints

### CP1: Pseudonymization Verification (Week 4)

**Objective:** Verify pseudonymization is correctly implemented.

```python
# Verification Tests
def test_pseudonymization():
    # Test 1: Deterministic
    id1 = pseudonymize("acc_12345")
    id2 = pseudonymize("acc_12345")
    assert id1.pseudonym == id2.pseudonym

    # Test 2: Unique (different accounts)
    id3 = pseudonymize("acc_67890")
    assert id1.pseudonym != id3.pseudonym

    # Test 3: Irreversible without key
    assert cannot_reverse_without_key(id1.pseudonym)

    # Test 4: Performance
    times = []
    for _ in range(1000):
        start = time.time()
        pseudonymize("acc_test")
        times.append(time.time() - start)
    assert np.percentile(times, 95) < 0.01  # <10ms
```

### CP2: Data Separation Verification (Week 8)

**Objective:** Verify PII and signal data are properly separated.

```python
# Verification Tests
def test_data_separation():
    # Test 1: Signal service cannot access PII
    signal_service = SignalService()
    with pytest.raises(PermissionError):
        signal_service.get_pii("pseudo_abc123")

    # Test 2: PII access requires justification
    pii_service = PIIService()
    with pytest.raises(PermissionError):
        pii_service.reverse_pseudonym("pseudo_abc123", justification=None)

    # Test 3: Audit logging
    pii_service.reverse_pseudonym("pseudo_abc123", justification="fraud_investigation")
    logs = get_audit_logs_for_pseudonym("pseudo_abc123")
    assert len(logs) > 0
    assert logs[0]['justification'] == "fraud_investigation"
```

### CP3: Access Control Verification (Week 12)

**Objective:** Verify RBAC is correctly enforced.

```python
# Verification Tests
def test_access_control():
    # Test 1: Detection algorithm has no PII access
    algorithm_role = get_role("detection_algorithm")
    assert "pii_database" not in algorithm_role.permissions

    # Test 2: Human reviewer requires justification
    reviewer_role = get_role("human_reviewer")
    assert reviewer_role.constraints["pii_access_justification"] == "required"

    # Test 3: Audit log created for each access
    access_pii(account_id="acc_123", role="human_reviewer")
    logs = get_audit_logs()
    assert any(log["resource_id"] == "acc_123" for log in logs)
```

### CP4: Cross-Platform Verification (Week 16)

**Objective:** Verify cross-platform queries preserve privacy.

```python
# Verification Tests
def test_cross_platform_privacy():
    # Test 1: No PII in request
    query = create_cross_platform_query(account_id="acc_123")
    assert "acc_123" not in query
    assert "identity_hash" in query

    # Test 2: No PII in response
    response = send_cross_platform_query(query)
    assert "account_id" not in response
    assert "match" in response

    # Test 3: Query logged
    logs = get_cross_platform_logs()
    assert len(logs) > 0
    assert logs[0]["query_type"] == "identity_match"
```

---

## Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| Phase 1: Pseudonymization | 4 weeks | Pseudonymizer service |
| Phase 2: Data Separation | 4 weeks | Separated database architecture |
| Phase 3: Access Control | 4 weeks | RBAC + audit logging |
| Phase 4: Cross-Platform | 4 weeks | Privacy-preserving correlation |
| Phase 5: Customer Comms | 2 weeks | Privacy notices and UI |

**Total Timeline:** 18 weeks (~4.5 months)

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|-------|------------|
| Pseudonymization performance | Low | High | Performance testing, caching |
| PII database breach | Low | High | Encryption at rest, access controls |
| Cross-platform adoption | Medium | High | Legal agreements, value proposition |
| Regulatory change | Low | Medium | Flexible architecture, monitoring |
| Customer opt-out | Low | Medium | Clear communication, value demonstration |

---

**Document Status:** COMPLETE
**Companion Document:** `analysis/privacy-preservation-analysis.md` (detailed analysis)
