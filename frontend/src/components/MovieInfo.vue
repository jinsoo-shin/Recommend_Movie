<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" fullscreen  hide-overlay transition="dialog-bottom-transition" max-height="500">
      <v-card>
        <v-toolbar dark color="primary" style="z-index:2">
          <div class="flex-grow-1">
            <v-toolbar-title style="text-align:left">영화 상세 정보</v-toolbar-title>
          </div>
          <v-toolbar-items>
            <v-btn dark text @click="click">Close</v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-row>
          <v-col class="mb-6" color="red">
            <v-layout justify-center wrap>
            <v-flex xs12>
              <v-card>
                  <v-card-text>
                    <v-row>
                      <v-col md="4" color="red">
                        <v-img width="190" height="270" :src="movie_content.src" />
                      </v-col>
                      <v-col md="8" color="red">
                        <v-text-field filled label="타이틀" v-model="movie.title"></v-text-field>
                        <v-text-field filled label="장르" v-model="movie.genres"></v-text-field>
                        <v-text-field filled label="평점" v-model="movie.rating"></v-text-field>
                      </v-col>
                    </v-row>
                    <v-list-item v-if="movie_content.Director">
                      <v-col cols="2" id="colp">
                        <v-list-item-content >감독 :</v-list-item-content>
                      </v-col>
                      <v-col cols="10" id="colp">
                      <v-list-item-content class="align-end">{{movie_content.Director}}</v-list-item-content>
                      </v-col>
                    </v-list-item>
                    <v-list-item v-if="movie_content.Writers">
                      <v-col cols="2" id="colp">
                        <v-list-item-content >작가 :</v-list-item-content>
                      </v-col>
                      <v-col cols="10" id="colp">
                      <v-list-item-content class="align-end">{{movie_content.Writers}}</v-list-item-content>
                      </v-col>
                    </v-list-item>
                    <v-list-item v-if="movie_content.Summary">
                      <v-col cols="2" id="colp">
                        <v-list-item-content >줄거리 :</v-list-item-content>
                      </v-col>
                      <v-col cols="10" id="colp">
                      <v-list-item-content class="align-end" style="text-align:left">{{movie_content.Summary}}</v-list-item-content>
                      </v-col>
                    </v-list-item>
                    <v-divider class="my-2"></v-divider>
          
                  </v-card-text>
              </v-card>
            </v-flex>
            </v-layout>
          </v-col>
          <v-col class="mb-6" color="blue">
            <v-layout justify-center wrap>
              <v-flex xs12 id="content">
                    <v-card-text v-if="silmilar_movies.length!=0">
                      <v-list-item-group>
                        <v-subheader class="pl-0">유사한 영화들의 목록</v-subheader>
                        <v-list-item style="min-height:40px"
                          v-for="movie in silmilar_movies_computed"
                          :key="movie"
                        >
                        {{movie}}
                        </v-list-item>
                      </v-list-item-group>
                    <v-item-group multiple>
                      <v-subheader>관람 유저</v-subheader>
                      <v-item
                        v-for="(item,i) in viewUser"
                        :key="i"
                      >
                        <v-chip class="ma-2"
                        >
                        {{item.username}}
                        </v-chip>
                      </v-item>
                    </v-item-group>
                    </v-card-text>
              </v-flex>


             </v-layout>
          </v-col>

        </v-row>
        <v-divider></v-divider>
        <v-overlay :value="progress"
              :z-index="1" >
            <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import { mapState, mapActions } from "vuex";
import MovieListCard from "./MovieListCard"
  export default {
    props: {
      submit: {
        type: Function,
      default: () => {}
      },
      silmilar_movies: {
        type: Array,
        default: () => new Array()
      },
      movie_content: {
      },
     },
     computed:{
      ...mapState({
        dialog: state => state.data.dialogFlag,
        movie: state => state.data.curMovie,
        viewUser: state => state.data.viewUser
      }),
      progress(){
        if(this.silmilar_movies.length!=0&&this.dialog){
          return false
        }else if(this.silmilar_movies.length==0&&this.dialog){
          return true
        }else{
          return false
        }
      },
      silmilar_movies_computed(){
        return this.silmilar_movies.splice(1,9)
      }
     },
    data () {
      return {
        notifications: false,
        sound: true,
        widgets: false,
      }
    },
    methods:{
    click(){
      this.changeDialog();
    },
    ...mapActions("data", ["changeDialog"]),
   },
  }
</script>
<style>
#content{
  padding:0px
}
</style>