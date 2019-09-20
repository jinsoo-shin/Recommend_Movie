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
                        height="25vmax"
                    >

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
  },
  created() {
        history.pushState(null, null, location.href);
        window.onpopstate = function(event) {
        history.go(1);
        };
  },
}
</script>
