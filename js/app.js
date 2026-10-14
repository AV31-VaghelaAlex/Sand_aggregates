/**
 * LJ ENTERPRISE — Modern Industrial Sand & Aggregates
 * Client-Side Application Logic (Zero-Database Architecture)
 * Contact WhatsApp: +91 81413 52886
 * Contact Email: infoljenterprise07@gmail.com
 */

// 1. Static Materials Catalog Data (No database required!)
const PRODUCTS_DATA = [
  {
    id: "coarse-sand",
    name: "Coarse Sand",
    category: "sand",
    categoryName: "Sand & Fine Aggregates",
    image: "assets/coarse-sand.jpg",
    shortDesc: "Stronger Concrete, Better Binding. Ideal for structural RCC columns and slabs.",
    fullDesc: "Superior quality coarse sand suitable for concrete reinforcement, structural RCC slabs, foundation columns, and high-strength load bearing members. Cleanly screened with minimal silt for superior cement bonding.",
    price: 1350,
    unit: "Ton",
    specs: {
      "Silt Content": "< 3.0%",
      "Specific Gravity": "2.65",
      "Grading Zone": "Zone II (IS 383)",
      "Best For": "RCC Foundations, Columns & Beams"
    },
    inStock: true,
    featured: true
  },
  {
    id: "banas-sand",
    name: "Banas Sand",
    category: "sand",
    categoryName: "Sand & Fine Aggregates",
    image: "assets/banas-sand.jpg",
    shortDesc: "High Quality, Maximum Strength. Natural river sand sourced from Banas riverbeds.",
    fullDesc: "Authentic Banas river sand sourced from premium riverbeds. Free of excessive clay and silt, widely acknowledged for superior bonding and compressive strength in premium construction projects.",
    price: 1700,
    unit: "Ton",
    specs: {
      "Silt Content": "< 2.5%",
      "Specific Gravity": "2.68",
      "Grading Zone": "Zone II Natural River Sand",
      "Best For": "High-Rise Slabs, Bridges & High-Grade Concrete"
    },
    inStock: true,
    featured: true
  },
  {
    id: "msand",
    name: "M-Sand (Manufactured Sand)",
    category: "sand",
    categoryName: "Sand & Fine Aggregates",
    image: "assets/msand.jpg",
    shortDesc: "VSI machine crushed sand engineered for superior concrete strength with zero silt.",
    fullDesc: "Crushed manufactured sand produced via VSI (Vertical Shaft Impactor) machines with cubic grain shape. An eco-friendly and economical replacement for river sand with consistent grading and zero silt wastage.",
    price: 1100,
    unit: "Ton",
    specs: {
      "Silt Content": "0% Organic Silt",
      "Machine Type": "VSI Tertiary Crushed",
      "Grading Zone": "Zone II Compliant (IS 383:2016)",
      "Best For": "RMC Batching, Structural Concrete & Pavements"
    },
    inStock: true,
    featured: true
  },
  {
    id: "fine-sand",
    name: "Fine Plaster Sand",
    category: "sand",
    categoryName: "Sand & Fine Aggregates",
    image: "assets/fine-sand.jpg",
    shortDesc: "Best for Plastering & Brickwork. Clean, smooth mesh and silt-screened.",
    fullDesc: "Fine mesh graded sand specially screened for internal and external wall plastering, joint mortar, bricklaying, and tile bedding. Delivers a crack-free, silky smooth surface finish.",
    price: 1250,
    unit: "Ton",
    specs: {
      "Grain Size": "0.15mm to 1.18mm",
      "Silt Content": "< 3.5%",
      "Grading Zone": "Zone IV (IS 383)",
      "Best For": "Internal/External Wall Plastering & Brick Joint Mortar"
    },
    inStock: true,
    featured: false
  },
  {
    id: "aggregate-10mm",
    name: "10mm Stone Aggregate",
    category: "stone",
    categoryName: "Coarse Stone Aggregates",
    image: "assets/aggregate-10mm.jpg",
    shortDesc: "Crushed blue metal aggregate for dense reinforcement, precast items & roofing.",
    fullDesc: "Single-sized 10mm blue metal granite crushed aggregate. Essential for dense reinforcement concrete, precast slabs, pipe casting, and architectural beam manufacturing with tight rebar clearances.",
    price: 1350,
    unit: "Ton",
    specs: {
      "Size": "10mm Single Sized",
      "Flakiness Index": "< 15%",
      "Crushing Value": "< 20%",
      "Best For": "Thin RCC Slabs, Precast Elements, Lintels & Roofing"
    },
    inStock: true,
    featured: true
  },
  {
    id: "aggregate-20mm",
    name: "20mm Stone Aggregate",
    category: "stone",
    categoryName: "Coarse Stone Aggregates",
    image: "assets/aggregate-20mm.jpg",
    shortDesc: "Standard crushed aggregate for RCC structures, slabs, columns & foundations.",
    fullDesc: "The most widely used coarse aggregate in structural civil engineering. Tested for flakiness and elongation index under strict IS 383 specifications. Delivers high compressive load capacity and tight interlocking.",
    price: 1450,
    unit: "Ton",
    specs: {
      "Size": "20mm Graded Nominal",
      "Impact Value": "< 18%",
      "Water Absorption": "< 0.8%",
      "Best For": "Foundations, RCC Columns, Beams & Raft Slabs"
    },
    inStock: true,
    featured: true
  },
  {
    id: "aggregate-40mm",
    name: "40mm Stone Aggregate",
    category: "stone",
    categoryName: "Coarse Stone Aggregates",
    image: "assets/aggregate-40mm.jpg",
    shortDesc: "Heavy-duty aggregate for mass concrete, road sub-base, and retaining walls.",
    fullDesc: "Angular 40mm crushed basalt/granite stones. Widely utilized in mass concrete foundation rafts, industrial flooring sub-bases, dam foundations, railway track ballast, and road construction.",
    price: 1300,
    unit: "Ton",
    specs: {
      "Size": "40mm Coarse",
      "Compressive Strength": "High Impact Resistant",
      "Specific Gravity": "2.70+",
      "Best For": "Mass Concrete Rafts, Road WBM, Retaining Walls"
    },
    inStock: true,
    featured: false
  },
  {
    id: "gsb",
    name: "Granular Sub Base (GSB)",
    category: "subbase",
    categoryName: "Road Sub-Base",
    image: "assets/gsb.jpg",
    shortDesc: "MoRTH compliant crushed stone sub-base material for highway roadbeds.",
    fullDesc: "Graded Granular Sub Base (GSB) and Wet Mix Macadam (WMM) conforming to MoRTH specifications. Ready for heavy roller compaction, providing solid drainage and load distribution for roads and industrial yards.",
    price: 950,
    unit: "Ton",
    specs: {
      "Grading": "MoRTH Table 400-1 Compliant",
      "CBR Value": "> 30%",
      "Optimum Moisture": "Pre-mixed / Quarry Grade",
      "Best For": "Highway Sub-Bases, Factory Flooring & Parking Lots"
    },
    inStock: true,
    featured: true
  },
  {
    id: "zone-2",
    name: "Zone-2 River Sand",
    category: "sand",
    categoryName: "Sand & Fine Aggregates",
    image: "assets/zone-2.jpg",
    shortDesc: "Standard IS 383 Zone-2 graded sand for general masonry and concrete work.",
    fullDesc: "Natural alluvial river sand graded specifically to Zone II criteria. Excellent workability and low water-cement ratio requirement, ensuring high early compressive strength in concrete mixes.",
    price: 1400,
    unit: "Ton",
    specs: {
      "Grading Zone": "Zone II (IS 383)",
      "Fineness Modulus": "2.6 - 2.9",
      "Silt Content": "< 3.0%",
      "Best For": "General Concrete, Flooring Mortar & Masonry"
    },
    inStock: true,
    featured: false
  }
];

