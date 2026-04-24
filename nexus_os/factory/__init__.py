from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FactorySpec:
    name: str
    objective: str = ""
    product_type: str = "application"
    data_model: list[str] = field(default_factory=list)
    workflows: list[str] = field(default_factory=list)
    surfaces: list[str] = field(default_factory=list)
    integrations: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    deployment_plan: list[str] = field(default_factory=list)
    risk_controls: list[str] = field(default_factory=list)
    build_phases: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)


DOMAIN_HINTS = {
    "churn": "customer_retention_system",
    "customer": "customer_ops_application",
    "billing": "finance_operations_system",
    "compliance": "governed_workflow_system",
    "spreadsheet": "workflow_automation_app",
    "dashboard": "analytics_dashboard",
    "approval": "approval_workflow_system",
    "market": "market_intelligence_system",
    "portfolio": "portfolio_decision_system",
}


def _norm(text: str) -> str:
    return " ".join(text.lower().split())


def _slug(text: str) -> str:
    return "_".join(part for part in _norm(text).replace("/", " ").split() if part)[:64] or "nexus_app"


def _product_type(text: str) -> str:
    for term, kind in DOMAIN_HINTS.items():
        if term in text:
            return kind
    if "ai" in text or "automation" in text:
        return "ai_workflow_application"
    return "enterprise_application"


def _data_model(text: str) -> list[str]:
    model = ["Project", "User", "Task", "AuditEvent"]
    if "customer" in text or "churn" in text:
        model += ["Customer", "AccountHealth", "RetentionRisk", "Intervention"]
    if "billing" in text or "revenue" in text:
        model += ["Invoice", "Subscription", "PaymentEvent"]
    if "approval" in text or "compliance" in text:
        model += ["ApprovalRequest", "PolicyDecision", "ComplianceEvidence"]
    if "spreadsheet" in text or "workflow" in text:
        model += ["SourceRecord", "TransformationRule", "WorkflowRun"]
    return list(dict.fromkeys(model))


def _workflows(text: str) -> list[str]:
    workflows = [
        "capture_intake",
        "classify_priority_and_risk",
        "generate_recommended_next_action",
        "emit_audit_evidence",
    ]
    if "churn" in text:
        workflows += ["score_churn_risk", "assign_retention_playbook", "track_save_outcome"]
    if "approval" in text or "compliance" in text or "billing" in text:
        workflows += ["request_human_approval", "enforce_policy_gate", "record_compliance_trace"]
    if "dashboard" in text:
        workflows += ["aggregate_metrics", "render_status_dashboard"]
    if "automation" in text or "workflow" in text or "spreadsheet" in text:
        workflows += ["normalize_input", "run_automation", "repair_failed_step"]
    return list(dict.fromkeys(workflows))


def _surfaces(text: str) -> list[str]:
    surfaces = ["mission_control", "work_queue", "proof_panel"]
    if "customer" in text or "churn" in text:
        surfaces += ["account_health_panel", "retention_intervention_panel"]
    if "dashboard" in text:
        surfaces += ["metrics_dashboard"]
    if "approval" in text or "compliance" in text or "billing" in text:
        surfaces += ["approval_console", "audit_timeline"]
    return list(dict.fromkeys(surfaces))


def _integrations(text: str) -> list[str]:
    integrations = ["local_runtime", "file_store", "audit_log"]
    if "spreadsheet" in text:
        integrations.append("spreadsheet_import")
    if "customer" in text or "churn" in text:
        integrations += ["crm", "support_inbox"]
    if "billing" in text:
        integrations.append("billing_provider")
    return list(dict.fromkeys(integrations))


def _risk_controls(text: str) -> list[str]:
    controls = ["structured_logging", "input_validation", "rollback_plan"]
    if any(term in text for term in ["billing", "compliance", "customer", "production"]):
        controls += ["human_approval_required", "policy_gate", "audit_reconstruction"]
    if "customer" in text or "churn" in text:
        controls += ["pii_minimization", "customer_data_access_review"]
    return list(dict.fromkeys(controls))


def build_factory(name: str, objective: str | None = None) -> FactorySpec:
    text = _norm(f"{name} {objective or ''}")
    slug = _slug(name)
    product_type = _product_type(text)
    data_model = _data_model(text)
    workflows = _workflows(text)
    surfaces = _surfaces(text)
    integrations = _integrations(text)
    risk_controls = _risk_controls(text)
    tests = [
        "test_intake_classification_changes_with_input",
        "test_workflow_emits_audit_evidence",
        "test_policy_gate_blocks_risky_action",
        "test_surface_matches_runtime_state",
    ]
    if "churn" in text:
        tests.append("test_churn_score_drives_retention_playbook")
    if "billing" in text or "compliance" in text:
        tests.append("test_approval_required_for_governed_change")
    deployment_plan = [
        "package_application",
        "run_unit_and_scenario_tests",
        "run_security_and_policy_checks",
        "deploy_to_staging",
        "verify_health_and_rollback",
    ]
    build_phases = [
        "phase_1_domain_model_and_intake",
        "phase_2_workflow_engine_and_policy",
        "phase_3_operator_surface_and_evidence",
        "phase_4_tests_deployment_and_monitoring",
    ]
    acceptance = [
        "messy_input_produces_structured_plan",
        "recommended_action_changes_with_input",
        "audit_evidence_generated_for_each_run",
        "risky_actions_are_blocked_or_require_approval",
    ]
    return FactorySpec(
        name=slug,
        objective=objective or name,
        product_type=product_type,
        data_model=data_model,
        workflows=workflows,
        surfaces=surfaces,
        integrations=integrations,
        tests=tests,
        deployment_plan=deployment_plan,
        risk_controls=risk_controls,
        build_phases=build_phases,
        acceptance_criteria=acceptance,
    )


def blueprint_summary(spec: FactorySpec) -> dict[str, int | str]:
    return {
        "name": spec.name,
        "product_type": spec.product_type,
        "models": len(spec.data_model),
        "workflows": len(spec.workflows),
        "surfaces": len(spec.surfaces),
        "tests": len(spec.tests),
        "controls": len(spec.risk_controls),
    }


__all__ = ["FactorySpec", "build_factory", "blueprint_summary"]
