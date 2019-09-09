<style>
.dashed-border {
     width: 100%;
     margin: auto;
     margin-top: 10%;
     margin-bottom: 10%;
     border: 2px dashed #BDBDBD;
}
</style>
<template>
<div>
  <v-layout align-center justify-center row fill-height class="mt-2">
    <v-flex sm8 lg4 text-xs-center v-if="width>=600">
      <v-layout md12 justify-center column fill-height elevation-5 style="min-height:500px;" pa-5>
		<h1 class="mt-4" style="font-family: 'Nanum Gothic Coding', monospace;">LOGIN</h1>
		<v-layout align-center>
			<v-flex text-xs-center>
				<template>
					<form xs12 sm7 md7 v-on:submit='loginWithEmail'>
						<v-text-field type='text' v-model="email" label="Name" required @keydown.prevent.enter="loginWithEmail"></v-text-field>
						<v-text-field type='password' v-model="password" label="Password" required @keydown.prevent.enter="loginWithEmail"></v-text-field>
						<v-flex md1>
						</v-flex>
						<v-btn xs12 sm4 md4 color="#A99794" block dark type='button' class="mt-4" @click="loginWithEmail" style="">로그인</v-btn>
					</form>
				</template>
			</v-flex>
		</v-layout>
		<v-flex text-xs-center>
			<hr class="dashed-border">
			<h4>아직 회원이 아니신가요?</h4>
			<v-layout row justify-center>
				<v-dialog v-model="dialog" persistent max-width="600px">
					<template v-slot:activator="{on}">
						<v-btn class="mt-3" outlined v-on="on">회원가입</v-btn>
					</template>
					<v-card>
						<v-card-title center>
							<span style="margin: 0 auto; font-family: 'Nanum Gothic Coding', monospace; font-size:xx-large; font-weight: bold;">SIGN UP</span>
						</v-card-title>
						<v-card-text>
							<div style="text-align: right; font-size:small;">
								*는 필수 입력값입니다.
							</div>
							<v-container grid-list-md>
								<v-layout wrap>
									<v-flex xs12 sm6 md4>
										<v-text-field label="닉네임*" v-model="name" style="ime-mode:disabled;" :rules="[v => !!v || '닉네임을 입력해주세요.']" required></v-text-field>
									</v-flex>
									<v-flex xs9>
										<v-text-field label="이메일*" v-model="email" :rules="emailRules" required></v-text-field>
									</v-flex>
									<v-flex xs12>
										<v-text-field label="비밀번호*" type="password" v-model="password" :rules="[v => !!v || '비밀번호를 입력해주세요.']" required></v-text-field>
									</v-flex>
									<v-flex xs12 sm6 md4>
										<v-text-field label="First Name*" v-model="fn" required></v-text-field>
									</v-flex>
									<v-flex xs12 sm6 md4>
										<v-text-field label="Last Name*" v-model="ln" required></v-text-field>
									</v-flex>
									<v-row>
										<v-flex xs12 sm4 md4>
											<v-select
												:items="age"
												label="나이"
												outlined
												v-model="select_age"
												></v-select>
										</v-flex>
										<v-flex xs12 sm6 md4>
											<v-select
												:items="occupation"
												label="직업"
												outlined
												v-model="select_occupation"
												></v-select>
										</v-flex>
										<v-flex xs12 sm6 md4>
											<v-select
												:items="gender"
												label="성별"
												outlined
												v-model="select_gender"
												></v-select>
										</v-flex>
									</v-row>
								</v-layout>
							</v-container>
						</v-card-text>
						<v-divider class="mt-12"></v-divider>
						<v-card-actions>
							<v-spacer></v-spacer>
							<v-btn outlined text @click="dialog = false" v-on:click="close">닫기</v-btn>
							<v-btn outlined text @click="dialog = false" v-on:click="registMember">가입</v-btn>
						</v-card-actions>
					</v-card>
				</v-dialog>
			</v-layout>
		</v-flex>
      </v-layout>
    </v-flex>
	<v-flex v-if="width<600" xs10 sm8 lg4 text-xs-center>
      <v-layout align-center justify-center row fill-height elevation-5 style="min-height:500px;" pa-5>
        <v-flex xs12 text-xs-center>
			<h1 class="mt-4" style="font-family: 'Nanum Gothic Coding', monospace;">LOGIN</h1>
			<template>
				<form v-on:submit='loginWithEmail'>
					<v-text-field type='text' v-model="email" label="Name" required></v-text-field>
					<v-text-field type='password' v-model="password" label="Password" required></v-text-field>
					<v-btn color="#A99794" dark type='button' style="width:100%;">로그인</v-btn>
				</form>
			</template>
			<br>
			<hr class="dashed-border">
			<h5 class="mt-3 mb-2">아직 회원이 아니신가요?</h5>
			<v-layout row justify-center>
				<v-dialog v-model="dialog" persistent max-width="600px">
					<template v-slot:activator="{on}">
						<v-btn outlined v-on="on">회원가입</v-btn>
					</template>
					<v-card>
						<v-card-title>
							<span style="margin: 0 auto; font-family: 'Nanum Gothic Coding', monospace; font-size:xx-large; font-weight: bold;">SIGN UP</span>
						</v-card-title>
						<v-card-text>
							<div style="text-align: right; font-size:small;">
								*는 필수 입력값입니다.
							</div>
							<v-container grid-list-md>
								<v-layout wrap>
									<v-flex xs12 sm6 md4>
										<v-text-field label="이름*" v-model="name" required></v-text-field>
									</v-flex>
									<v-flex xs10>
										<v-text-field label="이메일*" v-model="email" required></v-text-field>
									</v-flex>
									<v-flex xs12>
										<v-text-field label="비밀번호*" type="password" v-model="password" required></v-text-field>
									</v-flex>
									<v-flex xs12 sm6 md4>
										<v-text-field label="First Name*" v-model="fn" required></v-text-field>
									</v-flex>
									<v-flex xs12 sm6 md4>
										<v-text-field label="Last Name*" v-model="ln" required></v-text-field>
									</v-flex>
									<v-flex xs12 sm4 md4>
											<v-select
												:items="age"
												label="나이"
												outlined
												v-model="select_age"
												></v-select>
										</v-flex>
										<v-flex xs12 sm6 md4>
											<v-select
												:items="occupation"
												label="직업"
												outlined
												v-model="select_occupation"
												></v-select>
										</v-flex>
										<v-flex xs12 sm6 md4>
											<v-select
												:items="gender"
												label="성별"
												outlined
												v-model="select_gender"
												></v-select>
										</v-flex>
								</v-layout>
							</v-container>
						</v-card-text>
						<v-divider class="mt-12"></v-divider>
						<v-card-actions>
							<div style="margin:0 auto;">
								<v-btn color="indigo" text outlined @click="dialog = false" v-on:click="close">닫기</v-btn>
								<v-btn color="indigo" text outlined @click="dialog = false" v-on:click="registMember">가입</v-btn>
							</div>
						</v-card-actions>
					</v-card>
				</v-dialog>
			</v-layout>
		</v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</div>