// WhatsApp Business Contact Configuration
const WHATSAPP_PHONE = "918141352886"; // +91 81413 52886
const CALL_PHONE = "+918141352886";

// 2. DOM Initialization
document.addEventListener("DOMContentLoaded", () => {
  initNavbar();
  renderProductsCatalog("all");
  initCatalogFilters();
  initCostCalculator();
  initContactForm();
  initScrollReveal();
  initMaterialModal();
});

// ==========================================================================
// 3. NAVBAR & MOBILE DRAWER
// ==========================================================================
function initNavbar() {
  const header = document.querySelector(".site-header");
  const toggleBtn = document.getElementById("mobileNavToggle");
  const drawer = document.getElementById("mobileMenuDrawer");
  const navLinks = document.querySelectorAll(".nav-link, .mobile-nav-link");

  // Sticky header scroll shadow
  window.addEventListener("scroll", () => {
    if (window.scrollY > 30) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  });

  // Mobile menu toggle
  if (toggleBtn && drawer) {
    toggleBtn.addEventListener("click", () => {
      const isOpen = drawer.classList.contains("open");
      if (isOpen) {
        drawer.classList.remove("open");
        toggleBtn.classList.remove("open");
        toggleBtn.setAttribute("aria-expanded", "false");
      } else {
        drawer.classList.add("open");
        toggleBtn.classList.add("open");
        toggleBtn.setAttribute("aria-expanded", "true");
      }
    });

    // Close mobile drawer on navigation click
    navLinks.forEach(link => {
      link.addEventListener("click", () => {
        drawer.classList.remove("open");
        toggleBtn.classList.remove("open");
        toggleBtn.setAttribute("aria-expanded", "false");
      });
    });
  }
}

