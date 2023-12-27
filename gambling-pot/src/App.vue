<script setup>
</script>

<template>
  <div id="app">

  <b-navbar variant="dark" type="dark" :sticky="true" class="d-flex justify-content-center">
  <b-navbar-brand href="/" class="m-2">Gambling Pot</b-navbar-brand>
  </b-navbar>
    <router-view/>
 </div>
</template>

<script>

    export default {
        created() {
            this.preventContextMenu()
        },
        data() {
            return {
                host: 'https://gameshow.nikolaiprjanikov.de:5000',
                //host: "http://localhost:5000", 
                selected_user: null,
                pollingInterval: 3000
            }
        },
        methods: {
            preventContextMenu() {
                document.addEventListener("contextmenu", function (e) {
                    e.preventDefault()
                }, false)
            }
        }
    }

</script>