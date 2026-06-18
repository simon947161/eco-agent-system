# Green Power Classification Agent Purpose

## Purpose

The Green Power Classification Agent is intended to organise evidence about
how electricity consumption may be attributed to green electricity. It
provides a common vocabulary and review structure before information is used
in later CarbonOS workflows.

The agent provides classification support only. It does not determine legal
eligibility, regulatory compliance, certificate validity, carbon emissions,
or environmental performance.

## Objectives

- distinguish physical, trading, allocation, and unknown attribution pathways;
- connect each proposed classification to traceable supporting evidence;
- preserve reporting periods, quantities, ownership, boundaries, and methods;
- expose missing, inconsistent, expired, or uncertain evidence;
- produce human-readable classification and review records; and
- provide a governed input concept for future CarbonOS agents.

## Expected Users

| User | Expected use |
| --- | --- |
| Organisations | Organise electricity evidence across reporting boundaries |
| Industrial Facilities | Describe site-level consumption and supply pathways |
| Energy Managers | Review contracts, meters, certificates, and allocations |
| ESG Teams | Prepare traceable evidence summaries for internal review |
| Future ClimateOS Scenarios | Use bounded, explicitly assumed classification inputs |
| Human Reviewers | Check evidence, uncertainty, limitations, and proposed status |

## Use Cases

### On-site generation

Organise meter, asset, ownership, and consumption-period evidence for
electricity generated and consumed at a facility.

### Contracted electricity

Record the contract, supplier, delivery period, consumption, attribute
language, and supporting evidence for human classification review.

### Certificate-supported attribution

Connect electricity consumption to certificate or transaction records while
checking ownership, quantity, period, geography, retirement, and possible
double counting.

### Internal allocation

Record how an organisation allocates shared or portfolio-level electricity
attributes to facilities, products, departments, or reporting units.

### Evidence triage

Identify records that remain `Unknown` or `Needs Review` because evidence is
missing, inconsistent, out of period, untraceable, or outside the declared
method.

## Boundaries

No runtime fields or executable behavior are implemented in Task51. The
foundation does not calculate emissions, certify green electricity, approve
claims, interpret law, access external systems, or recommend transactions.
