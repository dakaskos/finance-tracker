<template>
  <v-btn
      v-if="!isLoggedIn"
      color="primary"
      prepend-icon="mdi-plus"
      variant="tonal"
      @click="dialog = true"
    >
      Войти
    </v-btn>
  <v-btn
      v-if="isLoggedIn"
      color="primary"
      prepend-icon="mdi-plus"
      variant="tonal"
      @click="logout"
    >
      Выйти
    </v-btn>

  <v-dialog v-model="dialog" max-width="600">
    <v-card>
      <v-card-title>
        <h2>Войти</h2>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            v-model="username"
            label="Имя пользователя"
            required
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Пароль"
            required
            type="password"
          ></v-text-field>
          <v-btn
            @click="login"
            color="primary"
          >
            Войти
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginForm",
  data: () => ({
    dialog: false,
    username: "",
    password: "",
  }),
  props: {
    isLoggedIn: Boolean,
  },
  methods: {
    async login() {
      try {
        const response = await axios.post(window.django_host + "/api/token/", {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem("access_token", response.data.access);
        this.$emit("update-tokens");
        this.dialog = false;
      } catch (error) {
        console.error(error);
      }
    },
    logout() {
      localStorage.removeItem("access_token");
      this.$emit("update-tokens");
    },
  },
};

</script>
