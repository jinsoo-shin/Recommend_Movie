<template>
  <v-flex shrink style="text-align:center">

<!-- --><!-- --><!-- --><!-- -->
  <v-sheet
      class="mx-auto"
      elevation="8"
      max-width="800"
    >
      <v-slide-group
        v-model="model"
        class="pa-4"
        show-arrows
      >
        <v-slide-item
          v-for="item in data"
          :key="item.key"
          v-slot:default="{ active, toggle }"
        >
            <v-hover>
               <template v-slot:default="{ hover }">
          <v-card
            class="ma-4"
            @click="toggle"
            width="100"
            height="150"
          >
            <v-row
              class="fill-height"
              align="center"
              justify="center"
            >
              <v-img width="100" height="150" :src="item.src" />
              <v-fade-transition>
          <v-overlay
            v-if="hover"
            absolute
            color="#036358"
          >
            <v-btn>More info</v-btn>
          </v-overlay>
        </v-fade-transition>
            </v-row>
          </v-card>

               </template>
            </v-hover>

        </v-slide-item>
      </v-slide-group>

      <v-expand-transition>
        <v-sheet
          v-if="model != null"
          color="grey lighten-4"
          height="200"
          tile
        >
          <v-row
            class="fill-height"
            align="center"
            justify="center"
          >
            <v-col>
              <v-card
                color="#385F73"
                dark
              >
                <v-card-text class="white--text">
                  <div class="headline mb-2">{{data[model].title}} </div>
                  {{data[model].genres}}
                </v-card-text>

                <!-- <v-card-actions>
                  <v-btn text>Listen Now</v-btn>
                </v-card-actions> -->
                </v-card>
              </v-col>
            <!-- <h3 class="title">{{model}}Selected {{ data[model].value }}</h3> -->
          </v-row>
        </v-sheet>
      </v-expand-transition>
    </v-sheet>
<!-- --><!-- --><!-- -->
  </v-flex>
</template>

<script>
import axios from "axios"
const apiUrl = '/api'
export default {
    data: () => ({
      data:[
      ],
      model:null,
      str: '',
      user:null
    }),
    mounted() {
      if(sessionStorage.getItem('user')){
        this.user=JSON.parse(sessionStorage.getItem('user'))
        console.log(this.user.id)
        const params = {
          userid: this.user.id,
        };     
        axios.get(`${apiUrl}/test/`, {
              params,
          }).then(response => {
            this.data=response.data
          }) 
      }
    }
  }
</script>