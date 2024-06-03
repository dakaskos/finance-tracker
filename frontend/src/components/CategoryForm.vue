<template>
    <v-btn
      color="primary"
      prepend-icon="mdi-plus"
      variant="tonal"
      @click="dialog = true"
    >
      Add category
    </v-btn>
    <v-dialog v-model="dialog" max-width="600">
      <v-form method="post" v-model="valid" action>
        <v-card prepend-icon="mdi-folder" title="Add category">
          <v-card-text>
            <v-row dense>
              <v-col cols="12" md="12" sm="12">
                <v-text-field
                  v-model="categoryForm.name"
                  :counter="10"
                  :rules="[v => !!v && v.length > 3 || 'Name is required']"
                  label="Name"
                  hide-details
                  required
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
</template>

<script>
import axios from "axios";

export default {
  name: "CategoryForm",
  data: () => ({
    dialog: false,
    valid: false,
    categoryForm: {
      name: "",
    },
  }),
  methods: {
    async submitForm() {
      try {
          const response = await axios.post(
            'http://127.0.0.1:8000/api/category/',
            {
              name: this.categoryForm.name,
              user: 1, // TODO: replace with the logged-in user
            }
          );
          this.dialog = false;
          this.$emit('update-categories');
          console.log('Response:', response.data);
        } catch (error) {
          console.error('Error:', error);
        }
    },
  },
};
</script>
