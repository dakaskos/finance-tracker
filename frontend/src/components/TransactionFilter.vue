<script setup>

</script>

<template>
  <v-row dense>
    <v-btn class="btn-danger" @click="getLastWeek()">Last Week</v-btn>
    <v-btn @click="getThisMonth()">This Month</v-btn>
    <v-btn @click="dialog = true">Select Period</v-btn>
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
      console.log("Last Week");
    },
    getThisMonth() {
      console.log("This Month");
    },
  },
};
</script>
