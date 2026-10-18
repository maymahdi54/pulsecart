'use strict';

const PRODUCTS = [
  { id: 1, name: 'Nova Bluetooth Headphones', category: 'audio', price: 89.99, image: 'HEADPHONES' },
  { id: 2, name: 'Zenith Smart Watch', category: 'wearables', price: 199.99, image: 'WATCH' },
  { id: 3, name: 'Aura Tablet Pro', category: 'electronics', price: 449.99, image: 'TABLET' },
  { id: 4, name: 'Echo Wireless Earbuds', category: 'audio', price: 129.99, image: 'EARBUDS' },
  { id: 5, name: 'Pulse Fitness Band', category: 'wearables', price: 79.99, image: 'BAND' },
  { id: 6, name: 'Volt USB-C Hub', category: 'electronics', price: 49.99, image: 'HUB' },
  { id: 7, name: 'Beacon Portable Speaker', category: 'audio', price: 149.99, image: 'SPEAKER' },
  { id: 8, name: 'Glide Mouse Pro', category: 'electronics', price: 69.99, image: 'MOUSE' },
];

const TAX_RATE = 0.08;
const LOGIN_CREDENTIALS = { username: 'testuser', password: 'password123' };

let state = {
  products: [...PRODUCTS],
  filter: 'all',
  search: '',
  cart: [],
  user: null,
};

const els = {
  productGrid: document.querySelector('[data-testid="product-grid"]'),
  categoryChips: document.querySelectorAll('[data-testid^="category-"]'),
  searchInput: document.querySelector('[data-testid="search-input"]'),
  cartBadge: document.querySelector('[data-testid="cart-badge"]'),
  cartSlideover: document.querySelector('[data-testid="cart-slideover"]'),
  cartCloseBtn: document.querySelector('[data-testid="cart-close-btn"]'),
  cartItems: document.querySelector('[data-testid="cart-items"]'),
  cartEmpty: document.querySelector('[data-testid="cart-empty"]'),
  cartSubtotal: document.querySelector('[data-testid="cart-subtotal"]'),
  cartTax: document.querySelector('[data-testid="cart-tax"]'),
  cartTotal: document.querySelector('[data-testid="cart-total"]'),
  btnCheckout: document.querySelector('[data-testid="btn-checkout"]'),
  navUserStatus: document.querySelector('[data-testid="nav-user-status"]'),
  navLoginBtn: document.querySelector('[data-testid="nav-login-btn"]'),
  navCartBtn: document.querySelector('[data-testid="nav-cart-btn"]'),
};

function iconFor(product) {
  const map = {
    HEADPHONES: '<svg viewBox="0 0 24 24"><path d="M3 13v2c0 5 5 5 5 5s5 0 5-5v-2L3 13zM9 3L5 6.99V10c0 5.51 4.49 10 10 10c5.51 0 10-4.49 10-10V6.99L15 3c-.53-1.05-1.38-2-2.35-2.52-.23-.13-.49-.21-.77-.27-.73-.16-1.49-.24-2.23-.24-.74 0-1.5.08-2.23.24-.28.06-.54.14-.77.27C10.38 1 9.53 1.95 9 3z" fill="currentColor"/></svg>',
    WATCH: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 9v4M12 17v4M9 12h4M17 12h4" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    TABLET: '<svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/><line x1="12" y1="17" x2="12.01" y2="17" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    EARBUDS: '<svg viewBox="0 0 24 24"><path d="M17.33 2.72A8 8 0 0119 12c0 1.1-.46 2.09-1.22 2.86L7.28 3.92A8 8 0 017 12c0 1.1.46 2.09 1.22 2.86L17.33 2.72z" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    BAND: '<svg viewBox="0 0 24 24"><path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2z" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    HUB: '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    SPEAKER: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="6" fill="none" stroke="currentColor" stroke-width="2"/><rect x="9" y="11" width="6" height="4" rx="1" ry="1" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    MOUSE: '<svg viewBox="0 0 24 24"><path d="M3 3h18v18H3z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3v18M3 12h18" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  };
  return map[product.image] || '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/></svg>';
}

