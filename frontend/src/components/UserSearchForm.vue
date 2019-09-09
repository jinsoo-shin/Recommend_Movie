<template>
  <v-form ref="form">
    <v-container>
      <v-row>
          <v-col cols="12" sm="12">
            <v-text-field v-model="username" label="유저 이름" @keydown.prevent.enter="onUserSubmit" />
          </v-col>
        </v-row>
        <v-row>
            <v-layout justify-center pa-10>
              <v-btn large color="indigo white--text" @click="onUserSubmit">Search</v-btn>
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
    usersubmit: {
      type: Function,
      default: () => {}
    }
  },
  computed:{
    ...mapState({
      userList: state => state.data.userSearchList
    }),
    progress: function () {
      if(this.userList.length==0&& this.flag){ 
        this.flag=false
        return true
      }else if(this.userList.length==0 && !this.flag){ 
        return false
      }else if(this.userList.length!=0 && !this.flag){ 
        return false
      }else if(this.userList.length!=0 && this.flag){ 
       this.flag=false
        return true
      }
    },
  },
  data: () => ({
    select:[],
    username: "",
    flag:false
  }),
  methods: {
    onUserSubmit: function() {
      const params = {
        username: this.username,
      };
      this.usersubmit(params);
      this.flag=true
    },
  }
};
</script>