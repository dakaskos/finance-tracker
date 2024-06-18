<script setup>

</script>

<template>
  <v-row dense>
    <v-btn class="btn-danger" @click="getLastWeek()">За неделю</v-btn>
    <v-btn @click="getThisMonth()">За текущий месяц</v-btn>
    <v-btn @click="getThisYear()">За текущий год</v-btn>
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
    getThisYear() {
      const today = new Date();
      let year_beginning = new Date(today.getFullYear(), 0, 1);
      this.$emit('update-period', year_beginning, today);
    },
    getThisMonth() {
      const today = new Date();
      let month_ago = new Date(today.getFullYear(), today.getMonth(), 1);
      this.$emit('update-period', month_ago, today);
    },
    getAll() {
      this.$emit('update-period', null, null);
    },
  },
};
</script>
