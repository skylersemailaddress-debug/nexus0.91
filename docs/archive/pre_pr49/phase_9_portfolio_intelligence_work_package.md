> Historical archive. This document predates the current evidence-certified release state and is not current launch truth.

# Phase 9 Portfolio Intelligence Work Package

## Objective
Add portfolio intelligence with project registry, scoring, action recommendations, and portfolio actions.

## Required outcomes
- project registry
- project scoring
- recommended action generation
- kill path
- clone path
- bundle path
- portfolio listing and ranking
- reasons and evidence per project

## Implementation tasks
1. Add portfolio intelligence engine.
2. Add create, score, kill, clone, bundle, and list routes.
3. Add scenario and validator.
4. Wire portfolio intelligence into behavioral runtime.

## Validation tasks
- create must return project id
- score must return project score and recommended action
- kill must change status
- clone must create a new project
- bundle must annotate bundled status
- list must return portfolio items

## Blockers
Phase 9 is not complete if actions are decorative or untraceable.