// ==========================================================================
// 4. MATERIAL CATALOG RENDERING & FILTERING
// ==========================================================================
function renderProductsCatalog(category = "all") {
  const grid = document.getElementById("productsGrid");
  if (!grid) return;

  const filtered = category === "all" 
    ? PRODUCTS_DATA 
    : PRODUCTS_DATA.filter(p => p.category === category);

  grid.innerHTML = filtered.map(product => {
    const specEntries = Object.entries(product.specs || {}).slice(0, 3);
    const specsHtml = specEntries.map(([label, val]) => `
      <div class="product-spec-row">
        <span class="label">${label}:</span>
        <span class="val">${val}</span>
      </div>
    `).join("");

    return `
      <article class="product-card" data-category="${product.category}">
        <div class="product-thumb-wrap">
          <img src="${product.image}" alt="${product.name}" loading="lazy" onerror="this.src='assets/hero.jpeg'">
          <div class="product-badge-overlay">
            ${product.featured ? '<span class="badge badge-featured"><i class="fa-solid fa-star"></i> Featured</span>' : ''}
            <span class="badge badge-in-stock"><i class="fa-solid fa-circle-check"></i> In Stock</span>
          </div>
        </div>
        <div class="product-body">
          <span class="product-category">${product.categoryName}</span>
          <h3 class="product-title">${product.name}</h3>
          <p class="product-desc">${product.shortDesc}</p>
          
          <div class="product-specs">
            ${specsHtml}
          </div>

          <div class="product-price-row">
            <div>
              <span class="product-rate">₹${product.price.toLocaleString('en-IN')}</span>
              <span class="product-unit">/ ${product.unit} (Est.)</span>
            </div>
            <button type="button" class="btn btn-outline btn-sm view-specs-btn" data-product-id="${product.id}">
              <i class="fa-regular fa-file-lines"></i> Specs
            </button>
          </div>

          <div class="product-actions">
            <button type="button" class="btn btn-whatsapp btn-sm order-product-wa-btn" data-product-name="${product.name}" data-product-rate="${product.price}">
              <i class="fa-brands fa-whatsapp"></i> Order on WhatsApp
            </button>
            <button type="button" class="btn btn-outline btn-sm calc-product-btn" data-product-id="${product.id}">
              <i class="fa-solid fa-calculator"></i>
            </button>
          </div>
        </div>
      </article>
    `;
  }).join("");

  // Attach event handlers for newly rendered product card buttons
  attachProductCardEvents();
}

function initCatalogFilters() {
  const filterBtns = document.querySelectorAll(".filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const category = btn.getAttribute("data-filter");
      renderProductsCatalog(category);
    });
  });
}

function attachProductCardEvents() {
  // Order via WhatsApp button on each card
  document.querySelectorAll(".order-product-wa-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const name = btn.getAttribute("data-product-name");
      const rate = btn.getAttribute("data-product-rate");
      const message = `*Inquiry / Material Order from Website*\n\n` +
                      `Hello LJ Enterprise,\n` +
                      `I am interested in ordering:\n` +
                      `• *Material:* ${name}\n` +
                      `• *Estimated Rate:* ₹${rate} / Ton\n\n` +
                      `Please share dispatch availability, dumper freight, and current site delivery rates.`;
      
      openWhatsApp(message);
    });
  });

  // Jump to calculator with selected product
  document.querySelectorAll(".calc-product-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-product-id");
      const calcSelect = document.getElementById("calcProductSelect");
      if (calcSelect) {
        calcSelect.value = id;
        calcSelect.dispatchEvent(new Event("change"));
        document.getElementById("calculator").scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Specs modal button
  document.querySelectorAll(".view-specs-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-product-id");
      showProductModal(id);
    });
  });
}

