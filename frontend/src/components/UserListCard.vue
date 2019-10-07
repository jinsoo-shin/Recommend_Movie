<template>
  <v-container>
  <v-hover v-slot:default="{ hover }">
    <v-card :elevation="hover ? 8 : 2">
      <v-layout align-center py-4 pl-4>
        <v-flex text-center>
          <v-container grid-list-lg pa-0>
            <v-layout column>
              <v-card-text>
                <v-list>
                  <v-list-item-content>
                      <v-list-item-title class="headline">
                        {{ username }}   
                      </v-list-item-title>
                      <v-list-item-title >{{gender|genderfilter}}</v-list-item-title>
                      <v-list-item-title >{{age|agefilter}}</v-list-item-title>
                      <v-list-item-title v-text="occupation"></v-list-item-title>
                    </v-list-item-content>
                </v-list>
              </v-card-text>
              <v-card-text>
                <v-layout justify-center>
                  <v-list>
                    <v-list-group
                      v-for="item in items"
                      :key="item.title"
                      v-model="item.active"
                      :prepend-icon="item.action"
                      no-action
                    >
                      <template v-slot:activator>
                        <v-list-item-content>
                          <v-list-item-title v-text="item.title" ></v-list-item-title>
                        </v-list-item-content>
                      </template>
                      <v-list-item
                        v-for="subItem in subItems"
                        :key="subItem.title"
                        @click="item.active=false"
                      >
                        <v-list-item-content>
                          <v-list-item-title v-text="subItem.title"></v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list-group>
                  </v-list>
                </v-layout>
              </v-card-text>


              <v-card-actions>
                <v-row justify="center">
                  <v-dialog v-model="dialog" width="600px">
                    <template v-slot:activator="{ on }">
                      <v-btn color="primary" dark @click="get_silmilar_users">유사 유저 목록</v-btn>
                    </template>


                    <v-card>
                      <v-card-title>
                        <span class="headline">유사한 유저들의 목록</span>
                      </v-card-title>
                      <v-card-text v-if="dialog">
                        <v-item-group>
                          <v-item
                            v-for="item in silmilar_users"
                            :key="item.username"
                          >
                            <v-chip class="ma-2"
                            >
                            {{item.username}}
                            </v-chip>
                          </v-item>
                        </v-item-group>
                      </v-card-text>
                      <v-card-actions>
                        <div class="flex-grow-1"></div>
                        <v-btn color="green darken-1" text @click="dialog = false">Close</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-row>
              </v-card-actions>


            </v-layout>
          </v-container>
        </v-flex>
      </v-layout>
    </v-card>
  </v-hover>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";
import axios from "axios"
const apiUrl = '/api'

export default {
   components: {
  },
  props: {
    userid: {
      type: Number,
      default: 0
    },
    username: {
      type: String,
      default: ""
    },
    age: {
      type: Number,
      default: ""
    },
    gender: {
      type: String,
      default: ""
    },
    occupation: {
    type: String,
    default: ""
    },
  },
    filters: {
    agefilter: function (value) {
      if (value=='1') {
        return"Under 18";
      }else if(value=='18'){
        return "18-24";
        
      }else if(value=='25'){
        return "25-34";
        
      }else if(value=='35'){
        return "35-44";
        
      }else if(value=='45'){
        return "45-49";
        
      }else if(value=='50'){
        return "50-55";
        
      }else if(value=='56'){
        return "56+";
      }else{
        return value;
      }
    },
    genderfilter:function(value){
      if(value=='M'){
        return "남성";
      }else if(value=="F"){
        return "여성";
      } 
    }
  },
  mounted(){
    this.search();
      },
  computed: {
    ...mapState({
      userMovie: state => state.data.userMovie
    })
  },
  data () {
    return {
      open: ['public'],
      tree: [],
      items: [
          {
            action: 'movie',
            title: '본 영화 리스트',
            active: false,
          },
        ],
      subItems:[],
      dialog:false,
      silmilar_users:[]
    }
  },
  methods:{
    search(){
      const params = {
        userid: this.userid,
        mode:"usermovie"
      };     
      axios.get(`${apiUrl}/ratings/`, {
            params,
        }).then(response => {
          this.subItems=response.data
        }) 
    },
    get_silmilar_users(){
      this.dialog=true
      const params = {
        userid: this.userid,
      };     
      axios.get(`${apiUrl}/recommends/`, {
            params,
        }).then(response => {
          this.silmilar_users=response.data
        }) 
    },
  }
};
</script>