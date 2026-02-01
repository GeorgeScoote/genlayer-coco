#!/bin/bash

echo "🚀 Deploying GenLayer Consensus Challenge..."

# Switch to testnet
echo "📡 Switching to GenLayer Testnet..."
genlayer network testnet-asimov

# Deploy contract
echo "📦 Deploying contract..."
genlayer deploy --contract contracts/consensus_challenge.py

echo "✅ Deployment complete!"
echo "📋 Update .env with the new contract address"
