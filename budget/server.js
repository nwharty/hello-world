// Minimal backend for the budgeting app.
//
// It holds the Plaid secret (which must NEVER live in browser code) and
// exposes a few small endpoints the frontend calls:
//
//   POST /api/create_link_token     -> token used to open Plaid Link
//   POST /api/exchange_public_token -> swaps the public_token for an access_token
//   GET  /api/transactions          -> pulls synced transactions for the linked bank
//   GET  /api/status                -> has a bank been linked yet?
//   POST /api/unlink                -> forget the linked bank
//
// The access_token is the long-lived credential for a linked bank. We keep it
// server-side in token.json (gitignored) so it never touches the browser.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import express from 'express';
import dotenv from 'dotenv';
import { Configuration, PlaidApi, PlaidEnvironments, Products, CountryCode } from 'plaid';

dotenv.config();

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TOKEN_FILE = path.join(__dirname, 'token.json');
const PORT = process.env.PORT || 3000;

if (!process.env.PLAID_CLIENT_ID || !process.env.PLAID_SECRET) {
  console.error(
    '\n  Missing Plaid credentials.\n' +
    '  Copy .env.example to .env and fill in PLAID_CLIENT_ID and PLAID_SECRET\n' +
    '  from your Plaid dashboard (https://dashboard.plaid.com).\n'
  );
  process.exit(1);
}

const plaid = new PlaidApi(
  new Configuration({
    basePath: PlaidEnvironments[process.env.PLAID_ENV || 'sandbox'],
    baseOptions: {
      headers: {
        'PLAID-CLIENT-ID': process.env.PLAID_CLIENT_ID,
        'PLAID-SECRET': process.env.PLAID_SECRET,
      },
    },
  })
);

// --- tiny file-based store for the linked bank's access_token + sync cursor ---
function loadStore() {
  try {
    return JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
  } catch {
    return {};
  }
}
function saveStore(data) {
  fs.writeFileSync(TOKEN_FILE, JSON.stringify(data, null, 2));
}

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/status', (req, res) => {
  const store = loadStore();
  res.json({ linked: Boolean(store.access_token) });
});

// Step 1: the frontend asks for a link_token to open Plaid Link.
app.post('/api/create_link_token', async (req, res) => {
  try {
    const response = await plaid.linkTokenCreate({
      user: { client_user_id: 'local-user' },
      client_name: 'My Budget App',
      products: [Products.Transactions],
      country_codes: [CountryCode.Us],
      language: 'en',
    });
    res.json({ link_token: response.data.link_token });
  } catch (err) {
    sendPlaidError(res, err);
  }
});

// Step 2: Link hands back a public_token; swap it for a durable access_token.
app.post('/api/exchange_public_token', async (req, res) => {
  try {
    const { public_token } = req.body;
    const response = await plaid.itemPublicTokenExchange({ public_token });
    saveStore({ access_token: response.data.access_token, cursor: null });
    res.json({ ok: true });
  } catch (err) {
    sendPlaidError(res, err);
  }
});

// Step 3: pull transactions. /transactions/sync is incremental — it returns
// only what changed since the last cursor, so refreshing is cheap.
app.get('/api/transactions', async (req, res) => {
  const store = loadStore();
  if (!store.access_token) {
    return res.status(400).json({ error: 'No bank linked yet.' });
  }
  try {
    let cursor = store.cursor || undefined;
    let added = [];
    let modified = [];
    let removed = [];
    let hasMore = true;

    while (hasMore) {
      const response = await plaid.transactionsSync({
        access_token: store.access_token,
        cursor,
      });
      const data = response.data;
      added = added.concat(data.added);
      modified = modified.concat(data.modified);
      removed = removed.concat(data.removed);
      hasMore = data.has_more;
      cursor = data.next_cursor;
    }

    saveStore({ ...store, cursor });

    // Hand the frontend a trimmed, friendly shape.
    const txns = added.concat(modified).map((t) => ({
      id: t.transaction_id,
      date: t.date,
      name: t.merchant_name || t.name,
      amount: t.amount, // Plaid: positive = money out, negative = money in
      category: (t.personal_finance_category && t.personal_finance_category.primary) ||
        (t.category && t.category[0]) || 'Uncategorized',
    }));

    res.json({ transactions: txns, removed: removed.map((r) => r.transaction_id) });
  } catch (err) {
    sendPlaidError(res, err);
  }
});

app.post('/api/unlink', (req, res) => {
  try {
    fs.unlinkSync(TOKEN_FILE);
  } catch {
    /* already gone */
  }
  res.json({ ok: true });
});

function sendPlaidError(res, err) {
  const data = err.response && err.response.data;
  console.error('Plaid error:', data || err.message);
  res.status(500).json({ error: (data && data.error_message) || err.message });
}

app.listen(PORT, () => {
  console.log(`\n  Budget app running at http://localhost:${PORT}`);
  console.log(`  Plaid environment: ${process.env.PLAID_ENV || 'sandbox'}\n`);
});
