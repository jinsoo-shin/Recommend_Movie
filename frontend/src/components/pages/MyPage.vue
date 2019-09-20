<template>
  <div>
      {{userdata}}
  </div>
</template>

<script>
export default {
  name: 'MyPage',
  data: ()=>({
    userdata : null
  }),
  mounted(){
    this.userdata = JSON.parse(sessionStorage.getItem('user'));
    console.log(typeof this.userdata);
  }
}
</script>
