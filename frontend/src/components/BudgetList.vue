<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <AccountForm @update-accounts="getAccounts" />
      </v-col>
    </v-row>
    <v-row>
      <v-col class="border text-center" cols="4" v-for="account in accounts">
        <h2>{{ account.name }} </h2>
      </v-col>
    </v-row>
<!--    <v-row>-->
<!--      <v-col cols="12">-->
<!--        <TransactionFilter />-->
<!--      </v-col>-->
<!--    </v-row>-->
    <v-row>
      <v-col cols="6">
        <TransactionsList
          title="Приходы"
          :transactions="incomeTransactions"
          :accounts="accounts"
          :type=1
          @update-income-transactions="getIncomeTransactions"
          @update-balance="getAccounts"
        />
      </v-col>
      <v-col cols="6">
        <TransactionsList
          title="Расходы"
          :transactions="outcomeTransactions"
          :accounts="accounts"
          :type=-1
          @update-outcome-transactions="getOutcomeTransactions"
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
  }),
  mounted() {
    this.getIncomeTransactions();
    this.getOutcomeTransactions();
    this.getAccounts();
  },
  methods: {
    getIncomeTransactions() {
      console.log("getIncomeTransactions")
      axios
        .get(window.django_host + "/api/transaction/", {
          params: {
            user: 1, // TODO: replace with the logged-in user
            type: 1, // TODO: replace with constant
            ordering: "-date,-id",
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
        .get(window.django_host + "/api/transaction/", {
          params: {
            user: 1, // TODO: replace with the logged-in user
            type: -1, // TODO: replace with constant
            ordering: "-date,-id",
          },
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
        for (let account of response.data) {
          this.accounts.push({
            id: account.id,
            name: account.balance + " " + account.currency + " " + (account.is_cash ? "Наличка" : "Счет"),
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
