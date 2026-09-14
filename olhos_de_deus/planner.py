from __future__ import annotations

from .models import Mission, Step


def plan(request: str) -> Mission:
    text = request.strip()
    if not text:
        raise ValueError("Mission request cannot be empty")

    lowered = text.casefold()
    steps = [
        Step("Especificar objetivo", "specify"),
        Step("Planejar execucao", "plan"),
    ]

    code_terms = ("codigo", "código", "repo", "repositorio", "repositório", "bug", "erro", "projeto")
    if any(term in lowered for term in code_terms):
        steps.append(Step("Inspecionar base de codigo", "inspect_code"))

    if any(term in lowered for term in ("android", "celular", "telefone", "app mobile")):
        steps.append(Step("Preparar operacao Android", "android"))
    else:
        steps.append(Step("Implementar mudanca", "implement"))

    steps.append(Step("Verificar resultado", "verify"))
    return Mission(request=text, steps=steps)
