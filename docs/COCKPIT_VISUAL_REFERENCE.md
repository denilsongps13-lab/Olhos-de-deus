# Cockpit visual reference

A tela principal do Olho de Deus segue o Modelo 2 — Cockpit aprovado pelo usuário: HUD escuro/ciano, barra lateral com identidade visual, faixa superior de status, banner de rede global, Comando Central, Resposta/Execução grande e sempre visível e Painel de Operações à direita.

A implementação não deve simular integrações ou agentes: o visual pode ser rico, mas os estados exibidos precisam refletir o controller/adapters reais.

A partir da v0.7.1, os elementos gráficos principais são renderizados nativamente em Qt:

- olho digital HUD na marca e na área de execução;
- globo/rede global no banner superior;
- chips de status, barras de progresso e cards de operação;
- painel lateral com Ruflo, Swarm, agentes e as sete integrações reais;
- abas de Histórico, Logs, Resultados, Arquivos e Atividade dos Agentes.

Isso mantém o instalador autocontido e evita depender de imagens externas para compor o visual do cockpit.
