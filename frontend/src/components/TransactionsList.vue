<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <TransactionForm
        :categories="categories"
        :accounts="accounts"
        :type="type"
        class="text-right"
        @update-income-transactions="updateIncomeTransactions"
        @update-outcome-transactions="updateOutcomeTransactions"
      />
    </v-toolbar>

    <v-table>
      <thead>
        <tr>
          <th class="text-left">
            Date
          </th>
          <th class="text-left">
            Amount
          </th>
          <th class="text-left">
            Currency
          </th>
          <th class="text-left">
            Description
          </th>
          <th class="text-left">
            Category
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="transaction in transactions"
          :key="transaction.id"
        >
          <td>{{ formatDate(transaction.created_at) }}</td>
          <td>{{ transaction.amount }}</td>
          <td>{{ transaction.currency }} {{ isAccountCash(transaction) }}</td>
          <td>{{ transaction.description }}</td>
          <td>{{ transaction.category_name }}</td>
        </tr>
      </tbody>
    </v-table>
  </v-card>
</template>

<script>
import moment from "moment";
import TransactionForm from "@/components/TransactionForm.vue";
export default {
  name: "TransactionsList",
  components: {
    TransactionForm,
  },
  props: {
    transactions: Array, // TODO: add type checking
    categories: Array, // TODO: add type checking
    accounts: Array, // TODO: add type checking
    title: String,
    type: Number,
  },
  methods: {
    isAccountCash(transaction) {
      return transaction.is_cash === 1 ? "Cash" : "Bank";
    },
    formatDate(date) {
      return moment(date).format("DD.MM.YY");
    },
    updateIncomeTransactions() {
      this.$emit("update-income-transactions")
    },
    updateOutcomeTransactions() {
      this.$emit("update-outcome-transactions")
    },
  },
};
</script>
