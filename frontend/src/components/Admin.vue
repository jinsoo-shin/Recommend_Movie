<template>
    <v-card>
    <v-tabs
      background-color=""
      color="yellow"
      right
    >
      <v-tab><v-icon>supervised_user_circle</v-icon></v-tab>
      <v-tab><v-icon>subscriptions</v-icon></v-tab>
      <v-tab><v-icon>assessment</v-icon></v-tab>


      <!--USER-->
      <v-tab-item>
        <v-container fluid>
          <v-row>
            <v-col>
            <v-card color="#FB3640">
              <v-card-title>
                USER
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
                :headers="Userheaders"
                :items="Users"
                item-key="id"
                :search="search"
              >
              
              <template v-slot:item.action="{ item }">
                  <v-icon
                    small
                    class="mr-2"
                    @click.prevent="editItem(item, 'USER')"
                  >
                    edit
                  </v-icon>
                  <v-icon
                    small
                    @click.prevent="deleteItem(item, 'USER')"
                  >
                    delete
                  </v-icon>
                </template>
              </v-data-table>

              <v-dialog v-model="user_dialog" max-width="500px">
          <v-card>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field readonly v-model="user_edited.username" label="name"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="user_edited.age" label="age"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="user_edited.gender" label="gender"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="user_edited.occupation" label="occupation"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <div class="flex-grow-1"></div>
              <v-btn color="blue darken-1" text @click.prevent="close('USER')">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click.prevent="save('USER')">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
            </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-tab-item>

      <!--Movie-->
      <v-tab-item>
        <v-container fluid>
          <v-row>
            <v-col>
            <v-card color="#FB5A62">
              <v-card-title>
                Movie
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
                :items="Movies"
                :search="search"
              >
              <template v-slot:item.action="{ item }">
                  <v-icon
                    small
                    class="mr-2"
                    @click.prevent="editItem(item, 'MOVIE')"
                  >
                    edit
                  </v-icon>
                  <v-icon
                    small
                    @click.prevent="deleteItem(item, 'MOVIE')"
                  >
                    delete
                  </v-icon>
              </template>

            </v-data-table>

          <v-dialog v-model="movie_dialog" max-width="500px">
          <v-card>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="movie_edited.title" label="title"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field readonly v-model="movie_edited.rating" label="rating"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="movie_edited.viewCnt" label="viewCnt"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="12">
                    <v-text-field v-model="movie_edited.genres_array" label="genres"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <div class="flex-grow-1"></div>
              <v-btn color="blue darken-1" text @click.prevent="close('MOVIE')">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click.prevent="save('MOVIE')">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

            </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-tab-item>

      <!--Algorithm-->
      <v-tab-item>
        <v-container fluid>
          <v-row>
            <v-col>
            <v-card color="#00787E">
              <v-card-title>
                Algorithm
              </v-card-title>
            </v-card>
            <v-card>
              <AdminAlgorithm></AdminAlgorithm>
            </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-tab-item>

    </v-tabs>
    <v-overlay :value="progress" :z-index="0">
      <v-progress-circular indeterminate size="64" width="7" color="amber"></v-progress-circular>
    </v-overlay>
     <div class="text-center">
      <v-snackbar
        v-model="snackbar"
        :timeout="1000"
      >
        {{ snackbartext }}
        <v-btn
        text
        @click="snackbar = false"
      >
        Close
      </v-btn>
      </v-snackbar>
    </div>
  </v-card>
</template>

