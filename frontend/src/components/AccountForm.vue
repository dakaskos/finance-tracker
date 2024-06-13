<template>

    <v-btn
      color="primary"
      prepend-icon="mdi-plus"
      variant="tonal"
      @click="dialog = true"
    >
      Новый счет
    </v-btn>
    <v-dialog v-model="dialog" max-width="600">
      <v-form method="post" v-model="valid" action>
        <v-card prepend-icon="mdi-bank" title="Добавить счет">
          <v-card-text>
            <v-row dense>
              <v-col cols="12" md="4" sm="6">
                <v-text-field
                  v-model="accountForm.balance"
                  :counter="10"
                  :rules="positiveNumberRules"
                  label="Сумма"
                  hide-details
                  type="number"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="4" sm="6">
                <v-select
                  v-model="accountForm.currency"
                  label="Валюта"
                  :items="['USD', 'PLN', 'EUR']"
                  required></v-select>
              </v-col>

              <v-col cols="12" md="4" sm="6">
                <v-checkbox
                  v-model="accountForm.is_cash"
                  label="Наличка">
                </v-checkbox>
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
            >
              Сохранить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-dialog>
</template>

<script>
import axios from "axios";

export default {
  name: "AccountForm",
  data: () => ({
    dialog: false,
    valid: false,
    accountForm: {
      currency: "",
      is_cash: false,
      balance: 0,
    },
    positiveNumberRules: [
      (v) => !!v || "Amount is required",
      (v) => (v && v >= 0) || "Amount must be greater than 0",
    ],
  }),
  methods: {
    async submitForm() {
      try {
          const response = await axios.post(
            window.django_host + '/api/account/',
            {
              currency: this.accountForm.currency,
              is_cash: this.accountForm.is_cash,
              balance: this.accountForm.balance,
              user: 1, // TODO: replace with the logged-in user
            }
          );
          this.dialog = false;
          this.$emit('update-accounts');
          console.log('Response:', response.data);
        } catch (error) {
          console.error('Error:', error);
        }
    },
  },
};
</script>