// ==========================================================================
// 5. INTERACTIVE LIVE MATERIAL COST CALCULATOR
// ==========================================================================
function initCostCalculator() {
  const select = document.getElementById("calcProductSelect");
  const qtyInput = document.getElementById("calcQtyInput");
  const qtyRange = document.getElementById("calcQtyRange");
  const locationInput = document.getElementById("calcLocationInput");

  const rateDisplay = document.getElementById("calcUnitRateDisplay");
  const qtyDisplay = document.getElementById("calcQtyDisplay");
  const totalDisplay = document.getElementById("calcTotalDisplay");
  const truckCountDisplay = document.getElementById("calcTruckCountDisplay");
  const sendWaBtn = document.getElementById("calcSendWhatsAppBtn");

  if (!select || !qtyInput) return;

  // Populate product dropdown options
  select.innerHTML = PRODUCTS_DATA.map(p => `
    <option value="${p.id}" data-price="${p.price}" data-unit="${p.unit}">
      ${p.name} — ₹${p.price.toLocaleString('en-IN')}/${p.unit}
    </option>
  `).join("");

  function updateCalculator() {
    const selectedOption = select.options[select.selectedIndex];
    const unitPrice = parseFloat(selectedOption.getAttribute("data-price") || 0);
    const unit = selectedOption.getAttribute("data-unit") || "Ton";
    const quantity = parseFloat(qtyInput.value) || 0;

    const total = quantity * unitPrice;
    const approxTrucks = Math.max(1, Math.ceil(quantity / 25)); // ~25 tons per 10-wheeler dumper

    if (rateDisplay) rateDisplay.textContent = `₹${unitPrice.toLocaleString('en-IN')} / ${unit}`;
    if (qtyDisplay) qtyDisplay.textContent = `${quantity} ${unit}s`;
    if (totalDisplay) totalDisplay.textContent = `₹${total.toLocaleString('en-IN')}`;
    if (truckCountDisplay) truckCountDisplay.textContent = `${approxTrucks} Dumper(s) (approx. 25-30T each)`;
  }

  // Sync range and number input
  qtyInput.addEventListener("input", () => {
    if (qtyRange) qtyRange.value = qtyInput.value;
    updateCalculator();
  });

  if (qtyRange) {
    qtyRange.addEventListener("input", () => {
      qtyInput.value = qtyRange.value;
      updateCalculator();
    });
  }

  select.addEventListener("change", updateCalculator);

  // Initial calculation run
  updateCalculator();

  // Send Order via WhatsApp action
  if (sendWaBtn) {
    sendWaBtn.addEventListener("click", () => {
      const selectedOption = select.options[select.selectedIndex];
      const prodName = selectedOption.text.split("—")[0].trim();
      const unitPrice = parseFloat(selectedOption.getAttribute("data-price") || 0);
      const unit = selectedOption.getAttribute("data-unit") || "Ton";
      const quantity = qtyInput.value;
      const total = (parseFloat(quantity) * unitPrice).toLocaleString('en-IN');
      const location = locationInput && locationInput.value.trim() ? locationInput.value.trim() : "Ahmedabad / Gujarat site";
      const trucks = Math.max(1, Math.ceil(parseFloat(quantity) / 25));

      const message = `*Material Order Estimate via Website Calculator*\n\n` +
                      `Hello LJ Enterprise,\n` +
                      `I calculated an order on your website:\n` +
                      `• *Material:* ${prodName}\n` +
                      `• *Required Quantity:* ${quantity} ${unit}\n` +
                      `• *Estimated Unit Rate:* ₹${unitPrice.toLocaleString('en-IN')} / ${unit}\n` +
                      `• *Estimated Material Value:* ₹${total}\n` +
                      `• *Estimated Dumpers:* ${trucks} Truck Loads\n` +
                      `• *Site Location:* ${location}\n\n` +
                      `Please confirm order booking, delivery schedule, and invoice details.`;

      openWhatsApp(message);
    });
  }
}

