# Output Classification

## Purpose

This document defines classification frameworks for ClimateOS validation process outputs.

Output classification enables structured handling, routing, and delivery of validation outputs.

## Classification Dimensions

### Primary Dimension: Output Type

Outputs are classified by their output structure and purpose.

```text
OutputType {
    VALIDATION_RESULT,
    VALIDATION_PACK,
    REVIEW_MATERIAL,
    EVIDENCE_UPDATE,
    KNOWLEDGE_UPDATE,
    GOVERNANCE_RECOMMENDATION,
    CONFIDENCE_ASSESSMENT,
    REVISION_RECORD,
    ERROR_REPORT,
    STATUS_UPDATE
}
```

### Secondary Dimension: Output Status

Outputs are classified by their lifecycle status.

```text
OutputStatus {
    DRAFT,          // Output is draft, not yet finalized
    FINAL,          // Output is finalized and approved
    REVISED,        // Output has been revised
    ARCHIVED,       // Output is archived
    REJECTED        // Output is rejected
}
```

### Tertiary Dimension: Output Confidence Level

Outputs are classified by their confidence level.

```text
OutputConfidenceLevel {
    VERY_HIGH,      // Strong evidence, multiple sources, consistent
    HIGH,           // Good evidence, reliable source, consistent
    MODERATE,       // Adequate evidence, some uncertainty
    LOW,            // Limited evidence, high uncertainty
    VERY_LOW,       // Minimal evidence, very high uncertainty
    INSUFFICIENT    // Insufficient evidence to assess confidence
}
```

### Quaternary Dimension: Output Actionability

Outputs are classified by their actionability for governance or operations.

```text
OutputActionability {
    IMMEDIATE_ACTION,      // Requires immediate action
    SHORT_TERM_ACTION,     // Requires action within short timeframe
    MEDIUM_TERM_ACTION,    // Requires action within medium timeframe
    LONG_TERM_ACTION,      // Requires action within long term
    INFORMATIONAL,         // Informational only, no action required
    REVISION_REQUIRED      // Requires revision before action
}
```

### Quinary Dimension: Output Delivery Priority

Outputs are classified by their delivery priority.

```text
OutputDeliveryPriority {
    CRITICAL,       // Must be delivered immediately
    HIGH,           // Must be delivered within short timeframe
    NORMAL,         // Standard delivery timeframe
    LOW,            // Can be delivered with delay
    BATCH           // Can be delivered in batch
}
```

## Output Classification Framework

### Classification Matrix

Outputs are classified along multiple dimensions:

```text
OutputClassification {
    output_type: OutputType
    output_status: OutputStatus
    confidence_level: OutputConfidenceLevel
    actionability: OutputActionability
    delivery_priority: OutputDeliveryPriority
    evidence_strength: evidence_strength_enum
    traceability_status: traceability_enum
    revision_status: revision_enum
    governance_readiness: governance_readiness_enum
}
```

### Classification Rules

#### Rule 1: Validation Results

```text
IF output_type == VALIDATION_RESULT:
    output_status ∈ {DRAFT, FINAL, REVISED}
    confidence_level ∈ {VERY_HIGH, HIGH, MODERATE, LOW, VERY_LOW, INSUFFICIENT}
    actionability ∈ {IMMEDIATE_ACTION, SHORT_TERM_ACTION, MEDIUM_TERM_ACTION, INFORMATIONAL, REVISION_REQUIRED}
```

#### Rule 2: Validation Packs

```text
IF output_type == VALIDATION_PACK:
    output_status == FINAL (must be finalized before pack assembly)
    confidence_level ∈ {VERY_HIGH, HIGH, MODERATE}
    actionability ∈ {SHORT_TERM_ACTION, MEDIUM_TERM_ACTION, INFORMATIONAL}
```

#### Rule 3: Review Materials

```text
IF output_type == REVIEW_MATERIAL:
    output_status ∈ {DRAFT, FINAL}
    confidence_level ∈ {VERY_HIGH, HIGH, MODERATE}
    actionability ∈ {IMMEDIATE_ACTION, SHORT_TERM_ACTION, MEDIUM_TERM_ACTION}
```

