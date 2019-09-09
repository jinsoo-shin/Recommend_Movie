<template>
  <v-container class="pa-2" fluid grid-list-md>
    <v-layout column>
      <v-flex v-for="card in userListCardsSliced" :key="card.id" pa-2>
        <UserListCard
          :userid="card.userid"
          :username="card.username"
          :gender="card.gender"
          :age="card.age"
          :occupation="card.occupation"
        />
      </v-flex>
      <v-pagination v-if="maxPages > 1" v-model="page" :length="maxPages" />
    </v-layout>
  </v-container>
</template>

<script>
import UserListCard from "./UserListCard"
export default {
  components: {
    UserListCard
  },
  props: {
    userListCards: {
      type: Array,
      default: () => new Array(),
    },
  },
  data: () => ({
    cardsPerPage: 10,
    page: 1,
    overlay:false
  }),
  computed: {
    // pagination related variables
    userListEmpty: function() {
      return this.userListCards.length === 0;
    },
    maxPages: function() {
      return Math.floor((this.userListCards.length + this.cardsPerPage - 1) / this.cardsPerPage)
    },
    userListCardsSliced: function() {
      return this.userListCards.slice(this.cardsPerPage * (this.page - 1), this.cardsPerPage * this.page)
    },
    progress: function () {
      if(this.userListCards.length!=0){
        return true
      }else{
        return false
      }
    }
    
  },
};
</script>