</template>
<script>
import axios from "axios"
const apiUrl = '/api'

export default {
	name: 'LoginPage',
	data() {
		return {
			drawer: null,
			right: null,
			dialog: false,
			name: '',
			email: '',
			emailRules: [
				v => !!v || 'E-mail을 필수로 입력해주시기 바랍니다.',
				v => /.+@.+\..+/.test(v) || '올바른 E-mail 형식이 아닙니다.',
			],
			album: '',
			password: '',
			fn: '',
			ln: '',
			auth: '',
			myauth: '',
			width:0,
			select_age:'',
			select_occupation:'',
			select_gender:'',
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
	},
	created(){
	window.addEventListener('resize', this.handleResize)
    this.handleResize();
	},
	destroyed() {
    window.removeEventListener('resize', this.handleResize)
  	},
	methods: {
		handleResize() {	
			this.width = window.innerWidth;
		},
		loginWithEmail(e) {
			const params = {
			username: this.email,
			password: this.password
		};     
			axios.post(`${apiUrl}/auth/signin/`, {
					params,
			}).then(response => {
				if(!response.data)
				{
					alert("로그인 실패!")
				}
				else{
					alert("로그인 성공!")
					console.log(response)
					sessionStorage.setItem('user', response.data[0]);
					location.href="/";
				}
			}).catch(error =>{
				console.log(error)
			})
		},
		close() {
			this.name= ''
			this.email= ''
			this.password= ''
      	},
		registMember() {
			const params = {
				username : this.name,
				email: this.email,
				password: this.password,
				first_name : this.fn,
				last_name : this.ln,
				age : this.select_age,
				occupation : this.select_occupation,
				gender : this.select_gender
			};     
			axios.post(`${apiUrl}/auth/signup/`, {
					params,
			}).then(response => {
				console.log(response)
				alert("가입 성공!")
			}).catch(error =>{
			}).finally(rs =>{
				this.name= ''
				this.email= ''
				this.password= ''
			})
		},
		sendEmail() {
		}
	}
};
</script>