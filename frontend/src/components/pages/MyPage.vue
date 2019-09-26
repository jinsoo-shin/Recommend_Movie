<template>
  <div>
    <v-container>
        {{userdata}}
      <v-layout>
        <v-flex>
          <p>구독현황</p>
          
        </v-flex>
      </v-layout>

    </v-container>
  </div>
</template>

<script>
import axios from "axios"
const apiUrl = '/api' 

export default {
  name: 'MyPage',
  data: ()=>({
    userdata : null
  }),
  mounted(){
    this.userdata = JSON.parse(sessionStorage.getItem('user'));
    console.log(typeof this.userdata);

      // const params = {
      //   user_id: this.userdata.id,
      //   expiration: "" // 현재 날짜 + 30 스트링으로 보내야함
      // };

      // axios.get(`${apiUrl}/subscribe/`, {
      //   params,
      //   }).then(response => {
      //     // this.silmilar_movies=response.data
      //   })

  },
  methods: {
    subscribe_1mon() {
      const params = {
        period: "1mon",
        user_id: this.userdata.id,
        expiration: "" // 현재 날짜 + 30 스트링으로 보내야함
      };

      axios.post(`${apiUrl}/subscribe/`, {
        params,
        }).then(response => {
          console.log(response);
        })
    }



  }
}
</script>
