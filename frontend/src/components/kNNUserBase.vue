<template>
<v-flex>
   <v-flex v-if="user">
      <v-sheet
          class="mx-auto"
          elevation="8"
          max-width="800"
          light
        >
        <h3>{{user.username}}회원님과 비슷한 취향의 회원님들이 좋아하는 영화입니다</h3>
          <v-slide-group
            v-model="model"
            class="pa-4"
            show-arrows
            mandatory
          >
            <v-slide-item
              v-for="item in data"
              :key="item.key"
              v-slot:default="{ active, toggle }"
            >
            <v-hover>
              <template v-slot:default="{ hover }">
              <v-card
              :color="active ? 'red' : 'grey lighten-1'"
                class="ma-4"
                @click="toggle"
                width="110"
                height="160"
                dark
              >
                <v-row
                  class="fill-height"
                  align="center"
                  justify="center"
                >
                <v-card >
                  <v-img width="100" height="150" :src="item.src" />
                </v-card>
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
                       <v-rating half-increments readonly v-model="data[model].rating"></v-rating>({{data[model].rating}})
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
    </v-flex>
    <v-flex v-if="!user">
      로그인을 하셔야 유저별 맞춤 영화 추천 서비스를 받을 수 있습니다.
    </v-flex>
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
      user:null
    }),
    mounted() {
      if(sessionStorage.getItem('user')){
        this.user=JSON.parse(sessionStorage.getItem('user'))
        // console.log(this.user.id)
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