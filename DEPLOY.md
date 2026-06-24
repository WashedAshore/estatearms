# Deploy `estatearms.com` (Cloudflare Pages + Squarespace DNS)

The marketing site (this repo) deploys to **Cloudflare Pages** — free,
auto-SSL, global CDN, deploys on every git push.

The SaaS app at `estatearms-app` deploys to **Railway** at the
`app.estatearms.com` subdomain.

Total time: ~15 minutes.

---

## 1. Cloudflare Pages setup

1. Sign in at [cloudflare.com](https://dash.cloudflare.com). Create a free
   account if you don't have one.
2. Left sidebar → **Workers & Pages → Create application → Pages →
   Connect to Git**.
3. Authorize Cloudflare to access your GitHub. Select
   `WashedAshore/estatearms`.
4. Build settings:
   - **Project name:** `estatearms`
   - **Production branch:** `main`
   - **Framework preset:** None
   - **Build command:** *(leave empty — static HTML)*
   - **Build output directory:** `/`
5. **Save and Deploy.** First build runs ~30 seconds, then the site is live at
   `https://estatearms.pages.dev`.

Open it. Click around. Verify the 9 content pages render. Verify
`https://estatearms.pages.dev/llms.txt` and `/robots.txt` return the right text.

---

## 2. Custom domain — `estatearms.com` apex

1. In the Cloudflare Pages project → **Custom domains → Set up a custom
   domain → enter `estatearms.com`.**
2. Cloudflare will ask whether the domain is already on Cloudflare. It is
   not — your registrar is Squarespace.
3. Cloudflare shows you the DNS record it needs. For a Pages project, the
   apex setup is a single **CNAME** to `estatearms.pages.dev`.

### Set the DNS records at Squarespace

1. Sign in at [account.squarespace.com/domains](https://account.squarespace.com/domains).
2. Click **`estatearms.com` → DNS Settings → DNS** (under Advanced Settings).
3. Scroll to **Custom Records → Add Record.**

> **Squarespace does not support ALIAS/ANAME or CNAME-at-apex.**
> Pages requires either an apex CNAME or you must transfer the DNS to
> Cloudflare. We do the second — it's the recommended path and unlocks
> Cloudflare's other features.

#### Easiest path — move DNS to Cloudflare (recommended, 5 min)

1. Cloudflare dashboard → **Add a Site → enter `estatearms.com`.** Free plan.
2. Cloudflare scans existing records and gives you two **nameservers** that
   look like `xxx.ns.cloudflare.com`.
3. Back in Squarespace → Domains → `estatearms.com` → **Nameservers** →
   **Use custom nameservers** → paste in the two Cloudflare nameservers →
   **Save.**
4. Wait 5–60 minutes for nameserver propagation. Cloudflare will email
   you when active.
5. Once Cloudflare is the DNS authority, the Pages custom-domain setup
   completes automatically — apex CNAME is created, TLS cert is issued.

#### Alternative — keep DNS at Squarespace

If you really want to stay on Squarespace DNS, you cannot point the apex
at Cloudflare Pages. Two options:
- Point apex `A` record at one of Cloudflare's anycast IPs and serve the
  page through a Worker (advanced, not recommended)
- Use only `www.estatearms.com` and 301 the apex elsewhere (suboptimal SEO)

The Cloudflare-DNS path is dramatically simpler. Use it.

---

## 3. `www.estatearms.com`

Once Cloudflare is the DNS authority:

1. Cloudflare Pages → Custom domains → **Set up a custom domain →
   `www.estatearms.com`**.
2. Cloudflare auto-creates the CNAME and issues the cert.
3. Pages will redirect `www → apex` (or vice versa) per the project's
   redirect setting — toggle whichever direction you prefer.

---

## 4. `app.estatearms.com` (the SaaS app)

The Railway-hosted app needs its own subdomain.

1. Railway service → Settings → Networking → **+ Custom Domain →
   `app.estatearms.com`.**
2. Railway gives you a CNAME target like `<service>.up.railway.app`.
3. Cloudflare dashboard → **DNS → Records → Add record.**
   - **Type:** CNAME
   - **Name:** `app`
   - **Target:** `<service>.up.railway.app`
   - **Proxy status:** **DNS only** (gray cloud). Required so Railway can
     issue its own Let's Encrypt cert. Do NOT use Cloudflare's orange-cloud
     proxy here — it conflicts with Railway's cert issuance.
4. Wait 5–10 minutes. Railway shows "Active" on the custom domain.
5. `https://app.estatearms.com/api/health` should return `{"status":"ok"}`.

---

## 5. Verify

Once everything is propagated:

```bash
# From the estatearms-app repo
npm run preflight -- --domain=estatearms.com
```

The validator now checks both `estatearms.com` (marketing) and
`app.estatearms.com` (app). Required checks should all pass.

Spot checks:

| URL | Expected |
|---|---|
| `https://estatearms.com` | Marketing landing page |
| `https://estatearms.com/appraisal` | Appraisal content page |
| `https://estatearms.com/llms.txt` | The llms.txt content |
| `https://estatearms.com/robots.txt` | `User-agent: *` |
| `https://estatearms.com/sitemap.xml` | XML sitemap |
| `https://www.estatearms.com` | Redirects to apex (or serves same content) |
| `https://app.estatearms.com` | EstateArms app login |
| `https://app.estatearms.com/api/health` | `{"status":"ok"}` |

---

## 6. Iterating on content

Marketing site changes:
```bash
git checkout main
# edit / add content
python3 build_pages.py     # if you changed PAGES in the script
git add -A && git commit -m "..."
git push origin main
# Cloudflare Pages auto-builds in ~30 seconds
```

The app and marketing site now deploy independently. You can ship copy
changes 50 times a day without touching the app, and ship app changes
without redeploying the marketing site.

---

## 7. Cost

- **Cloudflare Pages:** $0 (free tier covers up to 500 builds/month and
  unlimited bandwidth)
- **Cloudflare DNS:** $0 (free)
- **Railway (the app):** ~$5/month
- **Squarespace domain renewal:** ~$20/year
- **Total monthly:** ~$5

---

## 8. Optional: submit the sitemap to Google

Once `estatearms.com` is live:

1. [Google Search Console](https://search.google.com/search-console) →
   Add property → `estatearms.com`
2. Verify via DNS TXT record (Cloudflare → DNS → Add record)
3. Sitemaps → **Add a new sitemap → `sitemap.xml`** → Submit
4. Indexing usually completes within a week
