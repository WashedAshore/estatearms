#!/usr/bin/env python3
"""
Generator for EstateArms content pages.

Static no-build site — but this script lets us keep 9 pages consistent without
hand-duplicating the header/footer. Run it after editing PAGES below; commit
both this script AND the generated .html files.

Usage:
    python3 build_pages.py
"""
from pathlib import Path

ROOT = Path(__file__).parent

# ─── Shared chrome ───
HEADER = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — EstateArms</title>
  <meta name="description" content="{description}" />
  <meta property="og:title" content="{title} — EstateArms" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="article" />
  <link rel="canonical" href="https://estatearms.com/{slug}.html" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css" />
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
</head>
<body>
  <header class="site-header">
    <a href="index.html" class="logo" aria-label="EstateArms home">
      <svg width="28" height="28" viewBox="0 0 32 32" fill="none" aria-hidden="true">
        <rect x="2" y="2" width="28" height="28" rx="3" stroke="currentColor" stroke-width="1.5" />
        <path d="M9 22 L9 10 L16 16 L23 10 L23 22" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none" />
        <circle cx="16" cy="22" r="1.2" fill="currentColor" />
      </svg>
      <span>EstateArms</span>
    </a>
    <nav class="site-nav" aria-label="Primary">
      <a href="appraisal.html">Appraisal</a>
      <a href="nfa.html">NFA</a>
      <a href="executors.html">Executors</a>
      <a href="about.html">About</a>
    </nav>
    <a href="https://app.estatearms.com/#/auth" class="btn btn-primary btn-sm">Start free</a>
  </header>

  <main>
    <section class="article-hero">
{deco_block}
      <div class="container">
        <div class="crumb">{crumb}</div>
        <h1>{h1}</h1>
        <p class="lede">{lede}</p>
      </div>
    </section>

    <section class="article-body">
      <div class="container">
"""

FOOTER = """      </div>
    </section>

    <section class="article-cta">
      <div class="container">
        <h3>Start cataloging the estate.</h3>
        <p>Free tier handles your first 25 items. Upgrade only when you outgrow it. No card required.</p>
        <a href="https://app.estatearms.com/#/auth" class="btn btn-primary">Create your account</a>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <div class="footer-logo">
          <svg width="22" height="22" viewBox="0 0 32 32" fill="none" aria-hidden="true">
            <rect x="2" y="2" width="28" height="28" rx="3" stroke="currentColor" stroke-width="1.5" />
            <path d="M9 22 L9 10 L16 16 L23 10 L23 22" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none" />
            <circle cx="16" cy="22" r="1.2" fill="currentColor" />
          </svg>
          <span>EstateArms</span>
        </div>
        <p>Probate-grade inventory for collectible &amp; NFA estates.</p>
      </div>
      <div>
        <h4>Services</h4>
        <a href="appraisal.html">Appraisal</a>
        <a href="nfa.html">NFA transfer</a>
        <a href="inventory.html">Probate inventory</a>
        <a href="comparables.html">Comparable sales</a>
        <a href="catalog.html">Digital catalog</a>
      </div>
      <div>
        <h4>Guides</h4>
        <a href="executors.html">For executors</a>
        <a href="nfa-probate.html">NFA in probate</a>
        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
      </div>
      <div>
        <h4>App</h4>
        <a href="https://app.estatearms.com/#/auth">Sign in</a>
        <a href="https://app.estatearms.com/#/auth">Create account</a>
        <a href="/#pricing">Pricing</a>
      </div>
    </div>
    <div class="container footer-bottom">
      <span>© 2026 EstateArms. All rights reserved.</span>
      <span>EstateArms is software and documentation support. It is not legal, tax, or appraisal advice.</span>
    </div>
  </footer>
</body>
</html>
"""


def page(slug, title, crumb, h1, description, lede, body, decorations=None):
    """Assemble one HTML file from chrome + body.
    `decorations` is a list of (image_filename, variant_class) tuples."""
    deco_block = ""
    if decorations:
        lines = []
        for img, variant in decorations:
            lines.append(
                f'      <img src="{img}" alt="" aria-hidden="true" '
                f'class="page-deco page-deco--{variant}" />'
            )
        deco_block = "\n".join(lines)
    html = (
        HEADER.format(
            slug=slug, title=title, crumb=crumb, h1=h1,
            description=description, lede=lede,
            deco_block=deco_block,
        )
        + body.strip() + "\n"
        + FOOTER
    )
    out = ROOT / f"{slug}.html"
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.name} ({len(html):,} bytes)")


# ─── Content ───

PAGES = []

PAGES.append(dict(
    slug="appraisal",
    title="Estate Firearm Appraisal",
    crumb="Service · Appraisal",
    h1="Fair-market appraisal for estate firearms.",
    description="Estate firearm appraisal for probate, insurance, and estate-tax purposes. Comparable-sales valuation including NFA items. Florida-based, remote nationwide.",
    lede="When a firearm collection enters probate, the court needs a number. We give you the right number — defensible, comparable-sales-backed, and properly itemized for Schedule A.",
    body="""
