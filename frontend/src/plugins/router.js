import { createRouter } from 'vue-router'
import BudgetList from "@/components/BudgetList.vue";

const routes = [
  { path: '/', component: BudgetList },
]

export default function(history) {
  return createRouter({
    history,
    routes
  })
}
