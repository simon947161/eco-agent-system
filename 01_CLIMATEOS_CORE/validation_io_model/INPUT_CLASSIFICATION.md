# Input Classification

## Purpose

This document defines classification frameworks for ClimateOS validation process inputs.

Input classification enables structured handling, routing, and processing of validation inputs.

## Classification Dimensions

### Primary Dimension: Input Source

Inputs are classified by their source system or layer.

```text
InputSourceType {
    OBSERVATION_LAYER,
    RELATIONSHIP_LAYER,
    RADAR_LAYER,
    EVIDENCE_LAYER,
    KNOWLEDGE_RUNTIME,
    VALIDATION_LAYER,
    REVIEW_ENGINE,
    PARTICIPATION_LAYER,
    EXTERNAL_PROVIDER,
    GOVERNANCE_LAYER
}
```

### Secondary Dimension: Input Content Type

Inputs are classified by their content structure and purpose.

```text
InputContentType {
    EVIDENCE_OBJECT,
    EVIDENCE_PACKAGE,
    EVIDENCE_RELATIONSHIP,
    KNOWLEDGE_OBJECT,
    KNOWLEDGE_SOURCE,
    OBSERVATION_RECORD,
    OBSERVATION_EVENT,
    RELATIONSHIP_MODEL,
    RADAR_SIGNAL,
    VALIDATION_RECORD,
    VALIDATION_PACK,
    REVIEW_MATERIAL,
    PARTICIPANT_CONTRIBUTION,
    GOVERNANCE_REQUEST
}
```

### Tertiary Dimension: Input Confidence Level

Inputs are classified by their confidence level.

```text
InputConfidenceLevel {
    VERY_HIGH,      // Strong evidence, multiple sources, consistent
    HIGH,           // Good evidence, reliable source, consistent
    MODERATE,       // Adequate evidence, some uncertainty
    LOW,            // Limited evidence, high uncertainty
    VERY_LOW,       // Minimal evidence, very high uncertainty
    UNKNOWN         // Confidence not yet assessed
}
```

### Quaternary Dimension: Input Urgency

Inputs are classified by their processing urgency.

```text
InputUrgency {
    CRITICAL,       // Immediate processing required
    HIGH,           // Processing required within short timeframe
    NORMAL,         // Standard processing timeframe
    LOW,            // Processing can be delayed
    DEFERRED        // Processing deferred to future batch
}
```

### Quinary Dimension: Input Complexity

Inputs are classified by their processing complexity.

```text
InputComplexity {
    SIMPLE,         // Single object, straightforward validation
    MODERATE,       // Multiple objects, some relationships
    COMPLEX,        // Many objects, complex relationships
    VERY_COMPLEX    // Large number of objects, very complex relationships
}
```

## Input Classification Framework

### Classification Matrix

Inputs are classified along multiple dimensions:

```text
InputClassification {
    source_type: InputSourceType
    content_type: InputContentType
    confidence_level: InputConfidenceLevel
    urgency: InputUrgency
    complexity: InputComplexity
    evidence_weight: evidence_weight_enum
    traceability_status: traceability_enum
    revision_status: revision_enum
}
```

### Classification Rules

#### Rule 1: Evidence Objects

```text
IF content_type == EVIDENCE_OBJECT:
    source_type ∈ {EVIDENCE_LAYER, OBSERVATION_LAYER, RELATIONSHIP_LAYER}
    confidence_level ∈ {VERY_HIGH, HIGH, MODERATE, LOW, VERY_LOW, UNKNOWN}
    complexity ∈ {SIMPLE, MODERATE}
```

#### Rule 2: Evidence Packages

```text
IF content_type == EVIDENCE_PACKAGE:
    source_type == EVIDENCE_LAYER
    confidence_level ∈ {VERY_HIGH, HIGH, MODERATE}
    complexity ∈ {MODERATE, COMPLEX, VERY_COMPLEX}
```

#### Rule 3: Knowledge Objects

```text
IF content_type == KNOWLEDGE_OBJECT:
    source_type == KNOWLEDGE_RUNTIME
    confidence_level ∈ {VERY_HIGH, HIGH, MODERATE, LOW}
    complexity ∈ {SIMPLE, MODERATE}
```

#### Rule 4: Observation Records

```text
IF content_type == OBSERVATION_RECORD:
    source_type == OBSERVATION_LAYER
    confidence_level ∈ {HIGH, MODERATE, LOW}
    complexity ∈ {SIMPLE}
```

#### Rule 5: Validation Packs

```text
IF content_type == VALIDATION_PACK:
    source_type == VALIDATION_LAYER
    confidence_level ∈ {VERY_HIGH, HIGH, MODERATE}
    complexity ∈ {COMPLEX, VERY_COMPLEX}
```

## Input Routing Based on Classification

### Routing by Source Type

```text
OBSERVATION_LAYER → Observation Validation Pipeline
RELATIONSHIP_LAYER → Relationship Validation Pipeline
EVIDENCE_LAYER → Evidence Validation Pipeline
KNOWLEDGE_RUNTIME → Knowledge Validation Pipeline
VALIDATION_LAYER → Validation Review Pipeline
REVIEW_ENGINE → Review Validation Pipeline
```