<h2>Why estate firearms need a specialist appraisal</h2>
<p>A generic personal-property appraiser will read a serial number and look up a blue-book value. That works for a Glock 19. It does not work for a 1929 Springfield Armory Model 1922 M2, a transferable Pre-86 dealer sample, a Singer-marked 1911A1, or any of the hundred small variants that move a $900 rifle into the $9,000 bracket.</p>

<p>EstateArms appraisals are produced by an active executor and NFA correspondent who has personally identified, valued, and transferred firearms inside probate. Every appraisal is tied to documented comparable sales — not a single online quote, not a vague "auction estimate." Court personnel, beneficiaries, and the IRS all want the same thing: a number with paper behind it.</p>

<h2>What an EstateArms appraisal includes</h2>
<ul>
  <li><strong>Per-item identification</strong> with rare-variant detection — we assume rare variant first, standard issue last, so anomalies are not missed.</li>
  <li><strong>Fair-market value (FMV)</strong> for each item, anchored to comparable-sales research from auction houses, RIA, Rock Island, GunBroker historical, and recognized NFA dealer networks.</li>
  <li><strong>High-end realized potential</strong> alongside FMV, so the executor sees both the conservative number for the court and the upside if the heirs choose to consign.</li>
  <li><strong>Condition documentation</strong> with photos: bore, action, finish, markings, accessories, original box and paperwork (or absence thereof).</li>
  <li><strong>NFA status</strong> when applicable — registry confirmation, tax-stamp tracking, and Form 4 / Form 5 path identification.</li>
  <li><strong>Court-ready output:</strong> a single PDF that drops directly into Schedule A of the inventory filing, with the appraiser's signature, methodology page, and source-list appendix.</li>
</ul>

<h2>What we appraise</h2>
<h3>Complete firearms</h3>
<p>Modern pistols and revolvers, sporting rifles and shotguns, military surplus, collectible long guns, Class III / NFA items including suppressors, SBRs, SBSs, machine guns, AOWs, and DDs.</p>

<h3>Firearm parts and accessories</h3>
<p>Slides, barrels, frames, receivers, triggers, stocks, grips, handguards, optics, magazines, and individual NFA components like silencers separated from a host firearm. Parts are often the most-mis-valued items in an estate.</p>

<h3>Anomalies and contract markings</h3>
<p>Military contract markings, factory variants, low-production runs, prototype features, mismatched-but-correct serials, refurbishment stamps, and other collector-grade anomalies that change valuation by an order of magnitude.</p>

<h2>How the engagement works</h2>
<ol>
  <li><strong>Intake.</strong> You send us photos and any paperwork the decedent kept. We confirm scope, fee, and turnaround in writing.</li>
  <li><strong>Identification &amp; condition.</strong> We work item-by-item, assuming rare variant until disproven. Anything we cannot confirm from photos is flagged for in-person inspection.</li>
  <li><strong>Comparables research.</strong> Each item is anchored to at least three recent comparable sales. NFA items are anchored to dealer-network and registry-tracked sales.</li>
  <li><strong>Deliverable.</strong> A PDF appraisal report, plus the full inventory loaded into a digital catalog in your EstateArms account that you can hand to a buyer, an auction house, or the heirs.</li>
</ol>

<h2>Fees</h2>
<p>Hourly for small estates, capped per-item for medium estates, flat-fee for large estates. We will quote in writing after intake. We do not work on commission — that creates a conflict of interest between the appraiser and the heirs.</p>

<div class="callout">
  <span class="label">Compliance</span>
  <p>EstateArms provides valuation, documentation, and correspondence support. It is not a law firm and does not provide legal advice. NFA transfers must comply with current ATF rules and the state law of the heir's domicile.</p>
</div>

<div class="next-reading">
  <h3>Related</h3>
  <ul>
    <li><a href="comparables.html">How we source comparable sales</a></li>
    <li><a href="nfa.html">NFA transfer and correspondence</a></li>
    <li><a href="executors.html">Executor's guide to estate firearms</a></li>
  </ul>
</div>
""",
    decorations=[("schematic-pistol.png", "primary"), ("schematic-revolver.png", "secondary")],
))

PAGES.append(dict(
    slug="nfa",
    title="NFA Transfer & Correspondence",
    crumb="Service · NFA",
    h1="NFA estate transfers, end to end.",
    description="ATF Form 5 tax-exempt heir transfer and Form 4 transfer guidance for suppressors, SBRs, SBSs, machine guns, AOWs, and DDs in probate. Correspondence handled by an active NFA correspondent.",
    lede="When the decedent owned an NFA item, the estate has a fuse on it. Lawful possession during administration is a federal question, the heir transfer paperwork is unforgiving, and the ATF response time is measured in months — not days.",
    body="""
<h2>The NFA-in-estate problem in two paragraphs</h2>
<p>An NFA-registered item — a suppressor, a short-barreled rifle (SBR), a short-barreled shotgun (SBS), a machine gun, an Any Other Weapon (AOW), or a Destructive Device (DD) — is registered to an individual or a trust. When the registrant dies, the item does not pass like ordinary chattel. The executor or successor trustee holds it in a constructive-possession capacity during settlement, and the only lawful path to an heir is an ATF-approved transfer.</p>

