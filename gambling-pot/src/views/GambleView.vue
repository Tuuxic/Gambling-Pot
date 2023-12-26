
<template>
  <b-container fluid class="d-flex flex-grow-1" style="height: auto;">
    <b-row class="d-flex justify-content-center align-items-center flex-column flex-grow-1">

      <b-col class="d-flex align-items-center justify-content-center mt-4 ">
        <h1>{{ (this.users.filter(e => e.id == this.$parent.selected_user)[0] || { 'name': 'Null' }).name }} - Runde {{
          this.gamestate.round }}</h1>
      </b-col>

      <b-col class="d-flex align-items-center justify-content-center mt-4 ">
        Punkte: {{ (this.users.filter(e => e.id == this.$parent.selected_user)[0] || { balance: 0 }).balance }}
      </b-col>

      <b-col class="d-flex justify-content-center mt-4" style="height:40vh; width:80vw;">

        <Doughnut :data="this.chartData" :options="this.chartOptions" />
      </b-col>

      <b-col v-if="this.selectedOption === -1" class="d-flex align-items-center justify-content-center mt-4">
        <b-row class="fillRow m-1"><b-button variant="danger" :disabled="this.gamestate['betLocked']" v-on:click="selectOption(0)"> Kill </b-button></b-row>
      </b-col>

      <b-col v-if="this.selectedOption === -1" class="d-flex align-items-center justify-content-center">
        <b-row class="fillRow m-1"><b-button variant="success" :disabled="this.gamestate['betLocked']" v-on:click="selectOption(1)"> Not Kill </b-button></b-row>
      </b-col>

      <b-spinner v-if="this.selectedOption != -1 " class="mt-5"></b-spinner>

      <h2 v-if="this.selectedOption != -1" class="mt-5 text-center"> {{ this.getCoiceText(this.selectedOption) }} </h2>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
ChartJS.register(ArcElement, Tooltip, Legend)
export default {
  components: { Doughnut },
  mounted() {
    if (this.$parent.selected_user == null) {
      this.$router.push("/")
    }
    this.refresh()

  },
  beforeDestroy() {
    clearInterval(this.intervalId) 
  },
  created() {
    this.refresh()
    this.intervalId = setInterval(function () {
      this.refresh()
    }.bind(this), this.$parent.pollingInterval)

    window.addEventListener("resize", this.chartResize);
  },
  data() {
    return {
      gamestate: { gameId: 0, round: 0, betLocked: false},
      users: [],
      last_round: -1,
      chartPotData: [0, 0, 0],
      selectedOption: -1,
      intervalId: 0
    }
  },
  computed: {
      chartData() { 
        return {
        labels: ["None (" + this.chartPotData[0] + ")" , "Kill (" + this.chartPotData[1] + ")", "Not Kill (" + this.chartPotData[2] + ")"],
        datasets: [{ data: this.chartPotData, backgroundColor: ['#00D8FF', '#E46651', '#41B883'] }]
        }
      },
      chartOptions() {
        return {
        responsive: true,
maintainAspectRatio: true
        }
      }
  },
  methods: {
    chartResize() {
      for (let id in ChartJS.instances) {
        ChartJS.instances[id].resize();
    }
    },
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
    getPots() {
      axios.get(this.$parent.host + '/pots').then((res) => {
        this.chartPotData = [res.data[-1], res.data[0], res.data[1]]
      })
    },
    getGameStateThenChoice() {
      axios.get(this.$parent.host + '/gamestate').then((res) => {
        this.gamestate = res.data
        this.getChoice(this.$parent.selected_user)
      })
    },
    getChoice(id) {
      let choice = {
        'id': id,
        'gameId': this.gamestate['gameId'],
        'round': this.gamestate['round']
      }
      axios.post(this.$parent.host + '/bets/choice', choice).then((res) => {
        let selection = res.data.optSelected
        if ([1, 0, -1].includes(selection)) {
          this.selectedOption = selection
        } else {
          this.selectedOption = -1
        }
      })
    },
    getCoiceText(opt) {
      if(opt === 1) {
        return 'Not Kill'
      }

      if(opt === 0) {
        return 'Kill'
      }

      return 'None'
    },
    selectOption(option) {
      let bet = {
        'gameId': this.gamestate.gameId,
        'round': this.gamestate.round,
        'id': this.$parent.selected_user,
        'optSelected': option

      }
      axios.post(this.$parent.host + '/bets/add', bet).then(() => {
        this.last_round = this.gamestate.round
        this.refresh()
      }).catch((error) => {
        console.log(error)
      })
    },
    refresh() {
      this.getUsers()
      this.getPots()
      this.getGameStateThenChoice()
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
