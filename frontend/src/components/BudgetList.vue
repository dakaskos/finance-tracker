<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <CategoryForm @update-categories="getCategories" />
        <AccountForm @update-accounts="getAccounts" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <TransactionsList
          title="Income"
          :transactions="incomeTransactions"
          :categories="categories"
          :accounts="accounts"
          :type=1
          @update-income-transactions="getIncomeTransactions"
        />
      </v-col>
      <v-col cols="6">
        <TransactionsList
          title="Outcome"
          :transactions="outcomeTransactions"
          :categories="categories"
          :accounts="accounts"
          :type=-1
          @update-outcome-transactions="getOutcomeTransactions"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import TransactionsList from "@/components/TransactionsList.vue";
import CategoryForm from "@/components/CategoryForm.vue";
import AccountForm from "@/components/AccountForm.vue";
export default {
  name: "BudgetList",
  components: {
    AccountForm,
    TransactionsList,
    CategoryForm,
  },

  data: () => ({
    incomeTransactions: [],
    outcomeTransactions: [],
    categories: [],
    accounts: [],
  }),
  mounted() {
    this.getCategories();
    this.getIncomeTransactions();
    this.getOutcomeTransactions();
    this.getAccounts();
  },
  methods: {
    getIncomeTransactions() {
      console.log("getIncomeTransactions")
      axios
        .get("http://127.0.0.1:8000/api/transaction/", {
          params: {
            user: 1, // TODO: replace with the logged-in user
            type: 1,
            ordering: "-created_at",
          },
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
      console.log(this.outcomeTransactions)
      axios
        .get("http://127.0.0.1:8000/api/transaction/", {
          params: {
            user: 1, // TODO: replace with the logged-in user
            type: -1,
            ordering: "-created_at",
          },
        })
        .then((response) => {
          this.outcomeTransactions = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getCategories() {
      axios
      .get("http://127.0.0.1:8000/api/category/", {
        params: {
          user: 1, // TODO: replace with the logged-in user
        },
      })
      .then((response) => {
        this.categories = response.data;
        // this.categories = [...response.data.map((category) => category.name)];
      })
      .catch((error) => {
        console.log(error);
      });
    },
    getAccounts() {
      axios
      .get("http://127.0.0.1:8000/api/account/", {
        params: {
          user: 1, // TODO: replace with the logged-in user
        },
      })
      .then((response) => {
        for (let account of response.data) {
          this.accounts.push({
            id: account.id,
            name: account.balance + " " + account.currency + " " + (account.is_cash ? "Cash" : "Bank"),
          });
        }
      })
      .catch((error) => {
        console.log(error);
      });
    }
  },
  watch: {
    incomeTransactions: function() {
      console.log("Income transactions updated");
    },
    outcomeTransactions: function() {
      console.log("Outcome transactions updated");
    },
  },
};
</script>
