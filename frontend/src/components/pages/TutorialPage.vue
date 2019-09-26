<template>
  <v-card>
        <v-container fluid>
          <v-row>
              <v-col md="4" sm="12">
                  <v-row
                  align="center"
                  >
                  <v-col
                    md="6" sm="2"
                    v-for="i in genres"
                    :key="i"
                  >
                    <v-chip @click="selection(i)">{{i}}
                    </v-chip>
                  </v-col>
                  </v-row>
              </v-col>
              <v-col md="8" sm="12">
                  <v-card color="#7f7f7f">
                    <v-card-title>
                        {{Title}}
                        <div class="flex-grow-1"></div>
                        <v-text-field
                        v-model="search"
                        append-icon="search"
                        label="Search"
                        single-line
                        hide-details
                        ></v-text-field>
                    </v-card-title>
                    <v-data-table
                        light
                        :headers="Movieheaders"
                        :items="select"
                        :search="search"
                        show-expand
                        item-key="id"
                        :single-expand="singleExpand"
                        height="25vmax"
                    >
                    <template v-slot:expanded-item="{ headers, item }">
                      <td :colspan="headers.length" style="text-align:center; background:antiquewhite; border:beige solid 0.1px;">
                        <v-rating v-model="rating" half-increments hover style="display:inline" 
                          background-color="white"
                          empty-icon="$vuetify.icons.ratingFull"></v-rating>
                          
                          <v-btn 
                          :loading="loading"
                          :disabled="loading"
                          depressed
                          small
                          color="blue-grey"
                          class="ma-2 white--text"
                          fab
                          @click="PostRate(item.id)"
                          >
                          <v-icon dark>mdi-cloud-upload</v-icon>
                        </v-btn>
                      </td>
                    </template>
                    </v-data-table>

                    </v-card>
              </v-col>
          </v-row>
        </v-container>
  </v-card>
</template>
<script>
import axios from "axios";
const apiUrl = '/api'
export default {
  name: 'TutorialPage',
  data: ()=>({
    userdata : null,
    loader: null,
    loading: false,
    index : 0,
    expanded: [],
    rating: 0,
    singleExpand: true,
    genres: ["Action", "Adventure", "Animation", "Children's", "Comedy", "Crime" ,"Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"],
    Title : 'Movie',
    search: '',
    Movieheaders: [
        {
          text: 'ID',
          align: 'left',
          sortable: false,
          value: 'id',
        },
        { text: 'title', value: 'title' }
      ],
      Movies: [],
      select: []
  }),
  mounted(){

    if(sessionStorage.getItem('Cookie'))
    {
      axios.get(`${apiUrl}/movies/`).then(response => {
            // this.Users=[]
            this.Movies = response.data;
            this.select = this.Movies;
          }).catch(error =>{
          }).finally(rs =>{
          })
    }
    else{
      alert('접근하실 수 없습니다!');
      location.replace('/');
    }

    this.$swal('평점 선택',
  '안녕하세요? 관람하신 영화의 평점을 남겨주세요.다 마치신 후에 다른 페이지로 이동하시면 됩니다.',
  'question');
  },
  methods: {
      selection(item){
          this.Title = item
          console.log(item)
          this.select = [];
          console.log(this.Movies[0])
          for(var i = 0; i < this.Movies.length;i++)
          {
              if(this.Movies[i].genres_array.indexOf(this.Title) != -1)
              {
                  this.select.push(this.Movies[i]);
              }
          }
      },
      PostRate(id){
        alert(id +  " " + this.rating);
        axios.POST(`${apiUrl}/ratings/`).then(response => {
            // this.Users=[]

          }).catch(error =>{
          }).finally(rs =>{
          })
      }
  },
  created() {
        history.pushState(null, null, location.href);
        window.onpopstate = function(event) {
        history.go(1);
        };
  },
  watch: {
      loader () {
        const l = this.loader
        this[l] = !this[l]

        setTimeout(() => (this[l] = false), 2000)
        this.loader = null
      },
    },
}
</script>