### Routing by Confidence Level

```text
VERY_HIGH → Fast-track validation (simplified process)
HIGH → Standard validation process
MODERATE → Standard validation process with additional review
LOW → Extended validation process with multiple review stages
VERY_LOW → Rejection or request for additional evidence
UNKNOWN → Confidence assessment required before validation
```

### Routing by Urgency

```text
CRITICAL → Immediate processing (priority queue)
HIGH → Processing within 24 hours
NORMAL → Processing within standard timeframe (e.g., 72 hours)
LOW → Processing within extended timeframe (e.g., 1 week)
DEFERRED → Processing in next batch cycle
```

### Routing by Complexity

```text
SIMPLE → Automated or single-reviewer validation
MODERATE → Standard validation workflow
COMPLEX → Multi-stage validation workflow
VERY_COMPLEX → Full validation pipeline with multiple review stages
```

## Input Prioritization

### Priority Calculation

Input priority is calculated based on classification:

```text
Priority = f(urgency, confidence, complexity, evidence_weight)

Where:
- urgency: CRITICAL=5, HIGH=4, NORMAL=3, LOW=2, DEFERRED=1
- confidence: VERY_HIGH=5, HIGH=4, MODERATE=3, LOW=2, VERY_LOW=1, UNKNOWN=0
- complexity: VERY_COMPLEX=1, COMPLEX=2, MODERATE=3, SIMPLE=4 (inverse)
- evidence_weight: STRONG=5, MODERATE=3, WEAK=1
```

### Priority Categories

```text
Priority ≥ 15: CRITICAL priority
Priority 10-14: HIGH priority
Priority 5-9: NORMAL priority
Priority < 5: LOW priority
```

## Input Batch Classification

### Batch Types

Inputs can be batched by classification:

```text
BatchType {
    HOMOGENEOUS_BATCH,    // Same content type, similar complexity
    HETEROGENEOUS_BATCH,  // Mixed content types, similar priority
    PRIORITY_BATCH,       // Same priority level
    SOURCE_BATCH,         // Same source type
    COMPLEXITY_BATCH      // Same complexity level
}
```

### Batch Assembly Rules

#### Rule 1: Homogeneous Batch

```text
IF batch_type == HOMOGENEOUS_BATCH:
    ALL inputs must have same content_type
    Complexity variance must be ≤ 1 level
    Priority variance must be ≤ 1 level
```

#### Rule 2: Priority Batch

```text
IF batch_type == PRIORITY_BATCH:
    ALL inputs must have same priority category
    Source types can be mixed
    Content types can be mixed
```

#### Rule 3: Source Batch

```text
IF batch_type == SOURCE_BATCH:
    ALL inputs must have same source_type
    Content types must be compatible
    Complexity can be mixed
```

## Input Classification Governance

### Classification Responsibilities

1. **Submission**: Input provider classifies input at submission
2. **Review**: Validation reviewer reviews and adjusts classification
3. **Appeal**: Input provider can appeal classification decision
4. **Update**: Classification can be updated based on new information

### Classification Transparency

- Classification criteria must be documented
- Classification decisions must be traceable
- Classification rationale must be recorded
- Classification updates must be version-controlled

### Classification Quality

- Classification must be consistent across similar inputs
- Classification must be evidence-based
- Classification must be reviewable
- Classification must support revision

## Input Classification Examples

### Example 1: Evidence Object from Evidence Layer

```text
Input: Evidence object for forest cover change
Classification:
    source_type: EVIDENCE_LAYER
    content_type: EVIDENCE_OBJECT
    confidence_level: HIGH
    urgency: NORMAL
    complexity: MODERATE
    evidence_weight: STRONG
    traceability_status: FULLY_TRACEABLE
    revision_status: CURRENT
Priority: 3 + 4 + 3 + 5 = 15 (CRITICAL priority)
```

### Example 2: Knowledge Object from Knowledge Runtime

```text
Input: Knowledge object for carbon accounting methodology
Classification:
    source_type: KNOWLEDGE_RUNTIME
    content_type: KNOWLEDGE_OBJECT
    confidence_level: MODERATE
    urgency: LOW
    complexity: MODERATE
    evidence_weight: MODERATE
    traceability_status: PARTIALLY_TRACEABLE
    revision_status: CURRENT
Priority: 2 + 3 + 3 + 3 = 11 (HIGH priority)
```

### Example 3: Observation Record from Observation Layer

```text
Input: Observation record for temperature anomaly
Classification:
    source_type: OBSERVATION_LAYER
    content_type: OBSERVATION_RECORD
    confidence_level: HIGH
    urgency: HIGH
    complexity: SIMPLE
    evidence_weight: STRONG
    traceability_status: FULLY_TRACEABLE
    revision_status: CURRENT
Priority: 4 + 4 + 4 + 5 = 17 (CRITICAL priority)
```

## Status

Documentation foundation only.

No runtime implementation, APIs, automated classification, scoring engine, workflow engine, or automated decisions.