function formatCurrency(amount) {
  return '$' + amount.toFixed(2);
}

function renderProducts() {
  els.productGrid.innerHTML = '';
  const filtered = state.products.filter(p => {
    const matchCategory = state.filter === 'all' || p.category === state.filter;
    const matchSearch = p.name.toLowerCase().includes(state.search.toLowerCase());
    return matchCategory && matchSearch;
  });

  if (filtered.length === 0) {
    els.productGrid.innerHTML = '<div class="cart-empty" style="grid-column:1/-1">No products found.</div>';
    return;
  }

  for (const product of filtered) {
    const card = document.createElement('article');
    card.className = 'product-card';
    card.dataset.testid = 'product-card';
    card.dataset.productId = product.id;
    card.setAttribute('role', 'button');
    card.tabIndex = 0;
    card.innerHTML = `
      <div class="product-badge">${product.category}</div>
      <div class="product-icon" style="font-size:2.5rem;color:var(--accent);margin-bottom:0.5rem;">${iconFor(product)}</div>
      <div class="product-title" data-testid="product-title-${product.id}">${product.name}</div>
      <div class="product-category">${product.category}</div>
      <div class="product-price" data-testid="product-price-${product.id}">${formatCurrency(product.price)}</div>
      <button class="btn-add-to-cart" data-testid="add-to-cart-${product.id}">Add to Cart</button>
    `;
    card.querySelector('[data-testid^="add-to-cart-"]').addEventListener('click', (e) => {
      e.stopPropagation();
      addToCart(product.id);
    });
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        addToCart(product.id);
      }
    });
    els.productGrid.appendChild(card);
  }
}

function updateCartBadge() {
  const total = state.cart.reduce((sum, item) => sum + item.qty, 0);
  els.cartBadge.textContent = total;
  els.cartBadge.style.display = total > 0 ? 'block' : 'none';
}

function renderCart() {
  els.cartItems.innerHTML = '';
  if (state.cart.length === 0) {
    els.cartItems.appendChild(els.cartEmpty.cloneNode(true) || document.createElement('div'));
    const empty = document.createElement('div');
    empty.className = 'cart-empty';
    empty.dataset.testid = 'cart-empty';
    empty.textContent = 'Your cart is empty.';
    els.cartItems.appendChild(empty);
  } else {
    for (const item of state.cart) {
      const product = PRODUCTS.find(p => p.id === item.id);
      const cartItem = document.createElement('div');
      cartItem.className = 'cart-item';
      cartItem.dataset.testid = 'cart-item';
      cartItem.dataset.cartItemId = item.id;
      cartItem.innerHTML = `
        <div class="cart-item-info">
          <div class="cart-item-title">${product.name}</div>
          <div class="cart-item-price">${formatCurrency(product.price)}</div>
        </div>
        <div class="cart-item-controls">
          <button class="btn-qty-minus" data-testid="qty-minus-${item.id}">&minus;</button>
          <input type="text" class="cart-item-qty" data-testid="qty-input-${item.id}" value="${item.qty}" readonly>
          <button class="btn-qty-plus" data-testid="qty-plus-${item.id}">&plus;</button>
          <button class="cart-remove-btn" data-testid="remove-${item.id}">&times;</button>
        </div>
      `;
      cartItem.querySelector('[data-testid^="qty-minus-"]').addEventListener('click', () => changeQty(item.id, -1));
      cartItem.querySelector('[data-testid^="qty-plus-"]').addEventListener('click', () => changeQty(item.id, 1));
      cartItem.querySelector('[data-testid^="remove-"]').addEventListener('click', () => removeFromCart(item.id));
      els.cartItems.appendChild(cartItem);
    }
  }
  updateTotals();
}

