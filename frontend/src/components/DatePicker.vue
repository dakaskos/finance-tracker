<template>
  <v-text-field
    v-model="date"
    label="Дата"
    hide-details
    @click="dialog = true"
    readonly
  ></v-text-field>
  <v-dialog v-model="dialog" max-width="300">
    <v-date-picker
      v-model="date"
      color="primary"
      @update:modelValue="saveDate"
      locale="ru"
    ></v-date-picker>
  </v-dialog>
</template>

<script>

export default {
  name: 'DatePicker',
  data: () => ({
    date: null,
    dialog: false,
  }),
  computed: {
    // dateFormatted() {
    //   var today = new Date();
    //   var dd = String(today.getDate()).padStart(2, '0');
    //   var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    //   var yyyy = today.getFullYear();
    //
    //   return yyyy + '-' + mm + '-' + dd;
    // },
  },
  methods: {
    saveDate() {
      console.log(this.date);
      // this.$emit('input', this.date);
      this.dialog = false;
    },
    format(date) {
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();

      return `${day}.${month}.${year}`;
    },
  },
};
</script>
