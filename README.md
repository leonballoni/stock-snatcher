# stock-snatcher
Stock Snatcher é um projeto para capturar dados de API do mercado, combiná-las com raspagem de dados e gerar um serviço para recuperar infos de ações, suas vendas e compras. 

# Objetivos

## Estrutura do projeto

Conceitualmente, o desenvolvimento esperado do projeto seguirá a seguinte estrutura:
1. Serviços localizados na pasta SRC compõem o núcleo de operações
   * snatcher compõe o backend da API 
   * airflow é o serviço de batching para atualizar os stocks do dia.
2. Serviço na pasta INFRA compõem:
    * airflow
    * snatcher
    * redis
    * postgresql

## Inicialização rápida

# Referências


