<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': isCollapsed }">
    <!-- Brand -->
    <div class="sidebar-brand">
      <span class="brand-name">{{ t('nav.companyName') }}</span>
      <span class="brand-subtitle">{{ t('nav.subtitle') }}</span>
    </div>

    <!-- Nav links -->
    <nav class="sidebar-nav" aria-label="Main navigation">
      <router-link
        to="/"
        class="nav-item"
        :exact-active-class="'nav-item--active'"
        :active-class="''"
        aria-current="page"
        :title="isCollapsed ? t('nav.overview') : null"
      >
        <!-- Grid/home icon for Overview -->
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
          <rect x="2" y="2" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
          <rect x="10" y="2" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
          <rect x="2" y="10" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
          <rect x="10" y="10" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <span class="nav-label">{{ t('nav.overview') }}</span>
      </router-link>

      <router-link
        to="/inventory"
        class="nav-item"
        active-class="nav-item--active"
        aria-current="page"
        :title="isCollapsed ? t('nav.inventory') : null"
      >
        <!-- Box icon for Inventory -->
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
          <path d="M2.5 5.5L9 2L15.5 5.5V12.5L9 16L2.5 12.5V5.5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
          <path d="M9 2V16" stroke="currentColor" stroke-width="1.5"/>
          <path d="M2.5 5.5L9 9L15.5 5.5" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <span class="nav-label">{{ t('nav.inventory') }}</span>
      </router-link>

      <router-link
        to="/orders"
        class="nav-item"
        active-class="nav-item--active"
        aria-current="page"
        :title="isCollapsed ? t('nav.orders') : null"
      >
        <!-- Clipboard/cart icon for Orders -->
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
          <rect x="3" y="3" width="12" height="13" rx="1.5" stroke="currentColor" stroke-width="1.5"/>
          <path d="M6.5 3V2C6.5 1.72386 6.72386 1.5 7 1.5H11C11.2761 1.5 11.5 1.72386 11.5 2V3" stroke="currentColor" stroke-width="1.5"/>
          <path d="M6 8H12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M6 11H10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span class="nav-label">{{ t('nav.orders') }}</span>
      </router-link>

      <router-link
        to="/restocking"
        class="nav-item"
        active-class="nav-item--active"
        aria-current="page"
        :title="isCollapsed ? t('nav.restocking') : null"
      >
        <!-- Refresh/arrows icon for Restocking -->
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
          <path d="M3 9C3 5.68629 5.68629 3 9 3C11.0722 3 12.9037 4.02742 14.0572 5.6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M12 5.5L14.5 5.5L14.5 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M15 9C15 12.3137 12.3137 15 9 15C6.92779 15 5.09633 13.9726 3.94282 12.4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M6 12.5L3.5 12.5L3.5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="nav-label">{{ t('nav.restocking') }}</span>
      </router-link>

      <router-link
        to="/spending"
        class="nav-item"
        active-class="nav-item--active"
        aria-current="page"
        :title="isCollapsed ? t('nav.finance') : null"
      >
        <!-- Dollar/chart icon for Finance -->
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
          <circle cx="9" cy="9" r="6.5" stroke="currentColor" stroke-width="1.5"/>
          <path d="M9 5.5V6.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M9 11.5V12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M7 8C7 7.44772 7.44772 7 8 7H9.5C10.3284 7 11 7.67157 11 8.5C11 9.32843 10.3284 10 9.5 10H8.5C7.67157 10 7 10.6716 7 11.5C7 12.3284 7.67157 13 8.5 13H10C10.5523 13 11 12.5523 11 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span class="nav-label">{{ t('nav.finance') }}</span>
      </router-link>

      <router-link
        to="/demand"
        class="nav-item"
        active-class="nav-item--active"
        aria-current="page"
        :title="isCollapsed ? t('nav.demandForecast') : null"
      >
        <!-- Trending-up icon for Demand Forecast -->
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
          <path d="M2 13L7 8L10.5 11.5L16 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 5H16V9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="nav-label">{{ t('nav.demandForecast') }}</span>
      </router-link>

      <router-link
        to="/reports"
        class="nav-item"
        active-class="nav-item--active"
        aria-current="page"
        :title="isCollapsed ? 'Reports' : null"
      >
        <!-- Document icon for Reports -->
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
          <path d="M4 3H11L15 7V15C15 15.5523 14.5523 16 14 16H4C3.44772 16 3 15.5523 3 15V4C3 3.44772 3.44772 3 4 3Z" stroke="currentColor" stroke-width="1.5"/>
          <path d="M11 3V7H15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M6 10H12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M6 12.5H10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span class="nav-label">Reports</span>
      </router-link>
    </nav>

    <!-- Collapse toggle — hidden on small screens where the rail is forced -->
    <div class="sidebar-toggle-row">
      <button
        class="sidebar-toggle"
        :aria-label="isCollapsed ? t('nav.expandSidebar') : t('nav.collapseSidebar')"
        :aria-expanded="!isCollapsed"
        @click="toggleCollapsed"
      >
        <!-- Chevron: points left («) when expanded, right (») when collapsed -->
        <svg
          class="toggle-icon"
          :class="{ 'toggle-icon--flipped': isCollapsed }"
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="none"
          aria-hidden="true"
        >
          <path d="M10 4L6 8L10 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="toggle-label">{{ t('nav.collapseSidebar') }}</span>
      </button>
    </div>

    <!-- Footer: language + profile -->
    <div class="sidebar-footer">
      <LanguageSwitcher :dark="true" />
      <ProfileMenu
        :dark="true"
        @show-profile-details="emit('show-profile-details')"
        @show-tasks="emit('show-tasks')"
      />
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from '../composables/useI18n'
import LanguageSwitcher from './LanguageSwitcher.vue'
import ProfileMenu from './ProfileMenu.vue'