function updateTotals() {
  const subtotal = state.cart.reduce((sum, item) => {
    const product = PRODUCTS.find(p => p.id === item.id);
    return sum + product.price * item.qty;
  }, 0);
  const tax = subtotal * TAX_RATE;
  const total = subtotal + tax;
  els.cartSubtotal.textContent = formatCurrency(subtotal);
  els.cartTax.textContent = formatCurrency(tax);
  els.cartTotal.textContent = formatCurrency(total);
}

function addToCart(productId) {
  const existing = state.cart.find(item => item.id === productId);
  if (existing) {
    existing.qty += 1;
  } else {
    state.cart.push({ id: productId, qty: 1 });
  }
  updateCartBadge();
  renderCart();
}

function changeQty(productId, delta) {
  const item = state.cart.find(i => i.id === productId);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) {
    removeFromCart(productId);
  } else {
    updateCartBadge();
    renderCart();
  }
}

function removeFromCart(productId) {
  state.cart = state.cart.filter(i => i.id !== productId);
  updateCartBadge();
  renderCart();
}

function updateModalBodyClass() {
  const loginOpen = document.querySelector('[data-testid="login-modal"]').classList.contains('visible');
  const checkoutOpen = document.querySelector('[data-testid="checkout-modal"]').classList.contains('visible');
  if (loginOpen || checkoutOpen) {
    document.body.classList.add('modal-open');
  } else {
    document.body.classList.remove('modal-open');
  }
}

function openCart() {
  els.cartSlideover.classList.add('open');
}

function closeCart() {
  els.cartSlideover.classList.remove('open');
}

function openLogin() {
  document.querySelector('[data-testid="login-modal"]').classList.add('visible');
  updateModalBodyClass();
}

function closeLogin() {
  document.querySelector('[data-testid="login-modal"]').classList.remove('visible');
  document.querySelector('#login-form').reset();
  document.querySelectorAll('[data-testid^="error-"]').forEach(el => el.textContent = '');
  updateModalBodyClass();
}

function openCheckout() {
  if (state.cart.length === 0) return;
  document.querySelector('[data-testid="checkout-modal"]').classList.add('visible');
  updateModalBodyClass();
}

function closeCheckout() {
  document.querySelector('[data-testid="checkout-modal"]').classList.remove('visible');
  document.querySelector('#checkout-form').reset();
  document.querySelectorAll('[data-testid^="error-"]').forEach(el => el.textContent = '');
  updateModalBodyClass();
}

function updateAuthUI() {
  if (state.user) {
    els.navUserStatus.textContent = state.user;
    els.navLoginBtn.textContent = 'Logout';
    els.navLoginBtn.dataset.testid = 'nav-logout-btn';
  } else {
    els.navUserStatus.textContent = 'Guest';
    els.navLoginBtn.textContent = 'Login';
    els.navLoginBtn.dataset.testid = 'nav-login-btn';
  }
}

function validateLogin(username, password) {
  const errors = {};
  if (!username) errors.username = 'Username is required.';
  if (!password) errors.password = 'Password is required.';
  if (username && username !== LOGIN_CREDENTIALS.username) errors.username = 'Invalid username.';
  if (password && password !== LOGIN_CREDENTIALS.password) errors.password = 'Invalid password.';
  return errors;
}

function validateCheckout(formData) {
  const errors = {};
  if (!formData.name) errors.name = 'Full name is required.';
  if (!formData.email) errors.email = 'Email is required.';
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) errors.email = 'Enter a valid email address.';
  if (!formData.address) errors.address = 'Shipping address is required.';
  if (!formData.card) errors.card = 'Card number is required.';
  else if (!/^\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}$/.test(formData.card.replace(/\s/g, ''))) errors.card = 'Enter a valid 16-digit card number.';
  return errors;
}

