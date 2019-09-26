<template>
  <div>
    <v-container>
      <!-- {{userdata}} -->
      <h1 style="text-align:center">마이페이지</h1>
      <br>
      <!-- <p>아이디 : user{{userdata.id}} </p> -->
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="3">
          <v-select
            :items="subitems.age"
            item-text="text"
            item-value="value"
            label="나이"
            outlined
            v-model="age"
          ></v-select>
        </v-col>
        <v-btn @click="test()">나이확인</v-btn>
      </v-row>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="3">
          <v-select
            :items="subitems.gender"
            item-text="text"
            item-value="value"
            label="성별"
            outlined
            v-model="gender"
          ></v-select>  
        </v-col>
      </v-row>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="3">
          <v-select
            :items="subitems.occupation"
            item-text="text"
            item-value="value"
            label="직업선택"
            outlined
            v-model="job"
          ></v-select>
        </v-col>
      </v-row>

      <v-btn @click="modify_user()">수정하기</v-btn>
    </v-container>
  </div>
</template>

<script>
import axios from "axios"
const apiUrl = '/api' 

export default {
  name: 'MyPage',
  data: ()=>({
    userdata : null,
    user_profile : null,
    userid : 0,
    age : 0,
    gender : "",
    job: "",
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
    }
  }),
  mounted(){
    // 유저 데이터 불러오기
    this.userdata = JSON.parse(sessionStorage.getItem('user'));
    this.userid = this.userdata.id;

    this.user_profile = JSON.parse(sessionStorage.getItem('user_temp'));
    this.age = this.user_profile.age;
    this.job = this.user_profile.occupation;
    this.gender = this.user_profile.gender;

    // switch(this.age) {
    //   case 1:
    //     this.age = "Under 18";
    //     break;
    //   case 18:
    //     this.age = "18-24";
    //     break;
    //   case 25:
    //     this.age = "25-34";
    //     break;
    //   case 35:
    //     this.age = "35-44";
    //     break;
    //   case 45:
    //     this.age = "45-49";
    //     break;
    //   case 50:
    //     this.age = "50-55";
    //     break;
    //   case 56:
    //     this.age = "56+";
    //     break;        
    // }

    console.log("나이", this.age);

    // const params = {
    //   user_id: this.userdata.id,
    //   expiration: "" // 현재 날짜 + 30 스트링으로 보내야함
    // };

    // axios.get(`${apiUrl}/subscribe/`, {
    //   params,
    //   }).then(response => {
    //     // this.silmilar_movies=response.data
    // })

  },
  methods: {
    modify_user() {
      // const params = {
      //   id: this.userdata.id, // 이거 user앞에 붙여야할까?
      //   age: 0,
      //   occupation: 0,
      //   gender: '' // 얘는 char?str?
      // };

      // axios.put(`${apiUrl}/auth_views/update_user`, {
      //   params,
      //   }).then(response => {
      //     console.log(response);
      //   })

      alert("구현중입니다.");
    },
    subscribe_1mon() {
      const params = {
        period: "1mon",
        user_id: this.userdata.id,
      };

      axios.post(`${apiUrl}/subscribe/`, {
        params,
        }).then(response => {
          console.log(response);
        })
    },
    test() {
      alert(this.age)
    }



  }
}
</script>