const { t } = useI18n()

const emit = defineEmits(['show-profile-details', 'show-tasks'])

// Read persisted collapsed state; default to false (expanded).
// Defensive: localStorage may be unavailable (private browsing, SSR, etc.)
const readPersistedCollapsed = () => {
  try {
    return localStorage.getItem('sidebar-collapsed') === 'true'
  } catch {
    return false
  }
}

const isCollapsed = ref(readPersistedCollapsed())

const toggleCollapsed = () => {
  isCollapsed.value = !isCollapsed.value
  try {
    localStorage.setItem('sidebar-collapsed', String(isCollapsed.value))
  } catch {
    // Storage unavailable — state still works for this session
  }
}
</script>

<style scoped>
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  width: var(--sidebar-width, 248px);
  flex-shrink: 0;
  background: var(--sidebar-bg, #0f172a);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 100;
  /* Smooth width transition when collapsing/expanding */
  transition: width 0.2s ease;
}

/* ── Rail state shared by both manual collapse and small-screen media query ─ */

/* Applied via .sidebar--collapsed class (manual toggle) or @media (see below).
   Grouped here as a comment anchor; actual selectors are written out in both
   places since CSS has no native mixin support. */

/* Brand section */
.sidebar-brand {
  padding: var(--space-6, 1.5rem) var(--space-4, 1rem);
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  flex-shrink: 0;
}

.brand-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.025em;
  line-height: 1.2;
}

.brand-subtitle {
  font-size: 0.75rem;
  color: #94a3b8; /* slate-400 */
  font-weight: 400;
  line-height: 1.3;
}

/* Nav section */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-3, 0.75rem);
  display: flex;
  flex-direction: column;
  gap: 2px;
  /* Custom scrollbar for dark bg */
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.1) transparent;
}

.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.875rem;
  border-radius: 8px;
  color: #cbd5e1; /* slate-300 */
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  transition: background 0.15s ease, color 0.15s ease;
  outline: none;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #ffffff;
}