<script>
import axios from "axios";
const apiUrl = '/api'
import AdminAlgorithm from "./AdminAlgorithm"
export default {
  name: 'Admin',
  components: {
        AdminAlgorithm,
	},
  data () {
    return {
      tabs : 3,
      search: '',
      tab: null,
      drawer: null,
      right: null,
      login: false,
      user_dialog: false,
      user_edited: [],
      search: '',
      Userheaders: [
        {
          text: 'ID',
          align: 'left',
          value: 'id',
        },
        { text: '이름', value: 'username'},
        { text: '나이', value: 'age' },
        { text: '성별', value: 'gender' },
        { text: '직업', value: 'occupation' },
        { text: 'Action', value: 'action', sortable: false },
      ],
      Movieheaders: [
        {
          text: 'ID',
          align: 'left',
          sortable: false,
          value: 'id',
        },
        { text: 'title', value: 'title' },
        { text: 'genres', value: 'genres_array' },
        { text: 'rating', value: 'rating'},
        { text: 'viewCnt', value: 'viewCnt'},
        { text: 'Action', value: 'action', sortable: false },
      ],
      Users: [
      ],
      Movies:[
      ],
      editedIndex : 0,
      movie_edited: [],
      movie_dialog: false,
      flag:true,
      snackbar:false,
      snackbartext:"로딩 완료!"
    }
  },
  created(){
   axios.get(`${apiUrl}/auth/signup-many/`).then(response => {
            // this.Users=[]
            this.Users = response.data;
          }).catch(error =>{
          }).finally(rs =>{
          })
    
    axios.get(`${apiUrl}/movies/`).then(response => {
            // this.Users=[]
            this.Movies = response.data;
          }).catch(error =>{
          }).finally(rs =>{
          })
  },
  mounted(){
     
  },
  computed:{
    progress(){
      if(this.flag && this.Users.length==0){
        this.flag=false
        return true
      }else{
        this.snackbar=true
        return false
      }
    }
  },
	methods: {
    editItem(item, str){
      if(str === 'USER')
      {
        this.editedIndex = this.Users.indexOf(item)
        this.user_edited = Object.assign({}, item)
        this.user_dialog = true;
      }
      else if(str === 'MOVIE')
      {
        this.editedIndex = this.Movies.indexOf(item)
        this.movie_edited = Object.assign({}, item)
        this.movie_dialog = true;
      }
    },
    deleteItem(item,str){
      if(str === 'USER')
      {
        const index = this.Users.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.Users.splice(index, 1)

        axios.delete(`${apiUrl}/delete/user/?id=`+item.id+'&username='+item.username
        ).then(response =>{
          console.log(response);
        }).catch(error =>{
          console.log(error);
        }).finally(fin => {
          console.log("END!")
        })
      }
      else if(str === 'MOVIE')
      {
        const index = this.Movies.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.Movies.splice(index, 1)

        axios.delete(`${apiUrl}/delete/movie/?movieid=`+item.id
        ).then(response =>{
          console.log(response);
        }).catch(error =>{
          console.log(error);
        }).finally(fin => {
          console.log("END!")
        })
      }
    },
    close (str) {
      if(str === 'USER')
      {
        this.user_dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      }
      else if(str === 'MOVIE')
      {
        this.movie_dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      }
      },

      save (str) {
        if(str === "USER")
        {
          if (this.editedIndex > -1) {
            Object.assign(this.Users[this.editedIndex], this.editedItem)
          } else {
            this.Users.push(this.editedItem)
          }
          var ageage = parseInt(this.user_edited.age);
          if( ageage < 18 )
          {
            this.user_edited.age = '1'
          }
          else if( ageage < 25)
          {
            this.user_edited.age = '18'
          }
          else if( ageage < 35)
          {
            this.user_edited.age = '25'
          }
          else if( ageage < 45)
          {
            this.user_edited.age = '35'
          }
          else if( ageage < 50)
          {
            this.user_edited.age = '45'
          }
          else if( ageage < 56)
          {
            this.user_edited.age = '50'
          }
          else
          {
            this.user_edited.age = '56'
          }

          const params = {
            id : this.user_edited.id,
            age : this.user_edited.age,
            occupation : this.user_edited.occupation,
            gender : this.user_edited.gender
          }
          console.log(params)

          axios.put(`${apiUrl}/update/user/`, { params }
          ).then(response =>{
            this.Users[this.editedIndex].age = params.age;
            this.Users[this.editedIndex].occupation = params.occupation;
            this.Users[this.editedIndex].gender = params.gender;
            this.close('USERS')
          }).catch(error =>{
            console.log(error);
          }).finally(fin => {
            console.log("END!")
          })
        }
        else if(str === 'MOVIE')
        {
          if (this.editedIndex > -1) {
            Object.assign(this.Movies[this.editedIndex], this.editedItem)
          } else {
            this.Movies.push(this.editedItem)
          }
          this.close('MOVIE')

          const params = {
            movieid : this.movie_edited.id,
            title : this.movie_edited.title,
            viewCnt : this.movie_edited.viewCnt
          }
          console.log(this.movie_edited)

          axios.put(`${apiUrl}/update/movie/`, { params }
          ).then(response =>{
            this.Movies[this.editedIndex].title = params.title;
            this.Movies[this.editedIndex].viewCnt = params.viewCnt;
            this.close('MOVIE')
          }).catch(error =>{
            console.log(error);
          }).finally(fin => {
            console.log("END!")
          })
        }
      },
  }
}
</script>
<style>
.text-shadow {
  text-shadow: 0 0 15px rgb(255,255,255);
}
.v-btn__content>a{
  color:white;
}
.v-list__tile>a{
  color:black;
}
.goog-te-combo{
  color:black;
}
.goog-te-banner-frame{
  display:none;
}
.fixed {
    position: fixed;
    top:0; left:0;
    width: 100%; 
}
.material-icons{
  vertical-align: bottom;
  margin-right: 9px;
}

</style>