<p>If the heir is a lawful U.S. person, an <strong>ATF Form 5</strong> tax-exempt transfer is typically the right vehicle. If the item is going to a non-heir purchaser, it is an <strong>ATF Form 4</strong> transfer with a $200 tax stamp. The wrong form, the wrong signatures, the wrong CLEO notification, or the wrong shipping arrangement turns a routine settlement into a federal felony exposure.</p>

<h2>What EstateArms handles</h2>
<ul>
  <li><strong>Inventory and confirmation</strong> of every NFA item the decedent owned, cross-referenced against the National Firearms Registration and Transfer Record where available.</li>
  <li><strong>Constructive-possession guidance</strong> for the executor or trustee during the open estate, including secure-storage standards and who in the household can and cannot have access.</li>
  <li><strong>Form 5 preparation</strong> for tax-exempt heir transfers: heir identification, photographs, fingerprint cards, CLEO notification, and Responsible Person Questionnaire (where applicable for trusts).</li>
  <li><strong>Form 4 preparation</strong> when the destination is a non-heir buyer (auction, dealer consignment, or arms-length sale by the estate).</li>
  <li><strong>Correspondence handling</strong> with the NFA Branch: response to Requests for Information (RFI), corrections, refiling, and status tracking through pending / approved.</li>
  <li><strong>Trust-administration support</strong> when the item is titled to a gun trust: amending the trust to reflect successor trustees, identifying Responsible Persons, and ensuring the trust survives the settlor.</li>
</ul>

<h2>Form 5 vs. Form 4: the practical distinction</h2>
<h3>Form 5 — tax-exempt heir transfer</h3>
<p>Used when an NFA item passes from the estate to a lawful heir. No $200 tax stamp. The heir must be a person who could lawfully possess the item (not a prohibited person, not a resident of a state that bans the specific item). Approval times have ranged from a few weeks to a year depending on backlog. Until approved, the heir cannot take possession — the executor holds the item.</p>

<h3>Form 4 — taxable transfer to a non-heir</h3>
<p>Used when the estate sells, auctions, or otherwise transfers an NFA item to someone who is not an heir. $200 tax stamp applies. Same lawful-possessor checks apply to the buyer. Often used when no heir wants the item and the estate liquidates it.</p>

<div class="callout">
  <span class="label">Critical timing</span>
  <p>The estate may legally hold the item indefinitely during open administration. Do not rush to transfer until the form is approved. Premature delivery of an NFA item to a beneficiary — even a clearly-named heir in the will — before ATF approval is a federal violation by both the executor and the heir.</p>
</div>

<h2>What we do not do</h2>
<p>EstateArms is not a law firm and does not provide legal advice. We do not appear before the ATF on your behalf — but we draft the paperwork, track the timeline, and handle the correspondence so your attorney's billable hours stay focused on the legal issues that actually require an attorney.</p>

<div class="next-reading">
  <h3>Related</h3>
  <ul>
    <li><a href="nfa-probate.html">NFA items in probate — full guide</a></li>
    <li><a href="executors.html">Executor's guide to estate firearms</a></li>
    <li><a href="appraisal.html">Estate firearm appraisal</a></li>
  </ul>
</div>
""",
    decorations=[("schematic-thompson.png", "primary"), ("schematic-suppressor.png", "secondary"), ("schematic-form4.png", "form")],
))

PAGES.append(dict(
    slug="inventory",
    title="Probate Firearm Inventory",
    crumb="Service · Inventory",
    h1="Itemized inventory built for the court.",
    description="Per-item probate inventory of estate firearms with make, model, serial, condition, photos, NFA status, and FMV — formatted for Schedule A.",
    lede="A probate inventory is not a spreadsheet of guns. It is a sworn filing the court reads, the heirs scrutinize, and the IRS can audit five years later. Build it the way the people who will read it expect to see it.",
    body="""
<h2>What goes into a court-ready firearm inventory</h2>
<p>Florida Probate Rule 5.340 (and its equivalents in every state) requires the personal representative to file a verified inventory of estate assets within 60 days of issuance of letters. For firearms — especially collectible, antique, and NFA-regulated items — the inventory needs to do four things at once: identify the item unambiguously, value it defensibly, document its condition contemporaneously, and flag any legal-transfer constraints.</p>

<h2>Per-item required fields</h2>
<ul>
  <li><strong>Make and model</strong> — manufacturer and model designation as marked on the receiver, not as colloquially called.</li>
  <li><strong>Serial number</strong> — exactly as stamped, including any prefix letters and slash characters.</li>
  <li><strong>Caliber / gauge</strong> — as marked, with any second caliber if dual-marked.</li>
  <li><strong>Barrel length</strong> — measured, not assumed. Critical for NFA classification.</li>
  <li><strong>Variant / configuration</strong> — military contract, factory variant, refurbishment marks, sporterized status.</li>
  <li><strong>Condition</strong> — using NRA or auction-grade descriptors (Excellent / Very Good / Good / Fair / Poor), with notes on bore, action, finish, and originality.</li>
  <li><strong>Accessories included</strong> — original box, paperwork, magazines, optics, cases — listed as part of the item, since they affect value.</li>
  <li><strong>NFA registration status</strong> when applicable — registry confirmation, tax-stamp number, and transferee tracking.</li>
  <li><strong>Photos</strong> — minimum: full-length both sides, action open, receiver markings, serial number, bore. Photos are the asset's contemporaneous condition record.</li>
  <li><strong>Fair-market value (FMV)</strong> with the source of valuation cited in an appendix.</li>
  <li><strong>Acquisition basis</strong> when known — needed for the heirs' step-up-in-basis calculation later.</li>