// ==========================================================================
// 6. CONTACT & ENQUIRY FORM (Zero-Database WhatsApp & Mailto Submission)
// ==========================================================================
function initContactForm() {
  const form = document.getElementById("enquiryForm");
  const materialSelect = document.getElementById("enquiryMaterialSelect");

  // Populate enquiry form material options
  if (materialSelect) {
    materialSelect.innerHTML = `<option value="">Select Material Needed...</option>` +
      PRODUCTS_DATA.map(p => `<option value="${p.name}">${p.name} (₹${p.price}/${p.unit})</option>`).join("") +
      `<option value="Multiple Materials">Multiple Materials / Bulk Supply</option>` +
      `<option value="Other / Special Requirement">Other / Custom Requirement</option>`;
  }

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();

      const name = document.getElementById("fName").value.trim();
      const phone = document.getElementById("fPhone").value.trim();
      const email = document.getElementById("fEmail").value.trim() || "N/A";
      const company = document.getElementById("fCompany").value.trim() || "N/A";
      const material = materialSelect.value || "Not specified";
      const quantity = document.getElementById("fQuantity").value.trim() || "Unspecified";
      const location = document.getElementById("fLocation").value.trim() || "Ahmedabad & nearby";
      const messageText = document.getElementById("fMessage").value.trim() || "Please call back with material prices.";

      if (!name || !phone) {
        alert("Please provide both your name and phone number.");
        return;
      }

      const formattedWhatsApp = `*New Material Quotation Inquiry from Website*\n\n` +
                                `*Customer Name:* ${name}\n` +
                                `*Mobile Number:* ${phone}\n` +
                                `*Company / Firm:* ${company}\n` +
                                `*Email:* ${email}\n\n` +
                                `*Material Needed:* ${material}\n` +
                                `*Estimated Quantity:* ${quantity}\n` +
                                `*Site / Delivery Location:* ${location}\n\n` +
                                `*Message / Specifications:*\n${messageText}`;

      openWhatsApp(formattedWhatsApp);
      showToast("Redirecting to WhatsApp...", "Your quotation inquiry was formatted. Complete sending on WhatsApp.");
      form.reset();
    });
  }
}

// ==========================================================================
// 7. PRODUCT SPECIFICATION MODAL
// ==========================================================================
function initMaterialModal() {
  const backdrop = document.getElementById("specsModalBackdrop");
  const closeBtn = document.getElementById("modalCloseBtn");
  const doneBtn = document.getElementById("modalDoneBtn");

  if (!backdrop) return;

  function closeModal() {
    backdrop.classList.remove("open");
  }

  if (closeBtn) closeBtn.addEventListener("click", closeModal);
  if (doneBtn) doneBtn.addEventListener("click", closeModal);
  backdrop.addEventListener("click", (e) => {
    if (e.target === backdrop) closeModal();
  });
}

function showProductModal(productId) {
  const product = PRODUCTS_DATA.find(p => p.id === productId);
  if (!product) return;

  const backdrop = document.getElementById("specsModalBackdrop");
  const titleEl = document.getElementById("modalProductTitle");
  const imgEl = document.getElementById("modalProductImg");
  const descEl = document.getElementById("modalProductDesc");
  const specsListEl = document.getElementById("modalSpecsList");
  const waBtn = document.getElementById("modalWaOrderBtn");

  if (titleEl) titleEl.textContent = product.name;
  if (imgEl) {
    imgEl.src = product.image;
    imgEl.alt = product.name;
  }
  if (descEl) descEl.textContent = product.fullDesc;

  if (specsListEl) {
    specsListEl.innerHTML = Object.entries(product.specs || {}).map(([k, v]) => `
      <div style="display:flex; justify-content:space-between; padding: 6px 0; border-bottom: 1px solid #E2E8F0; font-size: 0.9rem;">
        <span style="color:#64748B;">${k}</span>
        <strong style="color:#0F172A;">${v}</strong>
      </div>
    `).join("");
  }

  if (waBtn) {
    waBtn.onclick = () => {
      const msg = `*Inquiry for ${product.name}*\n\n` +
                  `Hello LJ Enterprise,\n` +
                  `I checked the specifications for ${product.name} (₹${product.price}/${product.unit}) on your website. Please provide availability and rate for delivery.`;
      openWhatsApp(msg);
    };
  }

  backdrop.classList.add("open");
}

// ==========================================================================
// 8. WHATSAPP & TOAST UTILITIES
// ==========================================================================
function openWhatsApp(textMessage) {
  const url = `https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(textMessage)}`;
  showToast("Opening WhatsApp...", "Connecting you directly to LJ Enterprise dispatch team.");
  window.open(url, "_blank");
}

function showToast(title, subtitle) {
  const toast = document.getElementById("toastContainer");
  const titleEl = document.getElementById("toastTitle");
  const subEl = document.getElementById("toastDesc");

  if (!toast) return;

  if (titleEl) titleEl.textContent = title;
  if (subEl) subEl.textContent = subtitle;

  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 4500);
}

// ==========================================================================
// 9. SCROLL REVEAL ANIMATIONS
// ==========================================================================
function initScrollReveal() {
  const elements = document.querySelectorAll(".fade-up");
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("revealed");
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: "0px 0px -40px 0px"
  });

  elements.forEach(el => observer.observe(el));
}
