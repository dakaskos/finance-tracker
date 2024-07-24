<template>
  <div class="pa-4 text-center">
    <v-btn
      color="primary"
      prepend-icon="mdi-plus"
      variant="tonal"
      @click="openDialog(null)"
    >
      Добавить
    </v-btn>
    <v-dialog v-model="transactionFormDialog" max-width="600" style="bottom: -500px;">
      <v-form method="post" v-model="valid" action>
        <v-card prepend-icon="mdi-cash" :title=title>
          <v-card-text>
            <v-row dense>
              <v-col cols="12" md="6" sm="6">
                <input
                  v-model="transactionForm.id"
                  type="hidden"
                ></input>
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
                  item-title="currency"
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
              v-if = "transactionForm.id"
              color="red-lighten-2"
              variant="tonal"
              @click="deleteTransaction"
              :disabled="!valid"
            >
              Удалить
            </v-btn>
            <v-btn
              color="primary"
              variant="tonal"
              @click="submitForm"
              :disabled="!valid"
            >
              Добавить
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
    title: String,
  },
  data: () => ({
    transactionFormDialog: false,
    datePickerDialog: false,
    valid: false,
    transactionForm: {
      id: null,
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
    openDialog(id) {
      if (id === null) {
        this.resetForm();
        this.transactionFormDialog = true;
        return;
      }
      axios.get(window.django_host + `/api/transaction/${id}/`).then((response) => {
        this.transactionForm = response.data;
        this.transactionForm.date = this.transactionForm.date.split('T')[0].split('-').reverse().join('.');
        this.transactionFormDialog = true;
      });
    },
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
    async deleteTransaction() {
      try {
        await axios.delete(
          window.django_host + `/api/transaction/${this.transactionForm.id}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          }
        );
        this.transactionFormDialog = false;
        this.$emit('update-income-transactions');
        this.$emit('update-outcome-transactions');
        this.$emit('update-balance');
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async submitForm() {
      try {
        const formattedDate = this.transactionForm.date.split('.').reverse().join('-')
        const data = {
          amount: this.transactionForm.amount,
          account: this.transactionForm.account,
          description: this.transactionForm.description,
          type: this.type,
          date: formattedDate,
          user: 1, // TODO: replace with the logged-in user
        }
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        }

        if (this.transactionForm.id) {
          await axios.put(
            window.django_host + `/api/transaction/${this.transactionForm.id}/`,
            data,
            config
          );
          this.transactionFormDialog = false;
        } else {
          const response = await axios.post(
            window.django_host + '/api/transaction/',
            data,
            config
          );
        }

        this.transactionForm = {
          id: null,
          amount: null,
          account: this.transactionForm.account,
          description: null,
          date: this.transactionForm.date,
        };

        if (this.type === 1) {
          this.$emit('update-income-transactions')
        } else {
          this.$emit('update-outcome-transactions');
        }

        this.$emit('update-balance');
      } catch (error) {
        console.error('Error:', error);
      }
    },
    resetForm() {
      this.transactionForm = {
          amount: null,
          account: null,
          description: null,
          date: this.getTodayDate(),
      };
    },
    getTodayDate() {
      const today = new Date();
      const dd = String(today.getDate()).padStart(2, '0');
      const mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
      const yyyy = today.getFullYear();
      return `${dd}.${mm}.${yyyy}`;
    }
  },
};
</script>
