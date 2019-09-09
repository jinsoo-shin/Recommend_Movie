<template>
  <v-form ref="form">
    <v-container>
      <v-row>
          <v-col cols="12" sm="12">
            <v-text-field v-model="title" label="영화 제목" @keydown.prevent.enter="onSubmit" />
          </v-col>
        </v-row>
         <v-layout row wrap  justify-center align-center >
              <v-chip-group
              multiple
              column 
              active-class="primary--text"  v-model="select" 
            >
              <v-chip v-for="genre in genres" :key="genre" :value="genre"   >
                {{ genre }}
              </v-chip>
          </v-chip-group>
         </v-layout>
        <v-row >
            <v-layout justify-center ma-10 >
              <v-btn class="ma-2" large color="indigo white--text" @click="orderbyview()">조회순<v-icon>{{viewitem.icon}}</v-icon></v-btn>
              <v-btn class="ma-2" large color="indigo white--text" @click="orderbyrating()">평점순 <v-icon>{{ratingitem.icon}}</v-icon></v-btn>
              <v-btn class="ma-2" large color="indigo white--text" @click="reset()">Reset</v-btn>
            </v-layout>
        </v-row>
        <v-row>
            <v-layout justify-center pa-10>
              <v-btn large color="indigo white--text" @click="onSubmit">Search</v-btn>
            </v-layout>
        </v-row>
      </v-container>
      <v-overlay :value="progress" :z-index="1">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
  </v-form>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  props: {
    submit: {
      type: Function,
      default: () => {}
    }
  },
  computed:{
    ...mapState({
      movieList: state => state.data.movieSearchList
    }),
    progress: function () {
      if(this.movieList.length==0&& this.flag){ 
        this.flag=false
        return true
      }else if(this.movieList.length==0 && !this.flag){ 
        return false
      }else if(this.movieList.length!=0 && !this.flag){ 
        return false
      }  
      else if(this.movieList.length!=0 && this.flag){ 
       this.flag=false
        return true
      }
    },
  },
  data: () => ({
    select:[],
    title: "",
    viewitem: {label:'조회순',value:'',icon:"poll",cnt:0},
    ratingitem:{label:'평점순',value:'',icon:"poll",cnt:0},
    iconitem:[{icon:"poll",value:""},
    {icon:"arrow_downward",value:"desc"},
    {icon:"arrow_upward",value:"asc"},],
    genres: [
      'Action',
      'Adventure' ,
      'Animation' ,
      "Children's" ,
      'Comedy',
      'Crime',
      'Documentary',
      'Drama',
      'Fantasy',
      'Film-Noir',
      'Horror',
      'Musical',
      'Mystery',
      'Romance',
      'Sci-Fi',
      'Thriller',
      'War',
      'Western'
      ],
      flag:false
  }),
  methods: {
    onSubmit: function() {
      const params = {
        viewcnt: this.viewitem.value,
        rating: this.ratingitem.value,
        title: this.title,
        select: this.select.join(',')
      };

      this.flag=true
      this.submit(params);
    },
    orderbyview(){
      this.viewitem.cnt+=1
      this.viewitem.cnt=this.viewitem.cnt%3
      this.viewitem.icon=this.iconitem[this.viewitem.cnt].icon
      this.viewitem.value=this.iconitem[this.viewitem.cnt].value
    },
    orderbyrating(){
      this.ratingitem.cnt+=1
      this.ratingitem.cnt=this.ratingitem.cnt%3
      this.ratingitem.icon=this.iconitem[this.ratingitem.cnt].icon
      this.ratingitem.value=this.iconitem[this.ratingitem.cnt].value
    },
    reset(){
      this.title=""
      this.select=[]
      this.viewitem.cnt=0
      this.viewitem.icon=this.iconitem[0].icon
      this.viewitem.value=this.iconitem[0].value
      this.ratingitem.cnt=0
      this.ratingitem.icon=this.iconitem[0].icon
      this.ratingitem.value=this.iconitem[0].value
    }
  }
};
</script>