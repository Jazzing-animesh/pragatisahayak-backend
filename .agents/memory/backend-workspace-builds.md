---
name: Backend workspace builds
description: Build behavior for the mixed Python API and existing frontend mockup workspace.
---

The PragatiSahayak API can be validated independently with the API package's typecheck/build scripts; the root build also reaches the existing mockup artifact, whose Vite build requires a workflow-provided `PORT`.

**Why:** The API workflow supplies its port, but a bare root build does not supply the mockup workflow environment, so an otherwise healthy Flask backend can coexist with a root build failure unrelated to backend code.

**How to apply:** Prefer the API package checks when validating backend changes; treat a root mockup build failure as separate unless the mockup artifact is part of the requested change.