</ul>

<h2>Why a generic inventory fails</h2>
<p>The most common error in firearm probate inventories is treating a collection as a single line item — "Firearms collection, estimated value $40,000." The court accepts it because it does not know better. The heirs accept it because they do not know better. Then five years later one heir sues another over a missing $18,000 Colt Python, and there is no contemporaneous record of whether that Python ever existed in the estate at all.</p>

<p>An EstateArms inventory makes each item independently verifiable. If a Colt Python was in the estate, there is a photograph of its serial number, a condition note, an FMV, and a distribution entry. If it was not, the record shows that too.</p>

<h2>NFA-specific inventory requirements</h2>
<p>NFA items get an additional row of fields: registration status, registry-tracked tax stamp number, current location and storage standard, lawful-possessor status of the constructive holder during administration, and the destination heir or buyer with the form (4 or 5) selected. The inventory becomes the working document for the NFA correspondence that follows.</p>

<h2>How the inventory gets built</h2>
<ol>
  <li><strong>Photo intake.</strong> Photograph every item per the field list above. We provide a one-page intake checklist.</li>
  <li><strong>Identification pass.</strong> Each item is identified, rare-variant assessed, NFA status confirmed.</li>
  <li><strong>Valuation pass.</strong> FMV assigned, comparable sales cited.</li>
  <li><strong>Court formatting.</strong> Schedule A export from EstateArms with appraiser certification page.</li>
  <li><strong>Distribution-plan integration.</strong> Same inventory feeds the distribution plan, the NFA transfer paperwork, and any auction consignment.</li>
</ol>

<div class="next-reading">
  <h3>Related</h3>
  <ul>
    <li><a href="catalog.html">Digital cataloging system</a></li>
    <li><a href="appraisal.html">Estate firearm appraisal</a></li>
    <li><a href="comparables.html">Comparable sales research</a></li>
  </ul>
</div>
""",
    decorations=[("schematic-garand.png", "primary"), ("schematic-shotgun.png", "secondary")],
))

PAGES.append(dict(
    slug="comparables",
    title="Comparable Sales Research",
    crumb="Service · Comparables",
    h1="Valuation backed by real sold prices.",
    description="Comparable-sales research for estate firearms — auction-house records, NFA dealer networks, GunBroker historical, and recognized collectible-firearm sources. Defensible methodology for probate and estate-tax purposes.",
    lede="Asking prices on listing sites are noise. Sold prices, in the right grade, within the right time window, are signal. We work in signal.",
    body="""
<h2>Why \"comparable sales\" is the only valuation methodology that holds up</h2>
<p>The IRS, the probate court, and any thoughtful heir will all ask the same question of an appraisal number: <em>how do you know?</em> The defensible answer is a list of recently sold comparable items — same make, same model, same configuration, same condition grade, sold in an arms-length transaction within a recent window. Anything else is opinion.</p>

<p>Estate firearm valuation is harder than ordinary collectibles because the comparables pool is smaller, NFA items have a regulatory layer that affects price, and condition grade swings value by 3–10x. A well-built comparables file shows the work.</p>

<h2>Sources we use</h2>
<h3>Auction-house records</h3>
<p>Rock Island Auction, Morphy's, James D. Julia, Heritage, Bonhams, and regional firearm auction houses publish realized prices. These are the gold standard — vetted descriptions, photographed condition, arms-length bidders, and a publicly recorded hammer price plus buyer's premium.</p>

<h3>Dealer-network sales</h3>
<p>For NFA items in particular, the recognized dealer network publishes asking and sold prices for transferable machine guns, registered suppressors, and other Class III items. These prices are the working market.</p>

<h3>GunBroker historical and similar venues</h3>
<p>Sold-listing data from major retail venues, filtered for arms-length completion (not bid-and-cancel, not relisted), gives a broad market floor.</p>

<h3>Specialist collector communities</h3>
<p>For obscure items — pre-WWI European service rifles, low-production run variants, contract-marked military arms — collector forums and references like the Italian weapons taxonomy at <a href="https://forum.enlisted.net/t/an-ultimate-italian-weapons-recollection/142899">forum.enlisted.net</a> are sometimes the only place a definitive identification exists.</p>

<h2>What a comparables file looks like</h2>
<p>Per appraised item, we deliver:</p>
<ul>
  <li>At least three comparables when the market supports it; more for high-value items.</li>
  <li>Each comparable: source, date of sale, hammer price (or sold price), condition grade as described, and a one-sentence note on any divergence from the appraised item.</li>
  <li>A single resolved FMV figure with a brief written rationale.</li>
  <li>For high-volatility items: a high-end realized potential alongside FMV, with the upside comparable cited separately.</li>
</ul>

