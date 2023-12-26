<script>
import axios from "axios";

import Vue from 'vue'
export default {
  created() {
    this.getUsers()
  },
  data() {
    return {
      users: [],
      isAdmin: !(this.$cookies.get("admin") == null) 
    }
  },
  methods: {
    clickButton(uid) {
      this.$parent.selected_user = uid
      this.$router.push('gamble')
    }, 
    getUsers() {
      axios.get(this.$parent.host + '/users').then((res) => {
        this.users = res.data.users
      })
    },
    openAdminPanel() {
      this.$router.push('admin')
    }
  }
}
</script>

<template>
  <div>
    <b-col class="d-flex justify-content-center">
      <b-row class=" fillRow">
        <b-col >
          <b-row v-for="u in this.users" :key="'user-' + u.id" class="m-2 justify-content-center">
            <b-button variant="outline-dark" class="p-3 fillRow" v-on:click="clickButton(u.id)">{{ u.name }}</b-button>
          </b-row>

          <b-row v-if="this.isAdmin" class="m-2 justify-content-center">
            <b-button variant="outline-dark" class="p-3 fillRow" v-on:click="openAdminPanel()">Admin</b-button>
          </b-row>

        </b-col>

      </b-row>


    </b-col>
  </div>
</template>

<style>
.fillRow {
  width: 100%;
}
</style>