function init() {
  // Category filter
  els.categoryChips.forEach(chip => {
    chip.addEventListener('click', () => {
      els.categoryChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      state.filter = chip.dataset.category;
      renderProducts();
    });
  });

  // Search
  els.searchInput.addEventListener('input', (e) => {
    state.search = e.target.value;
    renderProducts();
  });

  // Cart toggle
  els.navCartBtn.addEventListener('click', openCart);
  els.cartCloseBtn.addEventListener('click', closeCart);
  els.btnCheckout.addEventListener('click', openCheckout);

  // Login
  els.navLoginBtn.addEventListener('click', () => {
    if (state.user) {
      state.user = null;
      updateAuthUI();
    } else {
      openLogin();
    }
  });

  const loginModal = document.querySelector('[data-testid="login-modal"]');
  const loginCloseBtn = document.querySelector('[data-testid="login-close-btn"]');
  const loginForm = document.querySelector('#login-form');
  const btnCancelLogin = document.querySelector('[data-testid="btn-cancel-login"]');
  const btnContinueLogin = document.querySelector('[data-testid="btn-continue-login"]');

  loginCloseBtn.addEventListener('click', closeLogin);
  btnCancelLogin.addEventListener('click', closeLogin);
  btnContinueLogin.addEventListener('click', closeLogin);

  loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.querySelector('#login-username').value;
    const password = document.querySelector('#login-password').value;
    const errors = validateLogin(username, password);

    document.querySelector('[data-testid="error-username"]').textContent = errors.username || '';
    document.querySelector('[data-testid="error-password"]').textContent = errors.password || '';
    document.querySelector('[data-testid="login-error-general"]').textContent = '';

    if (Object.keys(errors).length === 0) {
      state.user = username;
      updateAuthUI();
      document.querySelector('[data-testid="logged-in-user"]').textContent = username;
      document.querySelector('#login-form').style.display = 'none';
      document.querySelector('[data-testid="login-success"]').style.display = 'flex';
    }
  });

  // Checkout
  const checkoutModal = document.querySelector('[data-testid="checkout-modal"]');
  const checkoutCloseBtn = document.querySelector('[data-testid="checkout-close-btn"]');
  const checkoutForm = document.querySelector('#checkout-form');
  const btnCancelCheckout = document.querySelector('[data-testid="btn-cancel-checkout"]');
  const btnContinueShopping = document.querySelector('[data-testid="btn-continue-shopping"]');

  checkoutCloseBtn.addEventListener('click', closeCheckout);
  btnCancelCheckout.addEventListener('click', closeCheckout);
  btnContinueShopping.addEventListener('click', () => {
    closeCheckout();
    state.cart = [];
    updateCartBadge();
    renderCart();
  });
  // Close modals when clicking the overlay backdrop
  checkoutModal.addEventListener('click', (e) => {
    if (e.target === checkoutModal) closeCheckout();
  });
  loginModal.addEventListener('click', (e) => {
    if (e.target === loginModal) closeLogin();
  });

  checkoutForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = {
      name: document.querySelector('#checkout-name').value,
      email: document.querySelector('#checkout-email').value,
      address: document.querySelector('#checkout-address').value,
      card: document.querySelector('#checkout-card').value,
    };
    const errors = validateCheckout(formData);

    document.querySelector('[data-testid="error-fullname"]').textContent = errors.name || '';
    document.querySelector('[data-testid="error-email"]').textContent = errors.email || '';
    document.querySelector('[data-testid="error-address"]').textContent = errors.address || '';
    document.querySelector('[data-testid="error-card"]').textContent = errors.card || '';
    document.querySelector('[data-testid="checkout-error-general"]').textContent = '';

    if (Object.keys(errors).length === 0) {
      document.querySelector('#checkout-form').style.display = 'none';
      document.querySelector('[data-testid="checkout-success"]').style.display = 'flex';
    }
  });

  renderProducts();
  updateCartBadge();
  updateAuthUI();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
