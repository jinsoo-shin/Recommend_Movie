<template>
<v-flex>
   <v-flex v-if="user">
      <v-sheet
          class="mx-auto"
          elevation="8"
          max-width="800"
          light
        >
        <h3>{{user.username}}회원님이 본 영화와 비슷한 영화입니다</h3>
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
                        <v-col cols="12" id="colp">
                          <v-card>
                            <v-list dense>
                              <v-list-item v-if="data[model].title">
                                <v-col cols="2" id="colp">
                                  <v-list-item-content>Genres:</v-list-item-content>
                                </v-col>
                                <v-col cols="10" id="colp">
                                  <v-list-item-content class="align-end">{{ data[model].genres }}</v-list-item-content>
                                </v-col>
                              </v-list-item>
                              <v-list-item v-if="data[model].rating">
                                <v-col cols="2" id="colp">
                                  <v-list-item-content>Rating:</v-list-item-content>
                                </v-col>
                                <v-col cols="10" id="colp">
                                  <v-list-item-content class="align-end">
                                    <v-flex>
                                      ({{data[model].rating}}) 
                                      <v-rating half-increments readonly v-model="data[model].rating" style="display:inline"></v-rating>
                                    </v-flex></v-list-item-content>
                                </v-col>
                              </v-list-item>
                              <v-list-item v-if="data[model].Summary">
                                <v-col cols="2" id="colp">
                                  <v-list-item-content>Summary:</v-list-item-content>
                                </v-col>
                                <v-col cols="10" id="colp">
                                  <v-list-item-content class="align-end">{{ data[model].Summary }}</v-list-item-content>
                                </v-col>
                              </v-list-item>

                              <v-list-item v-if="data[model].Director">
                                <v-col cols="2" id="colp">
                                <v-list-item-content>Director:</v-list-item-content>
                                </v-col>
                                <v-col cols="10" id="colp">
                                  <v-list-item-content class="align-end">{{ data[model].Director}}</v-list-item-content>
                                </v-col>
                              </v-list-item>

                              <v-list-item v-if="data[model].Writers">
                                <v-col cols="2" id="colp">
                                  <v-list-item-content >Writers:</v-list-item-content>
                                </v-col>
                                <v-col cols="10" id="colp">
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
        axios.get(`${apiUrl}/jwb_view/`, {
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