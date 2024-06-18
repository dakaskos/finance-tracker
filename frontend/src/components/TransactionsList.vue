<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <TransactionForm
        :accounts="accounts"
        :type="type"
        class="text-right"
        @update-income-transactions="updateIncomeTransactions"
        @update-outcome-transactions="updateOutcomeTransactions"
        @update-balance="updateBalance"
      />
    </v-toolbar>

    <v-table>
      <thead>
        <tr>
          <th class="text-left">
            Дата
          </th>
          <th class="text-left">
            Сумма
          </th>
          <th class="text-left">
            Валюта
          </th>
          <th class="text-left">
            Описание
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="transaction in transactions"
          :key="transaction.id"
          :class="currencyColor(transaction.currency)"
        >
          <td><strong>{{ formatDate(transaction.date) }}</strong></td>
          <td>{{ formatNumber(transaction.amount) }}</td>
          <td>{{ transaction.currency }} {{ isAccountCash(transaction) }}</td>
          <td><strong>{{ transaction.description }}</strong></td>
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
    accounts: Array, // TODO: add type checking
    title: String,
    type: Number,
  },
  methods: {
    isAccountCash(transaction) {
      return transaction.is_cash === 1 ? "Наличка" : "Счет";
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
    updateBalance() {
      this.$emit("update-balance")
    },
    currencyColor(currency) {
      if (currency.includes("EUR")) {
        return "bg-amber-lighten-4";
      } else if (currency.includes("USD")) {
        return "bg-light-green-lighten-4";
      }

      return "bg-grey-lighten-4";
    },
    formatNumber(value) {
      return this.$filters.numberWithSpaces(value);
    },
  },
};
</script>
