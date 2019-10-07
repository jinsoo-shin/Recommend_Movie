<template>
  <div>
    <v-container>

      <h1 style="text-align:center">마이페이지</h1>
      <br>
      
      <v-row>
        <v-spacer></v-spacer><v-spacer></v-spacer>
        <v-col cols="12" sm="4" md="4" xs="12">
          <h2 style="text-align:center">회원 정보 수정</h2> <br>
          <h3>아이디 : user {{userid}} </h3> <br>
            <v-select
              :items="subitems.age"
              item-text="text"
              item-value="value"
              label="나이"
              outlined
              v-model="age"
            ></v-select>
            <v-select
              :items="subitems.gender"
              item-text="text"
              item-value="value"
              label="성별"
              outlined
              v-model="gender"
            ></v-select>
            <v-select
              :items="subitems.occupation"
              item-text="text"
              item-value="value"
              label="직업선택"
              outlined
              v-model="job"
            ></v-select>
          <v-btn @click="modify_user()" color="info">수정하기</v-btn>
          <!-- 정보수정 박스 -->
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="6" md="5" xs="12" style="text-align:center;">
          <h2 style="text-align:center">구독</h2> <br>
          <span style="font-size:1.3em; font-weight:bold;">구독 만료일 : {{expiration}}</span><span>에 만료됨</span>
          <br><br>
          <v-row justify="center">
          <v-btn @click="subscribe('1mon')" color="red">1개월 구독</v-btn> &nbsp;&nbsp;
          <v-btn @click="subscribe('3mon')" color="red">3개월 구독</v-btn> &nbsp;&nbsp;
          <v-btn @click="subscribe('1year')" color="red">1년 구독</v-btn>
          <!-- 구독 박스 -->
          </v-row>
        </v-col>
        <v-spacer></v-spacer><v-spacer></v-spacer>
        <!-- 마이페이지 박스 -->
      </v-row>


       <br><br><br>
      <v-row>
        <v-col>
          <h1 style="text-align:center">평점 수정</h1> <br>
          <h2>영화 리스트</h2>
        </v-col>
      </v-row>
      <br>
      <v-row>
        <v-col>
          <v-card color="#7f7f7f">
                    <v-card-title>
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
                        :items="movielist"
                        :search="search"
                        show-expand
                        item-key="movieid"
                        :single-expand="singleExpand"
                        height="25vmax"
                    >
                    <template v-slot:expanded-item="{ headers, item }">
                      <td :colspan="headers.length" style="text-align:center; background:antiquewhite; border:beige solid 0.1px;">
                        <v-rating v-model="rating" half-increments hover style="display:inline" 
                          background-color="white"
                          empty-icon="$vuetify.icons.ratingFull"></v-rating>
                          
                          <v-btn 
                          :loading="loading"
                          :disabled="loading"
                          depressed
                          small
                          color="blue-grey"
                          class="ma-2 white--text"
                          fab
                          @click="PostRate(item.movieid)"
                          >
                          <v-icon dark>mdi-cloud-upload</v-icon>
                        </v-btn>
                      </td>
                    </template>
                    </v-data-table>

                    </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios"
const apiUrl = '/api' 
import Swal from 'sweetalert2'
export default {
  name: 'MyPage',
  data: ()=>({
    rating: 0,
    loader: null,
    search: "",
    loading: false,
    singleExpand: true,
    Movieheaders: [
        {
          text: 'ID',
          align: 'left',
          sortable: false,
          value: 'movieid',
        },
        { text: 'title', value: 'title' }
      ],
    userdata : null,
    user_profile : null,
    userid : 0,
    age : 0,
    gender : "",
    job: "",
    expiration: "",
    isStaff : false,
    username : "",
    movielist: [],
    subitems:{
      age:[
        {text:"Under 18",value:1},
        {text:"18-24",value:18},
        {text:"25-34",value:25},
        {text:"35-44",value:35},
        {text:"45-49",value:45},
        {text:"50-55",value:50},
        {text:"56+",value:56},
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
    this.isStaff = this.user_profile.is_staff;
    this.username = this.user_profile.username;

    if(this.age >= 1 && this.age <= 17) {
      this.age = 1;
    } else if (this.age >= 18 && this.age <= 24) {
      this.age = 18;
    } else if (this.age >= 25 && this.age <= 34) {
      this.age = 25;
    } else if (this.age >= 35 && this.age <= 44) {
      this.age = 35;
    } else if (this.age >= 45 && this.age <= 49) {
      this.age = 45;
    } else if (this.age >= 50 && this.age <= 55) {
      this.age = 50;
    }
    
    this.expiration = sessionStorage.getItem('subscribe');

    const params = {
        userid: this.userid,
        mode:"usermovie"
      };     
      axios.get(`${apiUrl}/ratings/`, {
            params,
        }).then(response => {
          this.movielist=response.data
          console.log(this.movielist)
        }) 
  },
  methods: {
    PostRate(id){
      console.log(id + "1")
        const params = {
          userid : this.userid,
          movieid : id,
          rating : this.rating
        }
        const Toast = Swal.mixin({
              toast: true,
              position: 'top-end',
              showConfirmButton: false,
              timer: 1500
            })
          axios.post(`${apiUrl}/ratings/`, { params }).then(response => {
            Toast.fire({
              type: 'success',
              title: '수정 완료!'
            })
          }).catch(error =>{
            Swal.fire({type:'error', title:'다시 시도해주세요!'})
          }).finally(rs =>{
          })
      },
    modify_user() {
      const params = {
        id: this.userid,
        age: this.age,
        gender: this.gender,
        occupation: this.job,
        is_staff: this.isStaff,
        username: this.username
      };

      axios.put(`${apiUrl}/update/user/`, {
        params,
        }).then(response => {
          sessionStorage.setItem('user_temp', JSON.stringify(params));
          alert("수정 완료했습니다.");
        })

    },
    subscribe(period_data) { // 구독 버튼
      const params = {
        period: period_data,
        user_id: this.userdata.id,
      };

      axios.post(`${apiUrl}/subscribes/`, {
        params,
        }).then(response => {
          this.expiration=response.data.expiration;
          sessionStorage.setItem('subscribe', this.expiration);
          
          if (period_data == "1mon") {
            alert("1개월 구독 되었습니다.");
          } else if (period_data == "3mon") {
            alert("3개월 구독 되었습니다.");
          } else if (period_data == "1year") {
            alert("1년 구독 되었습니다.");
          }
        })
    }

  }
}
</script>