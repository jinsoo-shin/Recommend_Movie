<template>
  <v-flex shrink style="text-align:center">
    <v-flex v-if="user">
      <v-flex v-if="user.username!=='admin'">
        <v-flex v-if="isSubscribe">
          <kNNUserBase></kNNUserBase>
          <v-divider class="ma-4"></v-divider>
          <kNNItemBase></kNNItemBase>
        </v-flex>
        <v-flex v-if="!isSubscribe">
          구독을 하셔야 유저별 맞춤 영화 추천 서비스를 받을 수 있습니다.
        </v-flex>
      </v-flex>
      <v-flex v-if="user.username==='admin'">
          관리자 계정입니다
      </v-flex>
    </v-flex>
     <v-flex v-if="!user">
      로그인을 하셔야 유저별 맞춤 영화 추천 서비스를 받을 수 있습니다.
    </v-flex>
    <!-- <v-divider class="ma-4"></v-divider> -->
    <!-- <kNNUserBase></kNNUserBase> -->
  </v-flex>
</template>

<script>
import axios from "axios"
const apiUrl = '/api'
import kNNUserBase from "../kNNUserBase"
import kNNItemBase from "../kNNItemBase"
export default {
    components: {
    kNNUserBase,kNNItemBase
  },
    data: () => ({
      data:[
      ],
      model:null,
      str: '',
      user:null,
      subscribe:null
    }),
    computed:{
      isSubscribe(){
        if(this.subscribe){
          var today = new Date();
          var dateArray = this.subscribe.split("-");  
          var sub = new Date(dateArray[0],dateArray[1],dateArray[2]);

          var between = sub.getTime()-today.getTime();
          if(between>0){
            return true;
          }else{
            return false;
          }
        }else{
          return false;
        }
      }
    },
    mounted() {
      if(sessionStorage.getItem('user')){
        this.user=JSON.parse(sessionStorage.getItem('user'))
      }
      if(sessionStorage.getItem('subscribe')){
        this.subscribe=sessionStorage.getItem('subscribe')
      }
      
      //   // console.log(this.user.id)
      //   const params = {
      //     userid: this.user.id,
      //   };     
      //   axios.get(`${apiUrl}/test/`, {
      //         params,
      //     }).then(response => {
      //       this.data=response.data
      //     }) 
      // }
    }
  }
</script>