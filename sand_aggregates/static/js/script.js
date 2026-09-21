/* =========================================================
   Apex Sand & Aggregates — Interactive Client Script
   Preserves original mobile menu, scroll reveal & enquiry links
   Adds live price computation for the ordering system
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  initScrollReveal();
  initEnquireButtons();
  initOrderCalculator();
  initAlertDismissal();
});

/* ---------- Mobile navigation ---------- */
function initNav() {
  const toggle = document.getElementById("nav-toggle");
  const nav = document.getElementById("main-nav");
  if (!toggle || !nav) return;

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  // Close menu after tapping a link (mobile)
  nav.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });

  // Close when clicking outside
  document.addEventListener("click", (e) => {
    if (!nav.contains(e.target) && !toggle.contains(e.target) && nav.classList.contains("open")) {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    }
  });
}

/* ---------- Product "Enquire Now" -> pre-fill form ---------- */
function initEnquireButtons() {
  const productSelect = document.getElementById("f-product");
  document.querySelectorAll(".enquire-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const card = btn.closest(".product-card");
      const productName = card ? card.dataset.product : "";
      if (productSelect && productName) {
        setSelectValue(productSelect, productName);
      }
      const enquirySection = document.getElementById("enquiry");
      if (enquirySection) {
        enquirySection.scrollIntoView({ behavior: "smooth", block: "start" });
        const nameField = document.getElementById("f-name");
        if (nameField) window.setTimeout(() => nameField.focus(), 450);
      }
    });
  });
}

function setSelectValue(selectEl, value) {
  const match = Array.from(selectEl.options).find(opt => 
    opt.value === value || opt.text.trim().toLowerCase().includes(value.trim().toLowerCase())
  );
  if (match) {
    selectEl.value = match.value;
  }
}

/* ---------- Interactive Order Form Price & Total Calculator ---------- */
function initOrderCalculator() {
  const productSelect = document.getElementById("order-product-select");
  const quantityInput = document.getElementById("order-quantity-input");
  const unitPriceDisplay = document.getElementById("order-unit-price-display");
  const quantityDisplay = document.getElementById("order-quantity-display");
  const totalAmountDisplay = document.getElementById("order-total-amount-display");
  const unitDisplay = document.getElementById("order-unit-display");

  if (!productSelect || !quantityInput) return;

  function recalculate() {
    const selectedOption = productSelect.options[productSelect.selectedIndex];
    if (!selectedOption || !selectedOption.value) {
      if (unitPriceDisplay) unitPriceDisplay.textContent = "₹0.00";
      if (quantityDisplay) quantityDisplay.textContent = "0";
      if (totalAmountDisplay) totalAmountDisplay.textContent = "₹0.00";
      return;
    }

    const price = parseFloat(selectedOption.getAttribute("data-price") || 0);
    const unit = selectedOption.getAttribute("data-unit") || "Ton";
    const qty = parseFloat(quantityInput.value) || 0;
    const total = price * qty;

    if (unitPriceDisplay) unitPriceDisplay.textContent = `₹${price.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (quantityDisplay) quantityDisplay.textContent = `${qty} ${unit}`;
    if (unitDisplay) unitDisplay.textContent = unit;
    if (totalAmountDisplay) totalAmountDisplay.textContent = `₹${total.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  }

  productSelect.addEventListener("change", recalculate);
  quantityInput.addEventListener("input", recalculate);
  recalculate();
}

/* ---------- Subtle scroll reveal ---------- */
function initScrollReveal() {
  const sections = document.querySelectorAll("main > section, .reveal-on-scroll");
  sections.forEach(sec => sec.classList.add("reveal"));

  if (!("IntersectionObserver" in window)) {
    sections.forEach(sec => sec.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  sections.forEach(sec => observer.observe(sec));
}

/* ---------- Auto dismiss flash messages ---------- */
function initAlertDismissal() {
  document.querySelectorAll(".alert-dismissible").forEach(alert => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.5s ease";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });
}
