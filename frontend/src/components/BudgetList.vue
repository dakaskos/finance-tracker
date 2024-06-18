<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <AccountForm @update-accounts="getAccounts" />
      </v-col>
    </v-row>
    <v-row>
      <v-col class="border text-center" :class="currencyColor(account.currency)" cols="4" v-for="account in accounts">
        <h2>{{ account.name }} </h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <TransactionFilter @update-period="updatePeriod" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <TransactionsList
          title="Приходы"
          :transactions="incomeTransactions"
          :accounts="accounts"
          :type=1
          @update-income-transactions="getTransactions"
          @update-balance="getAccounts"
        />
      </v-col>
      <v-col cols="6">
        <TransactionsList
          title="Расходы"
          :transactions="outcomeTransactions"
          :accounts="accounts"
          :type=-1
          @update-outcome-transactions="getTransactions"
          @update-balance="getAccounts"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import TransactionsList from "@/components/TransactionsList.vue";
import AccountForm from "@/components/AccountForm.vue";
import TransactionFilter from "@/components/TransactionFilter.vue";
export default {
  name: "BudgetList",
  components: {
    TransactionFilter,
    AccountForm,
    TransactionsList,
  },

  data: () => ({
    incomeTransactions: [],
    outcomeTransactions: [],
    accounts: [],
    date_to: null,
    date_from: null,
  }),
  mounted() {
    const today = new Date();
    let month_ago = new Date();
    month_ago.setMonth(today.getMonth() - 1);
    this.date_to = today
    this.date_from = month_ago

    this.getTransactions();
    this.getAccounts();
  },
  methods: {
    updatePeriod(date_from, date_to) {
      console.log(date_from)
      console.log(date_to)
      this.date_from = date_from;
      this.date_to = date_to;
      this.getTransactions();
    },
    getTransactions() {
      this.incomeTransactions = [];
      this.outcomeTransactions = [];
      let params = {
        user: 1, // TODO: replace with the logged-in user
        ordering: "-date,-id",
      };
      if (this.date_from) {
        params.start_date = this.formatDate(this.date_from);
      }
      if (this.date_to) {
        params.end_date = this.formatDate(this.date_to);
      }
      axios
        .get(window.django_host + "/api/transaction/", {
          params: params,
        })
        .then((response) => {
          response.data.forEach((transaction) => {
            if (transaction.type === 1) {
              this.incomeTransactions.push(transaction);
            } else {
              this.outcomeTransactions.push(transaction);
            }
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getIncomeTransactions() {
      console.log("getIncomeTransactions")
      let params = {
        user: 1, // TODO: replace with the logged-in user
        type: 1, // TODO: replace with constant
        ordering: "-date,-id",
      };
      if (this.date_from) {
        params.start_date = this.formatDate(this.date_from);
      }
      if (this.date_to) {
        params.end_date = this.formatDate(this.date_to);
      }
      axios
        .get(window.django_host + "/api/transaction/", {
          params: params,
        })
        .then((response) => {
          this.incomeTransactions = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getOutcomeTransactions() {
      console.log("getOutcomeTransactions")
      let params = {
        user: 1, // TODO: replace with the logged-in user
        type: -1, // TODO: replace with constant
        ordering: "-date,-id",
      };
      if (this.date_from) {
        params.start_date = this.formatDate(this.date_from);
      }
      if (this.date_to) {
        params.end_date = this.formatDate(this.date_to);
      }
      axios
        .get(window.django_host + "/api/transaction/", {
          params: params,
        })
        .then((response) => {
          this.outcomeTransactions = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getAccounts() {
      axios
      .get(window.django_host + "/api/account/", {
        params: {
          user: 1, // TODO: replace with the logged-in user
        },
      })
      .then((response) => {
        this.accounts = [];
        const currencyOrder = {
          "PLN": 0,
          "USD": 1,
          "EUR": 2,
        }

        for (let account of response.data) {
          this.accounts.push({
            id: account.id,
            name: this.formatNumber(account.balance) + " " + account.currency + " " + (account.is_cash ? "Наличка" : "Счет"),
            currency: account.currency + " " + (account.is_cash ? "Наличка" : "Счет"),
            order: currencyOrder[account.currency],
          });
        }
        // Accounts order by business requirements PLN, USD, EUR
        this.accounts.sort((a, b) => {
          if (a.order < b.order) {
            return -1;
          }
          if (a.order > b.order) {
            return 1;
          }
          return 0;
        });
      })
      .catch((error) => {
        console.log(error);
      });
    },
    formatNumber(value) {
      return this.$filters.numberWithSpaces(value);
    },
    formatDate(date) {
      console.log("test=", date)
      const yyyy = date.getFullYear();
      let mm = date.getMonth() + 1; // Months start at 0!
      let dd = date.getDate();

      if (dd < 10) dd = '0' + dd;
      if (mm < 10) mm = '0' + mm;

      return yyyy + '-' + mm + '-' + dd;
    },
    currencyColor(currency) {
      if (currency.includes("EUR")) {
        return "bg-amber-lighten-4";
      } else if (currency.includes("USD")) {
        return "bg-light-green-lighten-4";
      }

      return "bg-grey-lighten-4";
    },
  },
  watch: {
    incomeTransactions: function() {
      console.log("Income transactions updated");
    },
    outcomeTransactions: function() {
      console.log("Outcome transactions updated");
    },
    updatePeriod: function() {
      console.log("Period updated");
    },
  },
};
</script>
