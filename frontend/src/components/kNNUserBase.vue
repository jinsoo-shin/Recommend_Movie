<template>
<v-flex>
   <v-flex v-if="user">
      <v-sheet
          class="mx-auto"
          elevation="8"
          max-width="800"
          light
        >
        <h3 class="pt-4">{{user.username}}회원님과 비슷한 취향의 회원님들이 좋아하는 영화입니다</h3>
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
              height="400"
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
                    style="text-align:left"
                  >
                    <v-card-text class="white--text">
                      <div class="headline mb-2">{{data[model].title}} </div>
                      <v-row>
                        <v-col cols="12">
                          <v-card>
                            <v-list dense>
                              <v-list-item v-if="data[model].title">
                                <v-col cols="2">
                                  <v-list-item-content>Genres:</v-list-item-content>
                                </v-col>
                                <v-col cols="10">
                                  <v-list-item-content class="align-end">{{ data[model].genres }}</v-list-item-content>
                                </v-col>
                              </v-list-item>
                              <v-list-item v-if="data[model].rating">
                                <v-col cols="2">
                                  <v-list-item-content>Rating:</v-list-item-content>
                                </v-col>
                                <v-col cols="10">
                                  <v-list-item-content class="align-end">
                                    <v-flex>
                                      ({{data[model].rating}}) 
                                      <v-rating half-increments readonly v-model="data[model].rating" style="display:inline"></v-rating>
                                    </v-flex></v-list-item-content>
                                </v-col>
                              </v-list-item>
                              <v-list-item v-if="data[model].Summary">
                                <v-col cols="2">
                                  <v-list-item-content>Summary:</v-list-item-content>
                                </v-col>
                                <v-col cols="10">
                                  <v-list-item-content class="align-end">{{ data[model].Summary }}</v-list-item-content>
                                </v-col>
                              </v-list-item>

                              <v-list-item v-if="data[model].Director">
                                <v-col cols="2">
                                <v-list-item-content>Director:</v-list-item-content>
                                </v-col>
                                <v-col cols="10">
                                  <v-list-item-content class="align-end">{{ data[model].Director}}</v-list-item-content>
                                </v-col>
                              </v-list-item>

                              <v-list-item v-if="data[model].Writers">
                                <v-col cols="2">
                                  <v-list-item-content >Writers:</v-list-item-content>
                                </v-col>
                                <v-col cols="10">
                                <v-list-item-content class="align-end">{{data[model].Writers }}</v-list-item-content>
                                </v-col>
                              </v-list-item>
                            </v-list>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-card-text>
                     <v-card-actions>
                        <div class="flex-grow-1"></div>
                        <v-btn
                          text
                          outlined 
                          @click="newpage(data[model].ImdbLink)"
                          v-if="data[model].src!=='http://folo.co.kr/img/gm_noimage.png'"
                        >
                          Show More
                        </v-btn>
                        <v-btn
                          text
                          outlined 
                          @click="newsearchpage(data[model].title)"
                          v-if="data[model].src==='http://folo.co.kr/img/gm_noimage.png'"
                        >
                          Show More
                        </v-btn>
                      </v-card-actions>
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
        const params = {
          userid: this.user.id,
        };     
        axios.get(`${apiUrl}/test/`, {
              params,
          }).then(response => {
            this.data=response.data
          }) 
      }
    },
    methods:{
      newpage(url){
        window.open(url,'_blank')
      },
      newsearchpage(title){
        var query = title.split(" ").join("+")
        if(query.indexOf("(")!=-1){
          query=query.substring(0,query.indexOf("("))
        }
        var url = "https://www.imdb.com/find?ref_=nv_sr_fn&s=tt&q="+query
        window.open(url,'_blank')
      }
    }
  }
</script>
<style>
.col-xl, .col-xl-auto, .col-xl-12, .col-xl-11, .col-xl-10, .col-xl-9, .col-xl-8, .col-xl-7, .col-xl-6, .col-xl-5, .col-xl-4, .col-xl-3, .col-xl-2, .col-xl-1, .col-lg, .col-lg-auto, .col-lg-12, .col-lg-11, .col-lg-10, .col-lg-9, .col-lg-8, .col-lg-7, .col-lg-6, .col-lg-5, .col-lg-4, .col-lg-3, .col-lg-2, .col-lg-1, .col-md, .col-md-auto, .col-md-12, .col-md-11, .col-md-10, .col-md-9, .col-md-8, .col-md-7, .col-md-6, .col-md-5, .col-md-4, .col-md-3, .col-md-2, .col-md-1, .col-sm, .col-sm-auto, .col-sm-12, .col-sm-11, .col-sm-10, .col-sm-9, .col-sm-8, .col-sm-7, .col-sm-6, .col-sm-5, .col-sm-4, .col-sm-3, .col-sm-2, .col-sm-1, .col, .col-auto, .col-12, .col-11, .col-10, .col-9, .col-8, .col-7, .col-6, .col-5, .col-4, .col-3, .col-2, .col-1 {
    padding: 0px 12px!important;
}
</style>