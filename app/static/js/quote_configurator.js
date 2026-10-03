(() => {
  const root = document.querySelector("[data-configurator]");
  if (!root) return;
  const form = root.querySelector("[data-config-form]");
  const steps = [...root.querySelectorAll("[data-step]")];
  const progress = [...root.querySelectorAll("[data-progress]")];
  const choices = [...root.querySelectorAll("[data-catalog-choice]")];
  let current = 1;

  const money = value => new Intl.NumberFormat("fr-FR", {maximumFractionDigits:0}).format(value) + " FCFA";
  const guests = () => Math.max(0, Number(form.querySelector("[name='guest_count']")?.value || 0));
  const quantityFor = choice => {
    const name = `quantity_${choice.dataset.type.toLowerCase()}_${choice.value}`;
    return Math.max(1, Number(form.querySelector(`[name='${name}']`)?.value || 1));
  };

  const estimate = () => {
    let total = 0, partial = false;
    const lines = [];
    choices.filter(c => c.checked).forEach(choice => {
      const unit = choice.dataset.pricing;
      const price = choice.dataset.price === "" ? null : Number(choice.dataset.price);
      const minimum = Number(choice.dataset.minimum || 0);
      let qty = quantityFor(choice), subtotal = null, warning = "";
      if (minimum && guests() && guests() < minimum) {
        partial = true; warning = `minimum ${minimum} personnes — montant à confirmer`;
      } else if (unit === "ON_REQUEST" || price === null) {
        partial = true; warning = "sur devis";
      } else if (unit === "PER_PERSON") {
        qty = guests(); subtotal = price * qty;
      } else if (unit === "FIXED") {
        qty = 1; subtotal = price;
      } else {
        subtotal = price * qty;
      }
      if (subtotal !== null && Number.isFinite(subtotal)) total += subtotal;
      lines.push({label: choice.dataset.label, subtotal, warning});
    });
    return {total, partial, lines};
  };

  const refreshEstimate = () => {
    const r = estimate();
    root.querySelector("[data-estimate-total]").textContent = !r.lines.length
      ? "Aucune sélection chiffrée"
      : r.partial ? (r.total > 0 ? "Estimation partielle à partir de " + money(r.total) : "Montant à confirmer après étude") : "Environ " + money(r.total);
    const mobileEstimate = root.querySelector("[data-mobile-estimate-total]");
    if (mobileEstimate) mobileEstimate.textContent = root.querySelector("[data-estimate-total]").textContent;
    root.querySelector("[data-estimate-note]").textContent = r.partial
      ? "Certains éléments seront chiffrés après étude de votre demande."
      : "Le montant définitif sera confirmé par WATO EVENTS après étude de votre demande.";
  };

  const value = name => form.querySelector(`[name='${name}']`)?.value?.trim() || "";
  const fillSummary = () => {
    const r = estimate();
    root.querySelector("[data-summary-event]").textContent = value("event_type") || "—";
    root.querySelector("[data-summary-date]").textContent = [value("event_date"), value("event_time"), value("location")].filter(Boolean).join(" · ") || "—";
    root.querySelector("[data-summary-guests]").textContent = value("guest_count") ? value("guest_count") + " personnes" : "—";
    const items = root.querySelector("[data-summary-items]"); items.innerHTML = "";
    if (!r.lines.length) items.textContent = "Aucune offre précise sélectionnée";
    r.lines.forEach(line => { const p = document.createElement("p"); p.textContent = line.label + (line.warning ? " — " + line.warning : line.subtotal !== null ? " — " + money(line.subtotal) : ""); items.appendChild(p); });
    const min=value("budget_min"), max=value("budget_max");
    root.querySelector("[data-summary-budget]").textContent = min||max ? [min?money(Number(min)):"non précisé",max?money(Number(max)):"non précisé"].join(" → ") : "Non précisé";
    root.querySelector("[data-summary-contact]").textContent = [value("customer_name"),value("phone"),value("whatsapp"),value("email")].filter(Boolean).join(" · ") || "—";
    root.querySelector("[data-summary-estimate]").textContent = r.partial ? (r.total > 0 ? "À partir de " + money(r.total) + " + éléments à confirmer" : "À confirmer après étude") : r.lines.length ? money(r.total) : "À confirmer après étude";
  };

  const show = number => {
    current = Math.max(1, Math.min(4, number));
    steps.forEach(step => step.classList.toggle("is-active", Number(step.dataset.step) === current));
    progress.forEach(item => {
      const active = Number(item.dataset.progress) <= current;
      item.classList.toggle("is-active", active);
      if (Number(item.dataset.progress) === current) item.setAttribute("aria-current", "step");
      else item.removeAttribute("aria-current");
    });
    if (current === 4) fillSummary();
    root.scrollIntoView({behavior:"smooth",block:"start"});
  };

  const canContinue = () => {
    const activeStep = steps.find(step => Number(step.dataset.step) === current);
    if (!activeStep) return true;
    const fields = [...activeStep.querySelectorAll("input, select, textarea")].filter(field => !field.disabled && field.type !== "hidden");
    const invalid = fields.find(field => !field.checkValidity());
    if (invalid) {
      invalid.reportValidity();
      invalid.focus();
      return false;
    }
    return true;
  };
  root.querySelectorAll("[data-next]").forEach(b => b.addEventListener("click", () => {
    if (canContinue()) show(current+1);
  }));
  root.querySelectorAll("[data-prev]").forEach(b => b.addEventListener("click", () => show(current-1)));
  choices.forEach(c => c.addEventListener("change", refreshEstimate));
  form.querySelectorAll("input[type='number']").forEach(i => i.addEventListener("input", refreshEstimate));
  form.querySelector("[name='guest_count']")?.addEventListener("input", refreshEstimate);
  form.addEventListener("submit", () => { const b=form.querySelector("[data-submit]"); if(b){b.disabled=true;b.textContent="Envoi en cours…";} });
  refreshEstimate();
})();