<div class="callout">
  <span class="label">What we exclude</span>
  <p>Listed-but-unsold asking prices. Single-data-point sales from venues with poor description quality. Sales more than ~24 months old in volatile categories. Insurance-replacement quotes (these are not FMV — they are retail-replacement, which runs 30–50% higher).</p>
</div>

<h2>When the comparables are thin</h2>
<p>Some items are genuinely rare — a one-of-twelve experimental, an unmarked prototype, an item where the most recent public sale is five years stale. When that happens, the appraisal says so explicitly. We do not invent a precise FMV for an item that the market has not priced. We give the court a range with the methodology disclosed.</p>

<div class="next-reading">
  <h3>Related</h3>
  <ul>
    <li><a href="appraisal.html">Estate firearm appraisal</a></li>
    <li><a href="inventory.html">Probate firearm inventory</a></li>
    <li><a href="catalog.html">Digital cataloging system</a></li>
  </ul>
</div>
""",
    decorations=[("schematic-shotgun.png", "primary"), ("schematic-revolver.png", "secondary")],
))

PAGES.append(dict(
    slug="catalog",
    title="Digital Cataloging System",
    crumb="Service · Catalog",
    h1="A real database for the collection.",
    description="Photo-documented, database-backed firearm inventory built for executors, collectors, and FFLs. Per-estate isolation, AI-assisted identification, NFA tracking, court-ready PDF export.",
    lede="Spreadsheets work until they do not. A 200-item estate with photos, NFA paperwork, beneficiary assignments, and an active distribution plan needs a database — and an interface a non-engineer can actually use.",
    body="""
<h2>What the cataloging system does</h2>
<p>The EstateArms catalog is a multi-tenant web application built specifically for the inventory needs of estate firearms, collectible firearms, vehicles, coins, and high-value chattels. It was first built to solve the founder's own estate. It now runs the same way for any executor, NFA trustee, FFL, or probate attorney who needs the same toolset.</p>

<h2>Core features</h2>
<ul>
  <li><strong>Per-estate isolation.</strong> Each estate is its own logical database, so a probate attorney managing five concurrent estates never cross-contaminates the records.</li>
  <li><strong>Photo upload and storage.</strong> Drop in serial-number, full-length, and detail photos. The photo is part of the contemporaneous condition record.</li>
  <li><strong>AI-assisted identification.</strong> Upload a photo, get an identification with rare-variant detection and a dual FMV / high-end valuation. Assume rare variant first, standard issue last.</li>
  <li><strong>NFA tracking.</strong> Tax-stamp number, transfer date, transferee, Form 4 / Form 5 status, registry confirmation.</li>
  <li><strong>Beneficiary &amp; distribution tracking.</strong> Assign each item to an heir, track distribution status, log the actual transfer date.</li>
  <li><strong>Activity log.</strong> Every change is timestamped and attributed. The court accepts an audit trail that the heirs cannot.</li>
  <li><strong>Court-ready PDF report.</strong> One click → a Schedule-A-formatted inventory with appraiser certification, methodology page, and source-list appendix. White-label-able on the Professional and Firm tiers.</li>
  <li><strong>Team seats.</strong> Invite your attorney, your appraiser, your co-executor, or a co-trustee with role-based access (owner / admin / member / viewer).</li>
  <li><strong>Data export.</strong> Full inventory, photos, and activity log exportable as CSV and ZIP. No lock-in.</li>
</ul>

<h2>Asset categories beyond firearms</h2>
<p>The estate is rarely only firearms. The catalog also handles collectible vehicles, numismatics (coins and currency), general high-value chattels, and real property. Each category has its own field schema and its own valuation source.</p>

<h2>How it differs from generic probate software</h2>
<p>Generic probate inventory tools treat a $48,000 transferable machine gun the same as a kitchen appliance. There is no NFA tax-stamp field, no Form 5 transferee tracking, no rare-variant detection, no chain-of-custody for items the court will scrutinize. EstateArms was built by an executor who hit those gaps personally on a real estate.</p>

<h2>Pricing</h2>
<p>Free tier covers the first 25 items and one estate — enough to evaluate the system on a small estate. Paid tiers scale by estate count, seats, and white-label branding. See the <a href="/#pricing">pricing page</a> for current rates.</p>

<div class="next-reading">
  <h3>Related</h3>
  <ul>
    <li><a href="inventory.html">Probate firearm inventory</a></li>
    <li><a href="appraisal.html">Estate firearm appraisal</a></li>
    <li><a href="executors.html">Executor's guide to estate firearms</a></li>
  </ul>
</div>
""",
    decorations=[("schematic-ar15.png", "primary"), ("schematic-rifle.png", "secondary")],
))

PAGES.append(dict(
    slug="executors",
    title="Executor's Guide to Estate Firearms",
    crumb="Guide · For Executors",
    h1="What an executor must do with the firearms.",
    description="Practical guide for executors, personal representatives, and successor trustees handling firearms in an estate — including NFA items. Custody, valuation, lawful transfer, and documentation, in order.",
    lede="The first day you accept appointment as executor of an estate containing firearms, you become legally responsible for them. Here is the order of operations.",
    body="""