#### Rule 4: Governance Recommendations

```text
IF output_type == GOVERNANCE_RECOMMENDATION:
    output_status == FINAL (must be finalized before governance submission)
    confidence_level ∈ {VERY_HIGH, HIGH}
    actionability ∈ {IMMEDIATE_ACTION, SHORT_TERM_ACTION, MEDIUM_TERM_ACTION}
```

#### Rule 5: Evidence/Knowledge Updates

```text
IF output_type IN {EVIDENCE_UPDATE, KNOWLEDGE_UPDATE}:
    output_status ∈ {DRAFT, FINAL, REVISED}
    confidence_level ∈ {VERY_HIGH, HIGH, MODERATE}
    actionability ∈ {INFORMATIONAL, REVISION_REQUIRED}
```

## Output Routing Based on Classification

### Routing by Output Type

```text
VALIDATION_RESULT → Validation Record Storage
VALIDATION_PACK → Validation Pack Layer
REVIEW_MATERIAL → Review Engine
EVIDENCE_UPDATE → Evidence Layer
KNOWLEDGE_UPDATE → Knowledge Runtime
GOVERNANCE_RECOMMENDATION → Governance Layer
CONFIDENCE_ASSESSMENT → Confidence Framework Layer
REVISION_RECORD → Revision Tracking System
```

### Routing by Confidence Level

```text
VERY_HIGH → Immediate delivery and action
HIGH → Standard delivery and action
MODERATE → Delivery with additional context
LOW → Delivery with cautionary notes
VERY_LOW → Delivery with strong caveats
INSUFFICIENT → Revision required before delivery
```

### Routing by Actionability

```text
IMMEDIATE_ACTION → Urgent delivery to governance/operations
SHORT_TERM_ACTION → Delivery within short timeframe
MEDIUM_TERM_ACTION → Delivery within medium timeframe
LONG_TERM_ACTION → Delivery within long term
INFORMATIONAL → Delivery to information repository
REVISION_REQUIRED → Return to revision process
```

### Routing by Delivery Priority

```text
CRITICAL → Immediate delivery (priority queue)
HIGH → Delivery within 24 hours
NORMAL → Delivery within standard timeframe
LOW → Delivery within extended timeframe
BATCH → Delivery in next batch cycle
```

## Output Delivery Classification

### Delivery Method Classification

Outputs are delivered using appropriate methods:

```text
DeliveryMethod {
    IMMEDIATE_NOTIFICATION,  // Immediate notification to stakeholders
    DIRECT_INTEGRATION,      // Direct integration with destination system
    PACK_ASSEMBLY,           // Assembly into validation pack
    REVIEW_SUBMISSION,       // Submission to Review Engine
    GOVERNANCE_SUBMISSION,  // Submission to governance process
    STORAGE,                 // Storage in repository
    PUBLICATION,             // Publication to stakeholders
    BATCH_DELIVERY           // Delivery in batch
}
```

### Delivery Method Selection

```text
IF delivery_priority == CRITICAL:
    delivery_method = IMMEDIATE_NOTIFICATION
    
IF output_type == VALIDATION_PACK:
    delivery_method = PACK_ASSEMBLY
    
IF output_type == REVIEW_MATERIAL:
    delivery_method = REVIEW_SUBMISSION
    
IF output_type == GOVERNANCE_RECOMMENDATION:
    delivery_method = GOVERNANCE_SUBMISSION
    
IF actionability == INFORMATIONAL:
    delivery_method = STORAGE or PUBLICATION
```

## Output Prioritization

### Priority Calculation

Output priority is calculated based on classification:

```text
Priority = f(confidence, actionability, delivery_priority, evidence_strength)

Where:
- confidence: VERY_HIGH=5, HIGH=4, MODERATE=3, LOW=2, VERY_LOW=1, INSUFFICIENT=0
- actionability: IMMEDIATE_ACTION=5, SHORT_TERM_ACTION=4, MEDIUM_TERM_ACTION=3, LONG_TERM_ACTION=2, INFORMATIONAL=1, REVISION_REQUIRED=0
- delivery_priority: CRITICAL=5, HIGH=4, NORMAL=3, LOW=2, BATCH=1
- evidence_strength: STRONG=5, MODERATE=3, WEAK=1
```

