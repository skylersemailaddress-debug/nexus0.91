# AUTOBUILDER TARGET SPEC

This repository is the target repo operated on by Autobuilder.

## Repo roles
- C:\Autobuilder = builder/orchestrator/validator engine
- C:\NEXUS = target application repo

## Hard rules
- No merge between repos
- All generated code/test/workflow changes land in C:\NEXUS only
- Autobuilder is not considered complete when NEXUS is complete
- NEXUS must pass NEXUS-native validation to be considered finished

## Target completion loop
1. Repo audit
2. Gap map
3. Wave plan
4. Patch application
5. Validation
6. Evidence bundle
7. Release gate

## Required artifact roots
- C:\NEXUS\artifacts\autobuilder
- C:\NEXUS\artifacts\rollback
