<template>
  <div class="pa-4 text-center">
    <v-btn
      color="primary"
      prepend-icon="mdi-plus"
      variant="tonal"
      @click="transactionFormDialog = true"
    >
      Добавить
    </v-btn>
    <v-dialog v-model="transactionFormDialog" max-width="600">
      <v-form method="post" v-model="valid" action>
        <v-card prepend-icon="mdi-cash" title="Добавить">
          <v-card-text>
            <v-row dense>
              <v-col cols="12" md="6" sm="6">
                <v-text-field
                  v-model="transactionForm.amount"
                  :counter="10"
                  :rules="positiveNumberRules"
                  label="Сумма"
                  hide-details
                  type="number"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6" sm="6">
                <v-select
                  v-model="transactionForm.account"
                  label="Счет"
                  :items="accounts"
                  item-title="name"
                  item-value="id"
                ></v-select>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col cols="12" md="6" sm="6">
                <v-text-field
                  v-model="transactionForm.description"
                  label="Описание"
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6" sm="6">
                <v-text-field
                  v-model="transactionForm.date"
                  label="Дата"
                  hide-details
                  @click="datePickerDialog = true"
                  readonly
                ></v-text-field>
                <v-dialog v-model="datePickerDialog" max-width="300">
                  <v-date-picker
                    v-model="date"
                    color="primary"
                    @update:modelValue="saveDate"
                    locale="ru"
                  ></v-date-picker>
                </v-dialog>
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
              Сохранить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";
import DatePicker from "@/components/DatePicker.vue";

export default {
  name: "TransactionForm",
  components: {DatePicker},
  props: {
    accounts: Array, // TODO: add type checking
    type: Number,
  },
  data: () => ({
    transactionFormDialog: false,
    datePickerDialog: false,
    valid: false,
    transactionForm: {
      amount: null,
      account: null,
      description: null,
      date: null,
    },
    date: null,
    positiveNumberRules: [
      (v) => !!v || "Amount is required",
      (v) => (v && v > 0) || "Amount must be greater than 0",
    ],
  }),
  methods: {
    saveDate() {
      let day = this.date.getDate();
      if (day < 10) {
        day = `0${day}`;
      }
      let month = this.date.getMonth() + 1;
      if (month < 10) {
        month = `0${month}`;
      }
      const year = this.date.getFullYear();
      this.transactionForm.date = `${day}.${month}.${year}`;
      this.datePickerDialog = false;
    },
    async submitForm() {
      try {
        const formattedDate = this.transactionForm.date.split('.').reverse().join('-')
        const response = await axios.post(
          window.django_host + '/api/transaction/',
          {
            amount: this.transactionForm.amount,
            account: this.transactionForm.account,
            description: this.transactionForm.description,
            type: this.type,
            date: formattedDate,
            user: 1, // TODO: replace with the logged-in user
          }
        );

        this.transactionForm = {
          amount: null,
          account: this.transactionForm.account,
          description: null,
          date: this.transactionForm.date,
        };

        if (this.type === 1) {
          console.log('Income transaction')
          this.$emit('update-income-transactions')
        } else {
          console.log('Outcome transaction')
          this.$emit('update-outcome-transactions');
        }

        this.$emit('update-balance');

        console.log('Response:', response.data);
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
  mounted() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    this.transactionForm.date = dd + '.' + mm + '.' + yyyy;
  }
};
</script>