<h2>The first 72 hours</h2>
<p>Before anything else: <strong>secure the firearms</strong>. Take possession of the keys to every safe, drawer, and storage location. If household members remain in the residence and any of them is a prohibited person — a felon, a domestic-violence misdemeanant, an unlawful drug user, a person subject to a restraining order, an undocumented person, or any other category in 18 U.S.C. § 922(g) — you must move the firearms to a location where they cannot access them. Constructive possession by a prohibited person is a federal felony, and the executor's failure to act on a known risk is a fiduciary breach.</p>

<p>Take this seriously even when it is awkward. Especially when it is awkward.</p>

<h2>Inventory before anything moves</h2>
<p>Do not let an item leave the estate's possession before it is photographed, logged, and counted. Every executor who has ever skipped this step regrets it. The most common loss in a firearms estate is not theft — it is a beneficiary "borrowing" a rifle to clean it and never giving it back, with no record that the rifle ever existed in the inventory.</p>

<p>See the <a href="inventory.html">probate firearm inventory</a> page for the per-item field list. Photos are non-negotiable.</p>

<h2>Identify the NFA items</h2>
<p>Walk the inventory and flag every item that is or might be NFA-regulated: suppressors, short-barreled rifles (any rifle with a barrel under 16"), short-barreled shotguns (any shotgun with a barrel under 18"), machine guns of any vintage (yes, including the Thompson the grandfather brought home from the war), AOWs, and DDs.</p>

<p>For each flagged item, locate the tax stamp paperwork in the decedent's records. If you cannot find the paperwork, do not assume the item is unregistered — that is a federal felony to possess. The ATF maintains a registry; the path to confirmation runs through your attorney or an NFA correspondent. See <a href="nfa-probate.html">NFA items in probate</a> for the procedural detail.</p>

<h2>Get a defensible valuation</h2>
<p>You will be asked, by the court and probably by the IRS, what the firearms were worth on the date of death. A defensible answer requires a comparable-sales appraisal — not a blue-book number and not a beneficiary's opinion. See <a href="appraisal.html">estate firearm appraisal</a>.</p>

<h2>File the inventory</h2>
<p>Florida personal representatives file a verified inventory within 60 days of issuance of letters. Other states have similar deadlines. The firearms section of the inventory must be itemized, valued, and (for NFA items) flagged with current registration status.</p>

<h2>Handle distributions correctly</h2>
<h3>Ordinary firearms</h3>
<p>Distribute according to the will. If the will is silent, follow the state's residuary distribution rules. Confirm each recipient is a lawful possessor under federal and recipient-state law. <strong>Do not deliver to a prohibited person, even if they are the named beneficiary.</strong> Convert the bequest to its cash equivalent or distribute to an alternate per the will's gap-filler language.</p>

<h3>NFA items</h3>
<p>Different rules. NFA items cannot be physically transferred to the heir until the ATF approves the Form 5. Hold the item under constructive possession until approval. Then, and only then, transfer.</p>

<h3>If the heir does not want the item</h3>
<p>Sell it. Either through a dealer consignment, an auction house, or a direct sale to a lawful buyer. For NFA items, the sale is a Form 4 transaction with a $200 tax stamp paid by the buyer. The estate gets the proceeds; they go into the residue.</p>

<h2>Document everything</h2>
<p>Every conversation with a beneficiary about a firearm, every transfer, every appraisal source, every NFA correspondence — log it. The activity log is the executor's protection if the distribution is ever challenged.</p>

<div class="callout">
  <span class="label">When to call a lawyer</span>
  <p>Any beneficiary dispute over a firearm. Any prohibited-person issue with a named beneficiary. Any uncertainty about NFA registration status. Any out-of-state distribution where the destination state's firearm law differs from yours. These are not DIY situations.</p>
</div>

<div class="next-reading">
  <h3>Related</h3>
  <ul>
    <li><a href="nfa-probate.html">NFA items in probate</a></li>
    <li><a href="inventory.html">Probate firearm inventory</a></li>
    <li><a href="nfa.html">NFA transfer and correspondence</a></li>
  </ul>
</div>
""",
    decorations=[("schematic-form5.png", "form"), ("schematic-revolver.png", "primary")],
))

PAGES.append(dict(
    slug="nfa-probate",
    title="NFA Items in Probate",
    crumb="Guide · NFA in Probate",
    h1="How NFA items pass through an estate.",
    description="How NFA-regulated firearms pass to heirs, lawful possession during settlement, ATF Form 5 tax-exempt heir transfer, and the procedural requirements at each stage of probate.",
    lede="The National Firearms Act predates the modern probate code and was not drafted with estate administration in mind. The result is a procedural maze the executor must walk through carefully — but it is walkable.",
    body="""
<h2>The legal frame</h2>
<p>An NFA-regulated item — a registered suppressor, an SBR, an SBS, a machine gun, an AOW, or a DD — is registered to a specific person or trust in the National Firearms Registration and Transfer Record (NFRTR). When the registrant dies, the registration does not transfer automatically. The estate holds the item in a <strong>constructive possession</strong> capacity, and the only lawful path to an heir runs through an ATF-approved transfer.</p>

