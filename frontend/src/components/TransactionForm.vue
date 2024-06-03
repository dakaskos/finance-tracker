<template>
  <div class="pa-4 text-center">
    <v-btn
      color="primary"
      prepend-icon="mdi-plus"
      variant="tonal"
      @click="dialog = true"
    >
      Add
    </v-btn>
    <v-dialog v-model="dialog" max-width="600">
      <v-form method="post" v-model="valid" action>
        <v-card prepend-icon="mdi-cash" title="Add">
          <v-card-text>
            <v-row dense>
              <v-col cols="12" md="4" sm="6">
                <v-autocomplete
                  v-model="transactionForm.category"
                  label="Category"
                  :items="categories"
                  item-title="name"
                  item-value="id"
                ></v-autocomplete>
              </v-col>

              <v-col cols="12" md="4" sm="6">
                <v-text-field
                  v-model="transactionForm.amount"
                  :counter="10"
                  :rules="positiveNumberRules"
                  label="Amount"
                  hide-details
                  type="number"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="4" sm="6">
                <v-select
                  v-model="transactionForm.account"
                  label="Account"
                  :items="accounts"
                  item-title="name"
                  item-value="id"
                  ></v-select>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col cols="12" md="12" sm="12">
                <v-text-field
                  v-model="transactionForm.description"
                  label="Description"
                  hide-details
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              variant="tonal"
              @click="submitForm"
              :disabled="!valid"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TransactionForm",
  props: {
    categories: Array, // TODO: add type checking
    accounts: Array, // TODO: add type checking
    type: Number,
  },
  data: () => ({
    dialog: false,
    valid: false,
    transactionForm: {
      category: null,
      amount: null,
      account: null,
      description: null,
    },
    positiveNumberRules: [
      (v) => !!v || "Amount is required",
      (v) => (v && v > 0) || "Amount must be greater than 0",
    ],
  }),
  methods: {
    async submitForm() {
      try {
          const response = await axios.post(
            'http://127.0.0.1:8000/api/transaction/',
            {
              category: this.transactionForm.category,
              amount: this.transactionForm.amount,
              account: this.transactionForm.account,
              description: this.transactionForm.description,
              type: this.type,
              user: 1, // TODO: replace with the logged-in user
            }
          );

          this.transactionForm = {
            category: null,
            amount: null,
            account: null,
            description: null,
          };

          if (this.type === 1) {
            console.log('Income transaction')
            this.$emit('update-income-transactions')
          } else {
            console.log('Outcome transaction')
            this.$emit('update-outcome-transactions');
          }
          // this.dialog = false;
        console.log('Response:', response.data);
        } catch (error) {
          console.error('Error:', error);
        }
    },
  },
};
</script>
