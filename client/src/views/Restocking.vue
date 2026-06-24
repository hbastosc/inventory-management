<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error && !orderSuccess" class="error">{{ error }}</div>
    <div v-else>
      <!-- Success banner shown after a successful order -->
      <div v-if="orderSuccess" class="success-banner">
        {{ orderSuccess }}
      </div>

      <!-- Budget slider section -->
      <div class="card budget-card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.budgetLabel') }}</h3>
          <span class="budget-display">{{ currencySymbol }}{{ budget.toLocaleString() }}</span>
        </div>
        <div class="budget-slider-wrap">
          <span class="budget-bound">{{ currencySymbol }}0</span>
          <input
            type="range"
            min="0"
            :max="maxBudget"
            step="100"
            v-model.number="budget"
            class="budget-slider"
          />
          <span class="budget-bound">{{ currencySymbol }}{{ maxBudget.toLocaleString() }}</span>
        </div>
      </div>

      <!-- Summary stats -->
      <div class="stats-grid">
        <div class="stat-card info">
          <div class="stat-label">{{ t('restocking.selected') }}</div>
          <div class="stat-value">{{ includedRows.length }}</div>
        </div>
        <div class="stat-card" :class="isOverBudget ? 'danger' : 'success'">
          <div class="stat-label">{{ t('restocking.totalCost') }}</div>
          <div class="stat-value">{{ currencySymbol }}{{ totalCost.toLocaleString() }}</div>
        </div>
        <div class="stat-card" :class="remaining >= 0 ? 'success' : 'danger'">
          <div class="stat-label">{{ t('restocking.remaining') }}</div>
          <div class="stat-value">{{ currencySymbol }}{{ Math.abs(remaining).toLocaleString() }}</div>
        </div>
      </div>

      <!-- Budget status indicator -->
      <div class="budget-status" :class="isOverBudget ? 'over' : 'within'">
        {{ isOverBudget ? t('restocking.overBudget') : t('restocking.withinBudget') }}
        <span class="lead-time-note">{{ t('restocking.leadTimeNote', { days: 14 }) }}</span>
      </div>

      <!-- Recommendations table -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.recommendations') }}</h3>
          <!-- Place Order button placed in card header for layout balance -->
          <button
            class="place-order-btn"
            :disabled="includedRows.length === 0 || isOverBudget || submitting"
            @click="placeOrder"
          >
            {{ submitting ? t('restocking.placing') : t('restocking.placeOrder') }}
          </button>
        </div>

        <!-- Order error message -->
        <div v-if="orderError" class="error order-error">{{ orderError }}</div>

        <div v-if="rows.length === 0" class="no-data">
          {{ t('restocking.noRecommendations') }}
        </div>
        <div v-else class="table-container">
          <table class="restock-table">
            <thead>
              <tr>
                <th class="col-include">{{ t('restocking.table.include') }}</th>
                <th class="col-item">{{ t('restocking.table.item') }}</th>
                <th class="col-trend">{{ t('restocking.table.trend') }}</th>
                <th class="col-qty">{{ t('restocking.table.quantity') }}</th>
                <th class="col-unit-cost">{{ t('restocking.table.unitCost') }}</th>
                <th class="col-line-cost">{{ t('restocking.table.lineCost') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in rows"
                :key="row.item_sku"
                :class="{ 'row-excluded': !row.included }"
              >
                <td class="col-include">
                  <input
                    type="checkbox"
                    v-model="row.included"
                    class="row-checkbox"
                  />
                </td>
                <td class="col-item">
                  <span class="item-sku">{{ row.item_sku }}</span>
                  <span class="item-name">{{ translateProductName(row.item_name) }}</span>
                </td>
                <td class="col-trend">
                  <span class="badge" :class="getTrendClass(row.trend)">{{ row.trend }}</span>
                </td>
                <td class="col-qty">
                  <input
                    type="number"
                    min="0"
                    v-model.number="row.quantity"
                    class="qty-input"
                  />
                </td>
                <td class="col-unit-cost">
                  {{ currencySymbol }}{{ row.unit_cost.toLocaleString() }}
                </td>
                <td class="col-line-cost">
                  <strong>{{ currencySymbol }}{{ getLineCost(row).toLocaleString() }}</strong>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'

export default {
  name: 'Restocking',
  setup() {
    const { t, currentCurrency, translateProductName } = useI18n()

    const currencySymbol = computed(() => {
      return currentCurrency.value === 'JPY' ? '¥' : '$'
    })

    const loading = ref(true)
    const error = ref(null)
    // Immutable fetched recommendations
    const recommendations = ref([])
    // Editable rows derived from recommendations
    const rows = ref([])

    // Budget state
    const budget = ref(0)

    // Order submission state
    const submitting = ref(false)
    const orderSuccess = ref(null)
    const orderError = ref(null)

    // Safely compute line cost, treating NaN/empty quantity as 0
    const getLineCost = (row) => {
      const qty = typeof row.quantity === 'number' && !isNaN(row.quantity) ? row.quantity : 0
      return qty * row.unit_cost
    }

    // Max budget = sum of all recommended line costs
    const maxBudget = computed(() => {
      const total = rows.value.reduce((sum, row) => sum + row.recommended_quantity * row.unit_cost, 0)
      return Math.max(Math.ceil(total), 1000)
    })

    const includedRows = computed(() => rows.value.filter(r => r.included))

    const totalCost = computed(() => {
      return includedRows.value.reduce((sum, row) => sum + getLineCost(row), 0)
    })

    const remaining = computed(() => budget.value - totalCost.value)

    const isOverBudget = computed(() => totalCost.value > budget.value)

    // Map trend string to badge class
    const getTrendClass = (trend) => {
      if (!trend) return 'info'
      const t = trend.toLowerCase()
      if (t === 'increasing') return 'success'
      if (t === 'decreasing') return 'danger'
      return 'info'
    }

    // Greedy auto-selection: walk rows in priority order, include while cumulative cost <= budget
    const applyBudgetGreedy = () => {
      let cumulative = 0
      rows.value.forEach(row => {
        const cost = getLineCost(row)
        if (cumulative + cost <= budget.value) {
          row.included = true
          cumulative += cost
        } else {
          row.included = false
        }
      })
    }

    // Re-run greedy whenever budget slider moves
    watch(budget, () => {
      applyBudgetGreedy()
    })

    const loadRecommendations = async () => {
      loading.value = true
      error.value = null
      orderSuccess.value = null
      orderError.value = null
      try {
        const data = await api.getRestockRecommendations()
        recommendations.value = data

        // Build editable rows from fetched data
        rows.value = data.map(rec => ({
          ...rec,
          included: false,
          // Use recommended_quantity as the initial editable quantity
          quantity: rec.recommended_quantity
        }))

        // Initialize budget to ~50% of max — maxBudget computed is valid now that rows.value is set
        budget.value = Math.round(maxBudget.value * 0.5 / 100) * 100

        // Apply initial greedy selection
        applyBudgetGreedy()
      } catch (err) {
        error.value = 'Failed to load restock recommendations: ' + err.message
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const placeOrder = async () => {
      if (includedRows.value.length === 0 || isOverBudget.value || submitting.value) return

      submitting.value = true
      orderError.value = null
      orderSuccess.value = null

      try {
        const items = includedRows.value
          .map(r => ({
            item_sku: r.item_sku,
            item_name: r.item_name,
            quantity: typeof r.quantity === 'number' && !isNaN(r.quantity) ? r.quantity : 0,
            unit_cost: r.unit_cost
          }))
          // Safety net: drop zero-quantity rows the backend would reject
          .filter(r => r.quantity > 0)

        // Nothing to submit after filtering — bail out silently
        if (items.length === 0) return

        const payload = { items }
        const created = await api.createRestockingOrder(payload)
        // Reload recommendations first (resets rows/selection), then set success message
        // so loadRecommendations' internal null-reset does not wipe it
        await loadRecommendations()
        orderSuccess.value = t('restocking.orderSuccess', { orderNumber: created.order_number })
      } catch (err) {
        orderError.value = t('restocking.orderError')
        console.error(err)
      } finally {
        submitting.value = false
      }
    }

    onMounted(loadRecommendations)

    return {
      t,
      loading,
      error,
      rows,
      budget,
      maxBudget,
      currencySymbol,
      includedRows,
      totalCost,
      remaining,
      isOverBudget,
      submitting,
      orderSuccess,
      orderError,
      getTrendClass,
      getLineCost,
      placeOrder,
      translateProductName
    }
  }
}
</script>

<style scoped>
/* Budget card */
.budget-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.budget-display {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2563eb;
  letter-spacing: -0.025em;
}

.budget-slider-wrap {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 0 0.25rem;
}

.budget-bound {
  font-size: 0.813rem;
  color: #64748b;
  white-space: nowrap;
}

/* Range slider styling */
.budget-slider {
  flex: 1;
  -webkit-appearance: none;
  appearance: none;
  height: 6px;
  border-radius: 3px;
  background: #e2e8f0;
  outline: none;
  cursor: pointer;
}

.budget-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2563eb;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(37, 99, 235, 0.4);
  transition: transform 0.15s ease;
}

.budget-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.budget-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2563eb;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(37, 99, 235, 0.4);
}

/* Budget status bar */
.budget-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.625rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
}

.budget-status.within {
  background: #d1fae5;
  color: #065f46;
}

.budget-status.over {
  background: #fecaca;
  color: #991b1b;
}

.lead-time-note {
  font-size: 0.813rem;
  font-weight: 400;
  opacity: 0.85;
}

/* Table */
.restock-table {
  table-layout: fixed;
  width: 100%;
}

.col-include {
  width: 72px;
  text-align: center;
}

.col-item {
  width: 240px;
}

.col-trend {
  width: 110px;
}

.col-qty {
  width: 120px;
}

.col-unit-cost {
  width: 110px;
}

.col-line-cost {
  width: 120px;
}

/* Checkbox */
.row-checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #2563eb;
}