<h2>Constructive possession during administration</h2>
<p>The executor or successor trustee may lawfully hold the item during open administration without filing a transfer. There is no statutory deadline on how long the estate may hold the item — settlement can take months or years, especially in a litigated estate, and the ATF accepts that.</p>

<p>However, the constructive possessor must be a lawful person to possess. If the named executor is a prohibited person, that person cannot serve as constructive possessor of NFA items even though they are the executor. A co-executor, a special administrator, or a successor must hold the item. This is a place to involve counsel early.</p>

<h3>Storage standards during administration</h3>
<p>The item must be stored in a manner consistent with the executor's lawful possession — typically locked, separated from access by prohibited household members, and inventoried. Some states have specific safe-storage statutes; the executor must comply with the more restrictive of federal and state law.</p>

<h2>Transfer to a lawful heir — ATF Form 5</h2>
<p>The Form 5 (Application for Tax Exempt Transfer and Registration of Firearm) is the vehicle for transferring an NFA item from the estate to a lawful heir. It is tax-exempt — no $200 stamp. It is not, however, automatic. The heir must be:</p>
<ul>
  <li>A U.S. person (citizen or lawful permanent resident).</li>
  <li>Not a prohibited person under 18 U.S.C. § 922(g).</li>
  <li>A resident of a state where the specific NFA item type is lawful to possess (some states ban machine guns, some ban SBRs, some ban suppressors).</li>
  <li>For an heir under 21, additional restrictions may apply depending on item type.</li>
</ul>

<h3>What Form 5 requires</h3>
<ul>
  <li>The executor's signature and capacity (a copy of the letters of administration).</li>
  <li>The heir's identifying information, photographs, and fingerprint cards.</li>
  <li>Chief Law Enforcement Officer (CLEO) notification — a copy of the form sent to the CLEO in the heir's jurisdiction.</li>
  <li>For trust-owned items: amended trust documentation reflecting successor trustees and Responsible Persons.</li>
  <li>The original registration document or its known data (registry-tracked).</li>
</ul>

<h3>Approval timeline</h3>
<p>Historically, Form 5 approvals have ranged from a few weeks to over a year. The estate holds the item until approval; the heir cannot take physical possession before then, even informally, even briefly. Premature delivery is a federal violation by both parties.</p>

<h2>Transfer to a non-heir — ATF Form 4</h2>
<p>When no heir wants the item, or when the heir is unable to lawfully possess it, the estate may sell. The vehicle is the Form 4 (Application for Tax Paid Transfer and Registration of Firearm). $200 tax stamp paid by the buyer. Same lawful-possessor checks apply. The estate receives the proceeds.</p>

<p>Many NFA items have substantial value as collectibles — transferable Pre-86 machine guns in particular have appreciated dramatically. An auction-house consignment is often the best vehicle for maximizing value while documenting an arms-length sale for the inventory record.</p>

<h2>Trust-owned NFA items</h2>
<p>NFA items registered to a gun trust pass through the trust's terms, not the will. The successor trustee named in the trust assumes administration. The trust survives the settlor's death if drafted correctly; if not drafted correctly, the items may need to be transferred out of the trust to individual heirs via Form 5.</p>

<p>This is where trust drafting quality matters enormously. A well-drafted NFA trust names a successor trustee, identifies Responsible Persons, and provides a clear disposition mechanism. A poorly-drafted trust forces the estate into an expensive cleanup.</p>

<div class="callout">
  <span class="label">Common errors</span>
  <p>Delivering an NFA item to a beneficiary before Form 5 approval. Allowing a prohibited household member access to a stored NFA item. Failing to notify the CLEO when required. Filing a Form 5 with the executor's personal signature rather than as executor with letters attached. Selling an NFA item informally (no Form 4) to "settle" the estate quickly.</p>
</div>

<div class="next-reading">
  <h3>Related</h3>
  <ul>
    <li><a href="nfa.html">NFA transfer and correspondence service</a></li>
    <li><a href="executors.html">Executor's guide to estate firearms</a></li>
    <li><a href="appraisal.html">Estate firearm appraisal</a></li>
  </ul>
</div>
""",
    decorations=[("schematic-form5.png", "form"), ("schematic-thompson.png", "primary"), ("schematic-suppressor.png", "secondary")],
))

PAGES.append(dict(
    slug="contact",
    title="Contact",
    crumb="Contact",
    h1="Request an appraisal, inventory, or NFA consultation.",
    description="Contact EstateArms for estate firearm appraisal, probate inventory, NFA transfer correspondence, or comparable-sales research. Florida-based, remote nationwide.",
    lede="Tell us what the estate looks like and what you need. We respond within one business day.",
    body="""
<h2>Direct contact</h2>
<p>Email: <a href="mailto:craig@estatearms.com">craig@estatearms.com</a></p>
<p>Service area: Florida primary, with remote consultation available nationwide. NFA correspondence handled regardless of estate location.</p>

