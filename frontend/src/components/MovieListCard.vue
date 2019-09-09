<template>
  <v-container>
  <v-hover v-slot:default="{ hover }">
    <v-card :elevation="hover ? 8 : 2">
      <v-layout align-center py-4 pl-4 @click=click>
        <v-flex text-center>
          <v-container grid-list-lg pa-0>
            <v-layout column>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title class="headline">
                    {{ title }}
                  </v-list-item-title>
                  <v-list-item-subtitle>{{ genresStr }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-card-text>
                <v-layout justify-center>
                  <v-rating
                    :value="rating"
                    color="indigo"
                    background-color="indigo"
                    half-increments
                    dense
                    readonly
                  />
                  <div class="grey--text ml-4">{{ rating.toFixed(1) }}</div>
                </v-layout>
              </v-card-text>
              <v-card-text>
                <v-layout justify-center>
                  <v-icon color="black">mdi-eye</v-icon>
                  <div class="grey--text ml-4">{{ viewCnt }}</div>
                </v-layout>
              </v-card-text>
            </v-layout>
          </v-container>
        </v-flex>
      </v-layout>
    </v-card>
  </v-hover>
  <div v-if="silmilar_movies">
    <!-- <MovieInfo v-if="silmilar_movies" :silmilar_movies="state"></MovieInfo> -->
    <MovieInfo :silmilar_movies="state"></MovieInfo>
  </div>
  </v-container>
</template>

<script>
import axios from "axios"
const apiUrl = '/api'
import { mapState, mapActions } from "vuex";
import MovieInfo from "./MovieInfo"
export default {
   components: {
    MovieInfo
  },
  props: {
    id: {
      type: Number,
      default: 0
    },
    title: {
      type: String,
      default: ""
    },
    genres: {
      type: Array,
      default: () => new Array()
    },
    img: {
      type: String,
      default: ""
    },
    rating: {
      type: Number,
      default: 0.0
    },
    viewCnt: {
      type: Number,
      default: 0
    },
  },
  computed: {
    genresStr: function() {
      return this.genres.join(" / ");
    },
     ...mapState({
      flag: state => state.data.dialogFlag
    }),
    state(){
      if(!this.flag){
        this.silmilar_movies=[]
      } 
      return this.silmilar_movies
    }
  },
  data () {
    return {
      silmilar_movies:[],
    }
  },
  methods:{
    async get_silmilar_movies(){
      const params = {
        movieid: this.id,
      };     
      axios.get(`${apiUrl}/recommends/`, {
            params,
        }).then(response => {
          this.silmilar_movies=response.data
        }) 
    },
    async click(){
      const movie = {
        id:this.id,
        img:this.img,
        title:this.title,
        genres:this.genresStr,
        rating:this.rating,
        viewCnt:this.viewCnt,
      };
      const params = {
        mode: "user",
        movieid: this.id
        };
      this.searchRating(params)
      this.changeDialog();
      this.silmilar_movies = await this.get_silmilar_movies();
      this.changeMovieInfo(movie)
      axios.put(`${apiUrl}/movies/?movieid=`+this.id, {
      })
    },
    ...mapActions("data", ["changeDialog","changeMovieInfo","searchRating"]),
  },
};
</script>