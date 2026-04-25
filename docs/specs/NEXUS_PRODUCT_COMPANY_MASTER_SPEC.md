# NEXUS_PRODUCT_COMPANY_MASTER_SPEC

Status: BOUNDED ROADMAP / NOT CURRENT AUTONOMOUS PRODUCT-COMPANY CLAIM

## Current interpretation

This document is an implementation roadmap for product-company capability. It is not current release evidence and does not authorize a claim that Nexus can autonomously operate a complete product company.

Current launch truth is governed by `docs/release/CURRENT_STATUS.md`, current CI, `scripts/run_enterprise_gate.py`, validator outputs, and final certification evidence.

## Invariants

- Nexus must not claim autonomous product-company capability without passing the applicable product-company gate.
- All product-company actions must be inspectable and attributable.
- Unsafe actions must fail closed.
- Revenue and maintenance burden must be tracked per product.
- Product-company claims must remain bounded until runtime behavior, tests, and evidence prove the capability.

## Required packages

- nexus_os/models/product.py
- nexus_os/models/opportunity.py
- nexus_os/models/portfolio.py
- nexus_os/models/economics.py
- nexus_os/market_intelligence/
- nexus_os/portfolio/
- nexus_os/factory/
- nexus_os/surface_fabric/
- nexus_os/distribution/
- nexus_os/economics/
- nexus_os/fleet_maintenance/
- nexus_os/autonomy_policy/
- nexus_os/customer_ops/
- nexus_os/benchmarking/

## Required operator projections

- nexus_os/operator/portfolio_projection.py
- nexus_os/operator/market_projection.py
- nexus_os/operator/product_fleet_projection.py
- nexus_os/operator/economics_projection.py

## Cleanup note

This file remains active because it defines bounded future capability and safety invariants. It has been reworded to remove stale draft-status language and align with the evidence-certified release posture.
