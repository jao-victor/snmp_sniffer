# SNMP Sniffer 🕵️‍♂️📡

O **SNMP Sniffer** é uma ferramenta de auditoria de rede desenvolvida para analistas de segurança e infraestrutura. Seu objetivo é identificar rapidamente dispositivos em uma rede que possuam comunidades SNMP específicas configuradas (ideal para detectar se a comunidade `public` está exposta).

A ferramenta combina a velocidade de um **Ping Sweep** assíncrono com a biblioteca SNMP para validar as configurações de segurança de forma eficiente.

## 🚀 Funcionalidades

- **Ping Sweep Integrado:** Filtra automaticamente apenas os hosts ativos antes de iniciar o scan SNMP, economizando tempo e recursos.
- **Processamento Assíncrono:** Utiliza `asyncio` para realizar múltiplas verificações simultaneamente, permitindo escanear redes inteiras (`/24`, `/22`, etc) em segundos.
- **Controle de Concorrência:** Implementa um semáforo para limitar o número de tarefas simultâneas, evitando gargalos de rede ou bloqueios de firewall.
- **Relatório de Erros:** Identifica se a falha foi por Timeout (dispositivo inacessível) ou por Erro de Autenticação (Comunidade incorreta).

## 📋 Pré-requisitos

- Python 3.7 ou superior.
- **Permissões de Administrador:** O script utiliza a biblioteca `icmplib`, que requer privilégios elevados para enviar pacotes ICMP (RAW Sockets).
  - No Windows: Execute o Terminal/PowerShell como Administrador.
  - No Linux: Utilize `sudo`.

## 🛠️ Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/snmp_sniffer.git
   cd snmp_sniffer
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Como Usar

Para iniciar o scan, execute o script principal:

```bash
python snmp_sniffer.py
```

### Exemplo de interação:
1. **Rede:** Digite o range no formato CIDR (ex: `192.168.1.0/24`).
2. **Community:** Digite a comunidade SNMP que deseja testar (ex: `public`, `private`).

### Saída esperada:
```text
Realizando ping sweep...
64 hosts ativos encontrados

Iniciando verificação SNMP...

192.168.1.1 -> SNMP OK
192.168.1.10 -> SNMP FAIL (AUTH/COMMUNITY ERROR)
192.168.1.15 -> SNMP OK

Tempo total: 3.12 segundos
```

## 📂 Estrutura do Projeto

- `snmp_sniffer.py`: Script principal de alta performance (Async).
- `requirements.txt`: Lista de dependências.

## ⚠️ Aviso Legal

Este script foi criado para fins legítimos de auditoria e segurança. O autor não se responsabiliza pelo uso indevido da ferramenta em redes para as quais você não possui autorização explícita de teste.

---
**Desenvolvido para fortalecer a segurança de redes.** 🛡️⚡
