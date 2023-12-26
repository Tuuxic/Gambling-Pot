<template>
  <b-container>
    <b-row class="d-flex justify-content-center align-items-center flex-column h-100">

      <b-col class="d-flex align-items-center justify-content-center mt-4">
        <h1>Admin Panel</h1>
      </b-col>

      <b-col class="d-flex align-items-center justify-content-center mt-4">
        <h1>Runde {{ this.gamestate.round }}</h1>
      </b-col>


      <b-col class="d-flex align-items-center justify-content-center mt-4">
        <b-row class="fillRow m-1"><b-button variant="danger" v-on:click="selectOption(0)"> Kill </b-button></b-row>
      </b-col>

      <b-col class="d-flex align-items-center justify-content-center">

        <b-row class="fillRow m-1"><b-button variant="success" v-on:click="selectOption(1)"> Not Kill </b-button></b-row>
      </b-col>

      <b-col class="d-flex align-items-center justify-content-center">

        <b-row class="fillRow m-1"><b-button variant="primary" v-on:click="toggleBetLock()"> {{ this.gamestate['betLocked'] ? "Unlock Bets" : "Lock Bets"}} </b-button></b-row>
      </b-col>

        <b-container class="mt-5">
          <b-row class="d-flex justify-content-center align-items-center" cols="3">
                           <b-col v-for="user in this.users" :key="'active-' + user.id" md="4" cols="4"
                           class=" mb-3 px-3  text-center felx-grow-1">
                           <h3>{{ user.name }}: {{ user.balance }}</h3>
                           </b-col>
                    </b-row>
        </b-container>

      <b-col class="d-flex align-items-center justify-content-center mt-4">

        <b-row class="fillRow m-1"><b-button variant="primary" v-on:click="reset()"> Reset </b-button></b-row>
      </b-col>


    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";

export default {
  
  created() {
    this.getGameState()
    this.getUsers()
  },
  data() {
    return {
      gamestate: { gameId: 0, round: 0 },
      users: []

    }
  },
  methods: {
    getGameState() {

      axios.get(this.$parent.host + '/gamestate').then((res) => {
        this.gamestate = res.data
      })
    },
    getUsers() {
      axios.get(this.$parent.host + '/users').then((res) => {
        this.users = res.data.users
      })
    },
    toggleBetLock() {
      if(this.gamestate['betLocked']) {

        axios.post(this.$parent.host + '/bets/unlock', null).then(() => {
        this.refresh()
                }).catch((error) => {
                    console.log(error)
                })
      } else {

        axios.post(this.$parent.host + '/bets/lock', null).then(() => {
        this.refresh()
                }).catch((error) => {
                    console.log(error)
                })
      }
    },
    selectOption(option) {
      let opt = {
        'opt': option
      }
        axios.post(this.$parent.host + '/round/finish', opt).then(() => {

        this.refresh()
                }).catch((error) => {
                    console.log(error)
                })
    },
    reset() {

        axios.post(this.$parent.host + '/round/reset', null).then(() => {

        this.refresh()
                }).catch((error) => {
                    console.log(error)
                })
    }, 
    refresh() {
      
        this.getGameState()
        this.getUsers()
    }
  }
}
</script>

  <!--
    <b-col
      class="d-flex flex-column align-items-center justify-content-around h-100"
    >
      <b-row class="m-1">
        <h1>Round 1</h1>
      </b-row>

      <b-row class="m-1"> Points: 0 </b-row>

      <b-row class="fillRow">
        <b-col>
          <b-row class="m-1 fillRow">
            
          </b-row>

          <b-row class="m-1 fillRow">
            
          </b-row>
        </b-col>
      </b-row>
    </b-col>

-->

<style>
.fillRow {
  width: 90%;
}
</style>
