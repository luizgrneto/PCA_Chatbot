# Agent Template

## Visão Geral

O Agent Template fornece uma forma padrão e escalável para criar agentes de IA que operam em ambientes de produção. É feito para o desenvolvimento e implantação de agentes de IA construídos com o Google ADK (Agent Development Kit).

## Arquitetura

### Estrutura do Projeto

```
agent-template/
├── app/                                     # Aplicação principal dos agente
│   ├── agents/                              # Diretório de agentes
│   │   └── ...
│   │── commons/                             # Módulos compartilhados
│   │   ├── core.py                          # Configurações e utilitários principais
│   │   └── settings.py                      # Configurações globais
│   └── tools/                               # Módulos comportilhados
│   │   └── tools.py                         # Ferramentas compartilhadas
├── pyproject.toml                           # Configuração do projeto Python
├── uv.lock                                  # Lock file de dependências
└── README.md                                # Esta documentação
```

### Recursos Adicionais
- [Google ADK Documentation](https://google.github.io/adk-docs/)
