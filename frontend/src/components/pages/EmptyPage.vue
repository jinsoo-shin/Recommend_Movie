<template>
  <v-flex shrink style="text-align:center">
    <v-sheet height="590">
    <v-calendar
      type="month"
      now=date
      value=date
      light
      :events="events"
    ></v-calendar>
  </v-sheet>
  </v-flex>
</template>

<script>
export default {
    data: () => ({
      date: null,
      events: [
        {
          name: 'Vacation',
          start: '2019-09-22',
          end: '2019-09-30',
        },
        {
          name: 'Meeting',
          start: '2019-09-07',
        },
        {
          name: "SH's Birthday",
          start: '2019-10-04',
        },
        {
          name: 'New Month',
          start: '2019-09-01',
        },
        {
          name: 'Conference',
          start: '2019-09-21',
        },
        {
          name: 'ThanksGivingDay',
          start: '2019-09-12',
          end: '2019-09-16',
        },
      ],
    }),
    mounted() {
      this.date = new Date();
    }
  }
</script>