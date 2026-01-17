# Deployment Guide

## Prerequisites

1. Install GenLayer CLI
```bash
npm install -g genlayer
```

2. Configure wallet
```bash
genlayer config set private_key YOUR_PRIVATE_KEY
```

3. Get testnet tokens
```bash
curl -X POST https://genlayer-faucet.vercel.app/api/faucet \
  -H 'Content-Type: application/json' \
  -d '{"address": "YOUR_ADDRESS", "network": "Genlayer Testnet", "token": "GEN"}'
```

---

## Deploy Contract

### Option 1: Using Script

```bash
npm run deploy
```

### Option 2: Manual

```bash
genlayer network testnet-asimov
genlayer deploy --contract contracts/consensus_challenge.py
```

---

## Verify Deployment

1. Note the contract address from deployment output
2. Update `.env` with new address
3. Test via GenLayer Studio: https://studio.genlayer.com

---

## Frontend Deployment

### Local
```bash
npm run dev
# Open http://localhost:3000
```

### Production (Vercel/Netlify)

1. Connect repository
2. Set build directory: `frontend/public`
3. Deploy

---

## Network Configuration

| Parameter | Value |
|-----------|-------|
| Chain ID | 61999 (0xF21F) |
| RPC URL | https://studio.genlayer.com/api |
| Currency | GEN |
| Explorer | https://studio.genlayer.com |

### MetaMask Setup

Network will be auto-added when user connects. Manual config:

```
Network Name: GenLayer Testnet
RPC URL: https://studio.genlayer.com/api
Chain ID: 61999
Currency: GEN
```
