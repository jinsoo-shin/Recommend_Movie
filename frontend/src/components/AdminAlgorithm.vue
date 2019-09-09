<template>
<div>
  <v-container fluid>
    <v-row align="center">
       <v-col class="d-flex" cols="12" sm="6">
        <v-select
          :items="items"
          item-text="text"
          item-value="value"
          label="클러스터링 알고리즘"
          v-model="selectalgorithm"
          outlined
        ></v-select>
      </v-col>
       <v-col class="d-flex" cols="12" sm="6">
      </v-col>
       <v-col class="d-flex pb-12 pr-4" cols="12" sm="6" >
          <v-subheader class="pl-0">클러스터 갯수</v-subheader>
          <v-slider
            v-model="sliderCluster.val"
            class="align-center"
            :color="sliderCluster.color"
            min="10" max="20"
            hide-details
            thumb-label
          >
            <template v-slot:append>
              <v-text-field
                v-model="sliderCluster.val"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px"
              ></v-text-field>
            </template>
          </v-slider>
      </v-col>
       <v-col class="d-flex pb-12 pr-4" cols="12" sm="6" >
          <v-subheader class="pl-0">Data</v-subheader>
          <v-slider
            v-model="sliderRating.val"
            class="align-center"
            :color="sliderRating.color"
            min="10" max="100"
            hide-details
            thumb-label
          >
            <template v-slot:append>
              <v-text-field
                v-model="sliderRating.val"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                suffix='%'
              ></v-text-field>
            </template>
          </v-slider>
      </v-col>
    </v-row>
    <v-row>
          <v-layout justify-center>
            <v-btn large color="indigo white--text" @click="submit">Search</v-btn>
          </v-layout>
    </v-row>
  </v-container>
  <v-container v-if="series.length!=0">
    <v-list-item-content >
      <v-list-item-title class="headline mb-1 ml-4">결과</v-list-item-title>
      <v-list-item-subtitle class="ml-4">{{selectalgorithm}} 클러스터링 알고리즘</v-list-item-subtitle>
      <v-list-item-subtitle class="ml-4">클러스터 N : {{sliderCluster.val}}</v-list-item-subtitle>
    </v-list-item-content>
  <v-card color="#FFFFFF">
    <v-card-text>
     <!--결과 페이지-->
      <div id="chart">
      <apexchart type=scatter height=350 :options="chartOptions" :series="series" id="chartdata" />
    </div>
    </v-card-text>
  </v-card>
  </v-container>

<v-divider></v-divider>

  <div>
<v-container fluid>
  <v-container>
    <v-row>
        <v-layout justify-center>
          <v-btn large color="indigo white--text" @click="get_km_self">비교하기</v-btn>
        </v-layout>
    </v-row>
  </v-container>
    <v-row v-if="km_self.length!=0">
      <v-col class="d-flex" cols="12" sm="12">
        <v-card color="#FFFFFF" width="100%">
          <v-card-text>
          <!--결과 페이지-->
            <div id="chart">
            <apexchart type=scatter height=350 :options="chartOptions" :series="km_self" id="chartdata" />
          </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

  </div>


    <v-overlay :value="progress" :z-index="2">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
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
</div>
</template>
<script>
import Vue from 'vue'
import ApexCharts from 'apexcharts'
import VueApexCharts from 'vue-apexcharts'
import axios from "axios"
const apiUrl = '/api'
Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)
  export default {
    components: {
      ApexCharts,
      },
    data () {
      return {
        km_self:[],
        snackbar:false,
        snackbartext:"로딩 완료!",
        flag:false,
        selectalgorithm:"",
        selectmodel:"",
        items: [{text:"Kmeans",value:"Kmeans"},{text:"Hierarchical",value:"Hierarchical"},{text:"EM(Gaussian Mixture)",value:"EM"}],
        subitems: [{text:"영화",value:"movie"},{text:"유저",value:"user"}],
        sliderCluster: { label: 'color', val: 20, color: 'red darken-1' ,backcolor:'blue-grey darken-4'},
        sliderRating: { label: 'color', val: 10, color: 'red darken-1' ,backcolor:'blue-grey darken-4'},
        series: [ 
            
        ],
        chartOptions: {
          chart: {
            zoom: {
              enabled: true,
              type: 'xy'
            }
          },
          xaxis: {
              tickAmount: 10,
              labels: {
                  formatter: function(val) {
                      return parseFloat(val).toFixed(1)
                  }
              }
          },
          yaxis: {
            tickAmount: 7
          }
      }
      }
    },
     computed:{
    progress(){
      if(this.flag && this.series.length==0){
        this.flag=false
        return true
      }else if(!this.flag && this.series.length!=0){
        this.snackbar=true
        return false
      }else{
        return false
      }
    },
  },
    methods: {
      submit(){
        this.series=[]
        this.flag=true
        if(!this.selectalgorithm){
          this.selectalgorithm="Kmeans"
        }
        const params = {
          algorithm:this.selectalgorithm,
          cluster_num: this.sliderCluster.val,
          rating_percent: this.sliderRating.val,
        };
        axios.post(`${apiUrl}/recommends/`, {
        params,
        }).then(response => {
         this.series=response.data.series
        }) 
      },
      get_km_self(){
        this.km_self=[]
        const params = {
          algorithm:"Kmeans_self",
        };
        axios.post(`${apiUrl}/recommends/`, {
        params,
        }).then(response => {
         this.km_self=response.data.series
        }) 
      }
    }
  }
</script>
<style>
#chartdata{
 color: rgb(55, 61, 63);
}
</style>