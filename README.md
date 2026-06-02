# EstateArms — Marketing Site

Marketing & pricing landing page for **EstateArms**, the first inventory and probate-administration system built for estates containing collectible firearms, NFA items, vehicles, and high-value chattels.

**Live preview**: deployed via Perplexity Computer. To deploy your own, see "Deploy" below.

---

## What this is

A single-page static landing site (HTML + CSS + vanilla JS, zero framework, zero build step) used to validate market demand and capture the founding waitlist for EstateArms.

Pages:
- Hero with positioning statement
- The problem (why generic probate tools fail firearm estates)
- Feature highlights
- Audience cards (executors / FFLs & trustees / probate firms)
- 4-tier pricing + one-time lifetime option
- Founder quote
- FAQ
- Waitlist form

## Pricing model

| Tier | Price | Target |
|---|---|---|
| Free | $0 | Lead capture / small estates |
| Executor | $29/mo or $290/yr | Individual executors |
| Professional | $99/mo or $990/yr | FFLs & NFA trustees |
| Firm | $299/mo or $2,990/yr | Probate law firms |
| Single-Estate License | $499 one-time | Executors of exactly one estate |

## File structure

```
estatearms-site/
├── index.html      Full markup (single page)
├── styles.css      Tokens, layout, components, responsive
├── app.js          Sticky header, waitlist form, smooth scroll
├── favicon.svg     Brand mark
└── README.md
```

## Local preview

```bash
cd estatearms-site
python3 -m http.server 8765
# open http://localhost:8765
```

Or any static server: `npx serve`, `caddy file-server`, Nginx, etc.

## Deploy

Pure static site — host anywhere:

- **GitHub Pages**: enable Pages on the repo, point at `main` branch root
- **Vercel / Netlify**: drag-and-drop the folder, or connect this repo
- **Cloudflare Pages**: connect the repo, no build command, output dir = `/`
- **S3 + CloudFront**: `aws s3 sync . s3://your-bucket/`

The form posts to `window.__estatearms_waitlist` in memory only — before launch, replace the form handler in `app.js` with a POST to your real backend (Mailchimp, ConvertKit, Resend, Postmark, or an internal API).

## Design notes

- **Palette**: warm parchment background (`#f7f4ee`), deep navy near-black ink (`#0e1622`), aged-brass accent (`#8a6a2a`), walnut/burgundy secondary (`#6b3a2c`)
- **Typography**: Source Serif 4 for display, Inter for body, JetBrains Mono for technical labels
- **Aesthetic**: institutional / probate-grade / editorial — trust signals for attorneys, FFLs, and serious executors. Not "AI startup" or "consumer SaaS."

## Roadmap (Phase 2)

After validating demand:
1. Fork the Oefinger inventory app codebase into a clean SaaS product repo
2. Add user accounts, organization / multi-tenancy, Stripe billing, feature gates per tier
3. Build self-hosted single-estate installer for the $499 one-time license
4. White-label branding for Professional / Firm tiers
5. Direct ATF Form 5 e-filing integration

## License

MIT — landing copy and code free to fork. Brand name "EstateArms" reserved.