<h2>Request form</h2>
<form class="contact-form" action="mailto:craig@estatearms.com" method="post" enctype="text/plain">
  <label>
    Your name
    <input type="text" name="name" required autocomplete="name" />
  </label>
  <label>
    Email
    <input type="email" name="email" required autocomplete="email" placeholder="you@firm.com" />
  </label>
  <label>
    Your role
    <select name="role" required>
      <option value="" disabled selected>Choose one…</option>
      <option value="executor">Executor / Personal Representative</option>
      <option value="trustee">Successor Trustee / NFA Trustee</option>
      <option value="attorney">Probate / Estate Attorney</option>
      <option value="ffl">FFL / Estate Liquidator</option>
      <option value="heir">Heir or Beneficiary</option>
      <option value="other">Other</option>
    </select>
  </label>
  <label>
    What do you need?
    <select name="need" required>
      <option value="" disabled selected>Choose one…</option>
      <option value="appraisal">Estate firearm appraisal</option>
      <option value="inventory">Probate inventory</option>
      <option value="nfa">NFA transfer / correspondence</option>
      <option value="comparables">Comparable sales research</option>
      <option value="catalog">Digital cataloging system</option>
      <option value="consult">General consultation</option>
    </select>
  </label>
  <label>
    Estate state
    <input type="text" name="state" placeholder="e.g. FL" maxlength="2" />
  </label>
  <label>
    Approximate item count
    <input type="text" name="count" placeholder="e.g. 25, 200, unknown" />
  </label>
  <label>
    Briefly describe the situation
    <textarea name="message" required placeholder="What does the collection look like? Are there NFA items? What's the timeline?"></textarea>
  </label>
  <button type="submit" class="btn btn-primary">Send request</button>
</form>

<div class="callout">
  <span class="label">Privacy</span>
  <p>Contact submissions are read only by the founder. Nothing is shared, sold, or used for marketing. If you prefer, email directly using the address above.</p>
</div>
""",
    decorations=[("schematic-pistol.png", "secondary")],
))

PAGES.append(dict(
    slug="about",
    title="About EstateArms",
    crumb="About",
    h1="Built by an executor, for executors.",
    description="EstateArms was built by an active estate executor, NFA correspondent, durable power of attorney holder, and software engineer. Every feature first solved a real problem the founder hit while administering an estate of this kind.",
    lede="EstateArms is not the work of a software team that read about probate. It is the work of someone who is currently doing it.",
    body="""
<h2>Who built this</h2>
<p>EstateArms is built and operated by Craig Oefinger out of Brandon, Florida. The founder is concurrently:</p>
<ul>
  <li>Active estate executor on a multi-asset estate including 200+ firearms and NFA items;</li>
  <li>NFA correspondent handling Form 4 and Form 5 transfers;</li>
  <li>Durable Power of Attorney holder for estate-adjacent property matters;</li>
  <li>Property manager;</li>
  <li>Software engineer (JavaScript, Python, SQL).</li>
</ul>

<p>Every feature in the EstateArms platform was first a problem the founder personally hit while administering an estate of this kind. The rare-variant-first identification logic, the Form 5 tracking, the per-estate isolation, the activity log, the court-ready PDF formatting — all of it is the result of an executor needing the tool and writing it because nothing existing did the job.</p>

<h2>Service area</h2>
<p>Primary: Florida. The founder is based in Brandon (Hillsborough County) and works regularly with probate proceedings statewide. Remote consultation is available nationwide for appraisal, comparable-sales research, NFA correspondence, and use of the digital catalog. On-site inspection within Florida; photo-based assessment outside Florida.</p>

<h2>Approach</h2>
<h3>Accuracy first</h3>
<p>An estate firearm is a financial instrument with a regulatory layer. Getting the identification, the valuation, or the transfer paperwork wrong has consequences — for the executor's liability, the heirs' inheritance, and federal compliance. We work with the assumption that every item could be a rare variant, every NFA item could have an irregular registration, and every distribution will be scrutinized by someone.</p>

<h3>Documentation that holds up</h3>
<p>Court personnel, IRS auditors, insurance adjusters, and downstream heirs all read the same documents. We produce documents that read correctly to all of them.</p>

<h3>Software that respects the operator</h3>
<p>The catalog is a real database, not a glorified spreadsheet. It exports everything you put into it as CSV and ZIP — no lock-in. The activity log is timestamped and immutable. The white-label PDF format is professional enough to send to a probate court without further editing.</p>

<h2>What EstateArms is not</h2>
<p>EstateArms is not a law firm. We do not provide legal advice. We do not appear before the ATF on your behalf. We do not give tax advice. For all of those, work with appropriate counsel and a qualified accountant — and we will hand them clean documents to work from.</p>

<h2>Credentials and references</h2>
<p>Available on request via the <a href="contact.html">contact form</a>. We are happy to provide professional references to other executors, probate attorneys, and estate professionals considering engagement.</p>

<div class="next-reading">
  <h3>Get started</h3>
  <ul>
    <li><a href="contact.html">Contact for engagement</a></li>
    <li><a href="https://app.estatearms.com/#/auth">Create a free account in the catalog</a></li>
    <li><a href="executors.html">Executor's guide to estate firearms</a></li>
  </ul>
</div>
""",
    decorations=[("schematic-rifle.png", "primary")],
))

# ─── Build all ───
print(f"Generating {len(PAGES)} pages...")
for p in PAGES:
    page(**p)
print(f"Done. {len(PAGES)} HTML files in {ROOT}/")
