// Sticky header scrolled state
(() => {
  const header = document.getElementById("siteHeader");
  if (!header) return;
  const onScroll = () => {
    if (window.scrollY > 6) header.classList.add("scrolled");
    else header.classList.remove("scrolled");
  };
  document.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();

// Waitlist form: capture submission, surface confirmation.
// In production, swap to a real endpoint (Mailchimp / ConvertKit / Resend / your own).
(() => {
  const form = document.getElementById("waitlistForm");
  const success = document.getElementById("waitlistSuccess");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const email = (data.get("email") || "").toString().trim();
    const role = (data.get("role") || "").toString().trim();
    if (!email || !email.includes("@") || !role) {
      form.reportValidity?.();
      return;
    }

    // In-memory capture only on this site — swap to a real backend
    // (Mailchimp / ConvertKit / Resend / your own API) before launch.
    window.__estatearms_waitlist = window.__estatearms_waitlist || [];
    window.__estatearms_waitlist.push({ email, role, t: new Date().toISOString() });

    form.hidden = true;
    if (success) success.hidden = false;

    // Hook for future: POST to backend
    // fetch("/api/waitlist", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({ email, role }) });
  });
})();

// Smooth-scroll for in-page anchors with offset for sticky header
document.querySelectorAll('a[href^="#"]').forEach((a) => {
  a.addEventListener("click", (e) => {
    const href = a.getAttribute("href");
    if (!href || href === "#") return;
    const target = document.querySelector(href);
    if (!target) return;
    e.preventDefault();
    const offset = 72;
    const top = target.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top, behavior: "smooth" });
  });
});
