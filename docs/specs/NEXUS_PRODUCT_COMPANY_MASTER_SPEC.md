# NEXUS_PRODUCT_COMPANY_MASTER_SPEC

Status: DRAFT UNTIL IMPLEMENTED

## Invariants
- Nexus must not claim autonomous product-company capability without passing Gate B.
- All product-company actions must be inspectable and attributable.
- Unsafe actions must fail closed.
- Revenue and maintenance burden must be tracked per product.

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