.nav-item:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 1px;
}

/* Active state: exact-active-class on / route, active-class on all others */
.nav-item--active {
  background: var(--accent, #2563eb);
  color: #ffffff;
  font-weight: 600;
}

.nav-item--active:hover {
  background: #1d4ed8;
}

.nav-icon {
  flex-shrink: 0;
  /* currentColor tracks text color automatically */
}

.nav-label {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Toggle row — sits between nav and footer */
.sidebar-toggle-row {
  flex-shrink: 0;
  padding: var(--space-2, 0.5rem) var(--space-3, 0.75rem);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.sidebar-toggle {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  width: 100%;
  padding: 0.5rem 0.625rem;
  background: none;
  border: none;
  border-radius: 8px;
  color: #94a3b8; /* slate-400 — subtle, not as prominent as nav items */
  cursor: pointer;
  font-family: inherit;
  font-size: 0.813rem;
  font-weight: 500;
  transition: background 0.15s ease, color 0.15s ease;
}

.sidebar-toggle:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #cbd5e1;
}

.sidebar-toggle:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 1px;
}

.toggle-icon {
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

/* Flipped chevron points right (expand) when collapsed */
.toggle-icon--flipped {
  transform: rotate(180deg);
}

.toggle-label {
  white-space: nowrap;
  overflow: hidden;
}

/* Footer section */
.sidebar-footer {
  flex-shrink: 0;
  padding: var(--space-3, 0.75rem);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* ── Collapsed rail state (manual toggle) ─────────────────────────────────── */

.sidebar--collapsed {
  width: var(--sidebar-rail-width, 72px);
}

.sidebar--collapsed .brand-name,
.sidebar--collapsed .brand-subtitle {
  display: none;
}

.sidebar--collapsed .sidebar-brand {
  padding: var(--space-3, 0.75rem);
  min-height: 40px;
  justify-content: center;
}

.sidebar--collapsed .nav-label {
  display: none;
}

.sidebar--collapsed .nav-item {
  justify-content: center;
  padding: 0.625rem;
  gap: 0;
}

.sidebar--collapsed .sidebar-footer {
  align-items: center;
}

.sidebar--collapsed .sidebar-footer :deep(.language-label),
.sidebar--collapsed .sidebar-footer :deep(.profile-name),
.sidebar--collapsed .sidebar-footer :deep(.chevron) {
  display: none;
}

.sidebar--collapsed .sidebar-footer :deep(.language-button),
.sidebar--collapsed .sidebar-footer :deep(.profile-button) {
  justify-content: center;
  padding: 0.5rem;
  width: 100%;
}

/* Center the toggle button icon when rail is collapsed */
.sidebar--collapsed .sidebar-toggle {
  justify-content: center;
  padding: 0.5rem;
}

.sidebar--collapsed .toggle-label {
  display: none;
}

/* ── Small-screen responsive rail (forced, regardless of isCollapsed) ─────── */

@media (max-width: 900px) {
  .sidebar {
    width: var(--sidebar-rail-width, 72px);
  }

  /* Hide all brand text */
  .brand-name,
  .brand-subtitle {
    display: none;
  }

  .sidebar-brand {
    padding: var(--space-3, 0.75rem);
    min-height: 40px;
    justify-content: center;
  }

  .nav-label {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: 0.625rem;
    gap: 0;
  }

  .sidebar-footer {
    align-items: center;
  }

  /* Pierce child component scoped styles */
  .sidebar-footer :deep(.language-label),
  .sidebar-footer :deep(.profile-name),
  .sidebar-footer :deep(.chevron) {
    display: none;
  }

  .sidebar-footer :deep(.language-button),
  .sidebar-footer :deep(.profile-button) {
    justify-content: center;
    padding: 0.5rem;
    width: 100%;
  }

  /* Hide the manual toggle on small screens — rail is always forced here */
  .sidebar-toggle-row {
    display: none;
  }
}
</style>
