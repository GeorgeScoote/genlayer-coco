# GenLayer Consensus Challenge

A decentralized word-matching game built on GenLayer blockchain with AI-powered semantic analysis.

![GenLayer](https://img.shields.io/badge/GenLayer-Testnet-purple.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black.svg)

## 🚀 Vercel Deployment (Recommended)

### Method 1: One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

1. Click the button above
2. Import your GitHub repository
3. Click "Deploy" - Done!

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Method 3: Manual Deploy

1. Push this code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Deploy (no configuration needed!)

---

## 🔧 CORS Fix Explained

**Problem:** When deployed to Vercel, the browser blocks requests to `https://studio.genlayer.com/api` due to CORS policy.

**Solution:** This project includes a serverless API proxy (`api/rpc.js`) that forwards requests to GenLayer RPC from the server side, bypassing CORS restrictions.

```
Browser → /api/rpc (Vercel Serverless) → GenLayer RPC
```

---

## 📁 Project Structure

```
├── index.html        # Main frontend (complete single-page app)
├── api/
│   └── rpc.js        # ⭐ Serverless proxy for GenLayer RPC (CORS fix)
├── vercel.json       # Vercel configuration
├── package.json      # Project metadata
├── contracts/        # Smart contract source code
└── docs/             # Documentation
```

---

## ⚙️ How It Works

| Component | Purpose |
|-----------|---------|
| `index.html` | Complete game UI with MetaMask integration |
| `api/rpc.js` | Serverless proxy that forwards RPC calls to GenLayer |
| `vercel.json` | Configures routing and CORS headers |

### Request Flow

1. **Local Development:** Frontend → GenLayer RPC (direct)
2. **Vercel Production:** Frontend → `/api/rpc` → GenLayer RPC (proxied)

The frontend automatically detects the environment and uses the appropriate endpoint.

---

## 🎮 Game Rules

| Step | Action | Reward |
|------|--------|--------|
| 1 | Connect MetaMask wallet | - |
| 2 | Submit a blockchain keyword | - |
| 3 | Wait for 2-10 players | - |
| 4 | AI analyzes semantic similarity | - |
| 5 | Match bonus (same word) | +50 XP |
| 6 | Winner (most matches) | +100 XP |
| 7 | Participation | +20 XP |

---

## 🔗 Contract Info

| Field | Value |
|-------|-------|
| Address | `0x8443995060C9dd4bBE97A9e7e39F4E73c43cCb19` |
| Network | GenLayer Testnet |
| Chain ID | 61983 (0xf21f) |
| RPC URL | https://studio.genlayer.com/api |

---

## 💻 Local Development

```bash
# Option 1: Using serve
npx serve .

# Option 2: Using Python
python -m http.server 8000

# Open http://localhost:3000 or http://localhost:8000
```

**Note:** Local development connects directly to GenLayer RPC without the proxy.

---

## 📝 Contract API

### Write Methods

| Method | Parameters | Description |
|--------|------------|-------------|
| `submit_word` | `word: str` | Submit keyword to current game |

### View Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_leaderboard` | `dict` | All players' XP |
| `get_game_status` | `str` | Current game words |
| `get_history` | `list` | Recent game history |

---

## 🛠️ Troubleshooting

### "Failed to fetch" error on Vercel

1. Check if `api/rpc.js` file exists
2. Verify `vercel.json` configuration
3. Redeploy the project

### MetaMask not connecting

1. Make sure MetaMask is installed
2. Switch to GenLayer Testnet network
3. Refresh the page

### Transaction fails

1. Check if you have GEN tokens for gas
2. Verify you're on the correct network
3. Try refreshing and reconnecting wallet

---

## 📚 Resources

- [GenLayer Documentation](https://docs.genlayer.com)
- [GenLayer Studio](https://studio.genlayer.com)
- [Vercel Documentation](https://vercel.com/docs)

---

## 📜 License

MIT License - see [LICENSE](LICENSE)
