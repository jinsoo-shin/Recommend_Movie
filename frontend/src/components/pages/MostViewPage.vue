<!-- 특정 기준으로 많이 본 영화 검색 페이지 -->
<template>
  <v-container grid-list-md text-center>
    <v-layout justify-center wrap>
      <!-- 검색 폼 -->
      <v-flex xs6>
        <div class="display-2 pa-10">영화 검색 기능 확장</div>
        <v-form ref="form">
          <v-container fluid>
            <v-row align="center">
              <v-col class="d-flex" cols="12" sm="4">
                <v-select
                  :items="items"
                  item-text="text"
                  item-value="value"
                  label="기준"
                  outlined
                  v-model="select"
                ></v-select>
              </v-col>
              <v-col class="d-flex" cols="12" sm="6">
                <v-select
                  :items="subitems[select]"
                  item-text="text"
                  item-value="value"
                  label="조건"
                  outlined
                  v-model="where"
                ></v-select>
              </v-col>
              <v-col class="d-flex" cols="12" sm="2" style="margin-bottom: 30px;">
                 <v-btn large color="indigo white--text" @click="submit">Search</v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-flex>
      <!-- 검색 결과 -->
      <v-flex xs8 v-if="searchdata.length!=0">
        <v-data-table
          :headers="headers"
          :items="searchdata"
          :items-per-page="10"
          class="elevation-1"
       ></v-data-table>
      </v-flex>
    </v-layout>
    <v-overlay :value="progress" :z-index="0">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </v-container>
</template>

<script>
import axios from "axios"
const apiUrl = '/api'
import { mapState, mapActions } from "vuex";
import MovieSearchForm from "../MovieSearchForm";
import MovieList from "../MovieList";
export default {
  components: {
    MovieList,
    MovieSearchForm
  },
   data () {
      return {
        headers: [
          {
            text: 'Title',
            align: 'left',
            sortable: false,
            value: 'title',
          },
          { text: 'Count', value: 'movie_count', align: 'left', },
        ],
        select:"",
        where:"",
        items: [{text:"연령대",value:"age"},{text:"직업",value:"occupation"},{text:"성별",value:"gender"}],
        subitems:{
          age:[
            {text:"Under 18",value:"1"},
            {text:"18-24",value:"18"},
            {text:"25-34",value:"25"},
            {text:"35-44",value:"35"},
            {text:"45-49",value:"45"},
            {text:"50-55",value:"50"},
            {text:"56+",value:"56"},
            ]
          ,occupation:[
            {text:"other",value:"other"},
            {text:"academic/educator",value:"academic/educator"},
            {text:"artist",value:"artist"},
            {text:"clerical/admin",value:"clerical/admin"},
            {text:"college/grad student",value:"college/grad student"},
            {text:"customer service",value:"customer service"},
            {text:"doctor/health care",value:"doctor/health care"},
            {text:"executive/managerial",value:"executive/managerial"},
            {text:"farmer",value:"farmer"},
            {text:"homemaker",value:"homemaker"},
            {text:"K-12 student",value:"K-12 student"},
            {text:"lawyer",value:"lawyer"},
            {text:"programmer",value:"programmer"},
            {text:"retired",value:"retired"},
            {text:"sales/marketing",value:"sales/marketing"},
            {text:"scientist",value:"scientist"},
            {text:"self-employed",value:"self-employed"},
            {text:"technician/engineer",value:"technician/engineer"},
            {text:"tradesman/craftsman",value:"tradesman/craftsman"},
            {text:"unemployed",value:"unemployed"},
            {text:"writer",value:"writer"},
          ]
          ,gender:[
            {text:"여성",value:"F"},
            {text:"남성",value:"M"}
            ]
        },
        searchdata:[],
        flag:false,
      }
  },
  computed:{
    progress(){
      if(this.flag && this.searchdata.length==0){
        this.flag=false
        return true
      }else{
        return false
      }
    }
  },
  methods: {
    submit(){
      if((this.select&&this.where)||(!this.select&&!this.where)){
        const params = {
        mode: "mostview",
        select: this.select,
        where: this.where,
        };
        this.flag=true
        this.searchdata=[]
        axios.get(`${apiUrl}/ratings/`, {
        params,
        }).then(response => {
          this.searchdata=response.data
        }) 
      }else if(!this.select||!this.where){
        alert("기준이나 조건을 선택해주세요.")
      }

    }
  }
};
</script>