### Priority Categories

```text
Priority ≥ 15: CRITICAL priority (immediate delivery)
Priority 10-14: HIGH priority (delivery within 24 hours)
Priority 5-9: NORMAL priority (standard delivery)
Priority < 5: LOW priority (delayed delivery)
```

## Output Batch Classification

### Batch Types

Outputs can be batched by classification:

```text
BatchType {
    HOMOGENEOUS_BATCH,    // Same output type, similar priority
    HETEROGENEOUS_BATCH,  // Mixed output types, same delivery priority
    PRIORITY_BATCH,       // Same priority level
    DESTINATION_BATCH,    // Same destination
    ACTIONABILITY_BATCH   // Same actionability level
}
```

### Batch Assembly Rules

#### Rule 1: Homogeneous Batch

```text
IF batch_type == HOMOGENEOUS_BATCH:
    ALL outputs must have same output_type
    Priority variance must be ≤ 1 level
    Delivery method must be compatible
```

#### Rule 2: Priority Batch

```text
IF batch_type == PRIORITY_BATCH:
    ALL outputs must have same priority category
    Output types can be mixed
    Destinations can be mixed
```

#### Rule 3: Destination Batch

```text
IF batch_type == DESTINATION_BATCH:
    ALL outputs must have same destination
    Output types must be compatible
    Priority can be mixed
```

## Output Classification Governance

### Classification Responsibilities

1. **Generation**: Validation process classifies output at generation
2. **Review**: Output reviewer reviews and adjusts classification
3. **Approval**: Output approver approves final classification
4. **Delivery**: Delivery process uses classification for routing

### Classification Transparency

- Classification criteria must be documented
- Classification decisions must be traceable
- Classification rationale must be recorded
- Classification updates must be version-controlled

### Classification Quality

- Classification must be consistent across similar outputs
- Classification must be evidence-based
- Classification must be reviewable
- Classification must support revision

## Output Classification Examples

### Example 1: Validation Result with High Confidence

```text
Output: Validation result for evidence package
Classification:
    output_type: VALIDATION_RESULT
    output_status: FINAL
    confidence_level: HIGH
    actionability: SHORT_TERM_ACTION
    delivery_priority: HIGH
    evidence_strength: STRONG
    traceability_status: FULLY_TRACEABLE
    revision_status: CURRENT
    governance_readiness: READY
Priority: 4 + 4 + 4 + 5 = 17 (CRITICAL priority)
Delivery method: IMMEDIATE_NOTIFICATION
```

### Example 2: Validation Pack for Review

```text
Output: Validation pack for review
Classification:
    output_type: VALIDATION_PACK
    output_status: FINAL
    confidence_level: MODERATE
    actionability: MEDIUM_TERM_ACTION
    delivery_priority: NORMAL
    evidence_strength: MODERATE
    traceability_status: PARTIALLY_TRACEABLE
    revision_status: CURRENT
    governance_readiness: CONDITIONAL
Priority: 3 + 3 + 3 + 3 = 12 (HIGH priority)
Delivery method: PACK_ASSEMBLY
```

### Example 3: Governance Recommendation

```text
Output: Governance recommendation for policy revision
Classification:
    output_type: GOVERNANCE_RECOMMENDATION
    output_status: FINAL
    confidence_level: VERY_HIGH
    actionability: IMMEDIATE_ACTION
    delivery_priority: CRITICAL
    evidence_strength: STRONG
    traceability_status: FULLY_TRACEABLE
    revision_status: CURRENT
    governance_readiness: READY
Priority: 5 + 5 + 5 + 5 = 20 (CRITICAL priority)
Delivery method: GOVERNANCE_SUBMISSION
```

## Status

Documentation foundation only.

No runtime implementation, APIs, automated classification, scoring engine, workflow engine, or automated decisions.
