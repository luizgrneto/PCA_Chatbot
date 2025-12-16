# Introdução

Este é um protótipo do projeto de final de curso da pós-graduação em Processamento de Linguagem Natural, da Universidade Federal de Goiás. Consiste em dois blocos principais: 
- Template do Agente, baseado no Google ADK.
- Notebooks de estudo onde foi feita a criação da Vector Store e as análises de métricas da RAG.

# Instalação
1. Crie uma conta no [Ollama](`https://ollama.com/`).
2. Baixe e instale o Ollama. Siga as instruções do site sobre como baixar localmente os modelos disponíveis.
3. Crie um novo ambiente através do comando `make create-env`.
4. Instale todas as dependências através do comando `uv sync`.
5. (Opcional) Use o comando `make run` para rodar uma instância local do agente.

# Template do Agente

## Visão Geral

O Agent Template fornece uma forma padrão para criar agentes de IA. É feito para o desenvolvimento e implantação de agentes construídos com o Google ADK (Agent Development Kit).

## Arquitetura

### Estrutura do Template
```
agent-pca/
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

# Notebooks e frameworks de evaluation 

## Objetivos
- O notebook [Vector_Store.ipynb](Vector_Store.ipynb) faz do zero toda a etapa de criação, chunks, embeddings e ingest de documentos na Vector Store, baseada em ChromaDB.
- O notebook [eval_metrics.ipynb](eval_metrics.ipynb) automatiza a avaliação de datasets RAG (retrieval + generation) usando o vector store local e o DeepEval para métricas de LLM (context precision, context relevancy, answer relevancy e faithfulness).

## Principais blocos / funções
- Vector Store: instancia o store via [`HybridVectorStore`](src/vectorstore/hybrid_vector_store.py) usando as configurações em [`settings`](src/config/settings.py).
- Pipeline de RAG:
  - [`rag_pipeline`](eval_metrics.ipynb): realiza busca híbrida (retrieval) e gera resposta com o LLM escolhido (Ollama).
  - [`real_retrieval`](eval_metrics.ipynb): retorna apenas os textos recuperados (contexto) para inspeção.
- Geração de datasets:
  - [`generate_dataset_for_evaluation`](eval_metrics.ipynb): percorre o CSV de ground truth e salva um JSON por modelo contendo input do usuário, resposta esperada, resposta gerada pela LLM e contexto recuperado da Store.
- Avaliação com DeepEval:
  - [`run_evaluation_on_datasets`](eval_metrics.ipynb): carrega o JSON de test_cases, cria `LLMTestCase` e calcula métricas usando funções internas.


## Evaluation da RAG e da geração de respostas 
1. Execute um servidor Ollama local (ou ajuste `base_url`) e garanta modelos disponíveis.
2. (Opcional) Rode todas as células de [Vector_Store.ipynb](Vector_Store.ipynb) para criar a Vector Store pela primeira vez. Atenção para as variáveis em [`settings`](src/config/settings.py).
3. Abra [eval_metrics.ipynb](eval_metrics.ipynb) no Jupyter/VSCode e execute as células em ordem:
   - Instanciar `HybridVectorStore` (usa [`settings`](src/config/settings.py)).
   - Gerar datasets (opcional): use `generate_dataset_for_evaluation`.
   - Rodar avaliação: executar `run_evaluation_on_datasets`. Atenção para a estrutura de pastas em [`artifacts`](artifacts/)
4. A saída das métricas é escrita de volta no JSON do dataset e pode ser salva separadamente.

### Datasets e resultados
- Podem ser encontrados separados por modelo avaliador e conversacional em: artifacts/eval_metrics/ (ex.: artifacts/eval_metrics/datasets/ e artifacts/eval_metrics/deepeval/context/)