<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
    >
      <v-list dense>
        <v-list-item
          v-for="(choice, i) in choices"
          :key="i"
          @click="() => {
              if (choice.path) {
                goTo(choice.path)
              }
            }"
        >
          <v-list-item-action>
            <v-icon>{{ choice.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              {{ choice.text }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-subheader class="mt-4 grey--text text--darken-1">SUBSCRIPTIONS</v-subheader>
        <v-list>
          <v-list-item
            v-for="item in items2"
            :key="item.text"
            @click="goGitLab(item)"
          >
            <v-list-item-avatar>
              <img
                :src="getImgUrl(item.picture)"
                alt=""
              >
            </v-list-item-avatar>
            <v-list-item-title v-text="item.text"></v-list-item-title>
          </v-list-item>
        </v-list>
        <v-divider></v-divider>
        <v-list-item v-if="flag" 
            @click="() => {
                goTo('Admin')
            }">
          <v-list-item-action>
            <v-icon color="">settings</v-icon>
          </v-list-item-action>
          <v-list-item-title class=""
          >Manage</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      clipped-left
      color="red"
      dense
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-icon class="mx-4">fab fa-youtube</v-icon>
      <v-toolbar-title class="mr-12 align-center">
        <span class="title">추천해조</span>
      </v-toolbar-title>
      <div class="flex-grow-1"></div>
      <v-row
        align="center"
        style="max-width: 650px"
      >
      </v-row>
    </v-app-bar>

    <v-content>
      <v-container class="fill-height">
        <v-row>
          <v-col>
            <router-view />
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Vue from 'vue';
import VueSweetalert2 from 'vue-sweetalert2';
 
// If you don't need the styles, do not connect
import 'sweetalert2/dist/sweetalert2.min.css';
 
Vue.use(VueSweetalert2);
import router from "./router";
  export default {
    props: {
      source: String,
    },
    data: () => ({
      drawer: null,
      choices: [
      {
        icon: "home",
        text: "홈",
        path: "home"
      },
      {
        icon: "movie",
        text: "영화 검색",
        path: "movie-search"
      },
      {
        icon: "movie_filter",
        text: "영화 검색 기능 확장",
        path: "mostview-search"
      },
       {
        icon: "perm_identity",
        text: "유저 검색",
        path: "user-search"
      },
       {
        icon: "account_box",
        text: "로그인",
        path: "Login"
      }
    ],
      items2: [
        { picture: "rsh.jpg", text: '류승환',location:"https://lab.ssafy.com/shr2833" },
        { picture: "psh.jpg", text: '박성하' ,location:"https://lab.ssafy.com/SeongHaPark"},
        { picture: "sjs.jpg", text: '신진수',location:"https://lab.ssafy.com/jinsoo" },
        { picture: "jwb.jpg", text: '정우빈',location:"https://lab.ssafy.com/emerald6227" },
        { picture: "jjy.jpg", text: '정준영',location:"https://lab.ssafy.com/enter4836" },
      ],
      flag : false
    }),
    created () {
      this.$vuetify.theme.dark = true

      if(sessionStorage.getItem('user'))
      {
        this.choices[4].icon = 'exit_to_app';
        this.choices[4].path = '1';
        this.choices[4].text = '로그 아웃';

        let info = {
        icon: "account_box",
        text: "내 정보",
        path: "MyPage"
      }
        console.log(info);
        this.choices.push(info);
      }
    },
    mounted(){
      this.flag = this.chk()
    },
    methods: {
    goGitLab(item){
      window.open(item.location, '_blank'); 
    },
    goTo: function(path) {
      if(path === '1')
      {
        sessionStorage.clear();
        location.href="/"
      }
      else{
      router.push({ name: path });
      }
    },
    chk(){
      if(JSON.parse(sessionStorage.getItem('user')))
      {
        if(JSON.parse(sessionStorage.getItem('user')).is_staff == 0)
        {
          return false;
        }
        else{
          return true;
        }
      }
    },
    getImgUrl(img) {
			return require('./assets/' + img)
		}
  }
  }
</script>