/* Item display */
.col-item {
  display: table-cell;
}

.item-sku {
  display: block;
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
  letter-spacing: 0.025em;
}

.item-name {
  display: block;
  font-size: 0.875rem;
  color: #0f172a;
  font-weight: 500;
}

/* Quantity input */
.qty-input {
  width: 90px;
  padding: 0.375rem 0.5rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #0f172a;
  background: #f8fafc;
  transition: border-color 0.2s;
}

.qty-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Excluded row dimming */
.row-excluded td {
  opacity: 0.45;
}

.row-excluded td:first-child {
  opacity: 1;
}

/* Success banner */
.success-banner {
  background: #d1fae5;
  border: 1px solid #6ee7b7;
  color: #065f46;
  padding: 0.875rem 1.25rem;
  border-radius: 8px;
  margin-bottom: 1.25rem;
  font-size: 0.938rem;
  font-weight: 500;
}

/* Order error */
.order-error {
  margin: 0.5rem 1.25rem 0.75rem;
}

/* No data state */
.no-data {
  padding: 2.5rem;
  text-align: center;
  color: #64748b;
  font-size: 0.938rem;
}

/* Place Order button — matches TasksModal .task-add-btn style */
.place-order-btn {
  padding: 0.625rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.938rem;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
  white-space: nowrap;
}

.place-order-btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.place-order-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
</style>
