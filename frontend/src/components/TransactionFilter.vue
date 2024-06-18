<script setup>

</script>

<template>
  <v-row dense>
    <v-btn class="btn-danger" @click="getLastWeek()">За неделю</v-btn>
    <v-btn @click="getThisMonth()">За месяц</v-btn>
    <v-btn @click="getSixMonths()">За 6 месяцев</v-btn>
    <v-btn @click="getAll()">За весь период</v-btn>
  </v-row>
</template>

<script>
export default {
  name: "TransactionFilter",
  data: () => ({
    dialog: false,
  }),
  methods: {
    getLastWeek() {
      const today = new Date();
      let week_ago = new Date();
      week_ago.setDate(today.getDate() - 7);
      this.$emit('update-period', week_ago, today);
    },
    getThisMonth() {
      const today = new Date();
      let month_ago = new Date();
      month_ago.setMonth(today.getMonth() - 1);
      this.$emit('update-period', month_ago, today);
    },
    getSixMonths() {
      const today = new Date();
      let six_months_ago = new Date();
      six_months_ago.setMonth(today.getMonth() - 6);
      this.$emit('update-period', six_months_ago, today);
    },
    getAll() {
      this.$emit('update-period', null, null);
    },
  },
};
</script>
