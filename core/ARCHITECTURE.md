# Núcleo — Olhos de Deus

## Pipeline alvo

`request → orchestrate → specify → plan → inspect-context → route-agent → execute → verify → report`

## Componentes

### Orchestrator
Coordena a missão, mantém estado e delega para módulos especializados.

### Specification Engine
Transforma pedidos em requisitos, plano e tarefas verificáveis antes de mudanças grandes.

### Knowledge Graph
Indexa estrutura, relações, dependências e caminhos do código. Deve ser utilizável antes de abrir arquivos aleatórios em bases grandes.

### Agent Router
Escolhe um agente especializado por capacidade e escopo. Agentes têm permissões mínimas e contratos claros de entrada/saída.

### Workflow Engine
Representa tarefas como nós e dependências, permite reexecução parcial e registra estado de cada etapa.

### Guardian QA
Executa gates de testes, regressão, segurança, qualidade e readiness. Falha de gate retorna a tarefa para correção.

### Mobile Operator
Módulo opcional para automação/teste Android autorizado, com observação, ação, evidência, logs e recuperação.

### Output Adapter
Produz resposta operacional: próxima ação primeiro, passos curtos quando necessários, estado explícito e sem esconder o resultado principal.

## Princípios

- Mega Cérebro original é somente leitura até a fase futura de cópia e integração.
- Nada é considerado pronto sem verificação.
- Falhas devem ser registradas e recuperáveis.
- Cada agente recebe somente as ferramentas necessárias.
- Integrações externas devem ser desacopladas por adapters.
- Código GPL do ComfyUI não entra no núcleo por simples cópia; inicialmente usamos seus padrões como referência arquitetural.
