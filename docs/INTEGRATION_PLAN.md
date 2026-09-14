# Olhos de Deus — Integration Plan

## Goal
Build a unified architecture from compatible concepts in the seven upstream projects without blindly merging unrelated codebases.

## Layers
1. core — orchestration, model routing, state and execution contracts.
2. agents — specialized agent definitions and coordination.
3. skills — reusable capabilities and QA checks.
4. workflows — declarative and visual workflow definitions.
5. sources — upstream provenance, licenses and integration notes.

## Integration order
1. Inventory upstream licenses and architecture.
2. Extract reusable interfaces and patterns.
3. Implement a native Olhos de Deus core.
4. Add specialized agents and skills.
5. Add workflow orchestration and visual concepts.
6. Add automated QA gates.
7. Test integrations independently before enabling them together.

## Rule
Never copy third-party source into the native core without confirming its license and retaining required notices.
